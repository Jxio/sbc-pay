# Copyright © 2023 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Task to create AP file for FAS refunds and Disbursement via EFT for non-government orgs without a GL."""

import time
import traceback
from datetime import date, datetime, timedelta, timezone
from typing import List

from flask import current_app
from more_itertools import batched
from pay_api.models import CorpType as CorpTypeModel
from pay_api.models import DistributionCode as DistributionCodeModel
from pay_api.models import EFTRefund as EFTRefundModel
from pay_api.models import EjvFile as EjvFileModel
from pay_api.models import EjvHeader as EjvHeaderModel
from pay_api.models import EjvLink as EjvLinkModel
from pay_api.models import Invoice as InvoiceModel
from pay_api.models import Receipt as ReceiptModel
from pay_api.models import Refund as RefundModel
from pay_api.models import RoutingSlip as RoutingSlipModel
from pay_api.models import db
from pay_api.utils.enums import (
    DisbursementStatus,
    EFTShortnameRefundStatus,
    EjvFileType,
    EJVLinkType,
    InvoiceStatus,
    PaymentMethod,
    RoutingSlipStatus,
)
from sentry_sdk import capture_message
from sqlalchemy import Date, cast

from tasks.common.cgi_ap import CgiAP
from tasks.common.dataclasses import APHeader, APLine, APSupplier


class ApTask(CgiAP):
    """Task to create AP (Accounts Payable) Feeder Files.

    Purpose:
    1. Create mailed out cheques for unused amounts on routing slips.
    2. Distribution of funds to non government partners without a GL code (EFT).

    """

    @classmethod
    def create_ap_files(cls):
        """Create AP files and upload to CGI.

        Steps:
        1. Find all routing slip with status REFUND_AUTHORIZED.
        2. Create AP file and upload to SFTP.
        3. After some time, a feedback file will arrive and Payment-reconciliation queue will move these
           routing slips to REFUNDED. (filter out)
        4. Find all BCA invoices with status PAID. (DRAWDOWN/INTERNAL EXCLUDED)
           These invoices need to be disbursement status ERRORED or None
        5. Find all BCA invoices with status REFUND_REQUESTED or REFUNDED. (DRAWDOWN/INTERNAL EXCLUDED)
           These invoices need to be disbursement status COMPLETED
        6. Create AP file and upload to SFTP.
        7. After some time, a feedback file will arrive and Payment-reconciliation queue will set disbursement
           status to COMPLETED or REVERSED (filter out)
        8. Find all EFT refunds with status APPROVED.
        9. Create AP file and upload to SFTP.
        10. After some time, a feedback file will arrive and Payment-reconciliation queue will move these
            EFT refunds to REFUNDED. (filter out)
        """
        try:
            cls._create_routing_slip_refund_file()
        except Exception as e:
            capture_message(
                f"Error creating routing slip refund file ERROR : {str(e)}",
                level="error",
            )
            current_app.logger.error(f"{{error: {str(e)}, stack_trace: {traceback.format_exc()}}}")
        try:
            cls._create_non_gov_disbursement_file()
        except Exception as e:
            capture_message(
                f"Error creating non gov disbursement file ERROR : {str(e)}",
                level="error",
            )
            current_app.logger.error(f"{{error: {str(e)}, stack_trace: {traceback.format_exc()}}}")
        try:
            cls._create_eft_refund_file()
        except Exception as e:
            capture_message(
                f"Error creating eft refund file ERROR : {str(e)}",
                level="error",
            )
            current_app.logger.error(f"{{error: {str(e)}, stack_trace: {traceback.format_exc()}}}")

    @classmethod
    def _create_eft_refund_file(cls):
        """Create AP file for EFT refunds and upload to CGI."""
        cls.ap_type = EjvFileType.EFT_REFUND
        eft_refunds_dao = (
            db.session.query(EFTRefundModel)
            .filter(EFTRefundModel.status == EFTShortnameRefundStatus.APPROVED.value)
            .filter(EFTRefundModel.disbursement_status_code.is_(None))
            .filter(EFTRefundModel.refund_amount > 0)
            .all()
        )

        current_app.logger.info(f"Found {len(eft_refunds_dao)} to refund.")

        for refunds in list(batched(eft_refunds_dao, 250)):
            ejv_file_model = EjvFileModel(
                file_type=cls.ap_type.value,
                file_ref=cls.get_file_name(),
                disbursement_status_code=DisbursementStatus.UPLOADED.value,
            ).flush()
            batch_number: str = cls.get_batch_number(ejv_file_model.id)
            ap_content: str = cls.get_batch_header(batch_number)
            batch_total = 0
            line_count_total = 0
            for eft_refund in refunds:
                current_app.logger.info(
                    f"Creating refund for EFT Refund {eft_refund.id}, Amount {eft_refund.refund_amount}."
                )
                ap_header = APHeader(
                    total=eft_refund.refund_amount,
                    invoice_number=eft_refund.id,
                    invoice_date=eft_refund.created_on,
                    ap_supplier=APSupplier(eft_refund.cas_supplier_number, eft_refund.cas_supplier_site)
                )
                ap_content = f"{ap_content}{cls.get_ap_header(ap_header)}"
                ap_line = APLine(
                    total=eft_refund.refund_amount,
                    invoice_number=eft_refund.id,
                    line_number=line_count_total + 1,
                    ap_supplier=APSupplier(eft_refund.cas_supplier_number, eft_refund.cas_supplier_site)
                )
                ap_content = f"{ap_content}{cls.get_ap_invoice_line(ap_line)}"
                line_count_total += 2
                if ap_comment := cls.get_eft_ap_comment(
                    eft_refund.comment,
                    eft_refund.id,
                    eft_refund.short_name_id,
                    supplier_line=APSupplier(eft_refund.cas_supplier_number, eft_refund.cas_supplier_site)
                ):
                    ap_content = f"{ap_content}{ap_comment:<40}"
                    line_count_total += 1
                batch_total += eft_refund.refund_amount
                eft_refund.disbursement_status_code = DisbursementStatus.UPLOADED.value

            batch_trailer: str = cls.get_batch_trailer(batch_number, batch_total, control_total=line_count_total)
            ap_content = f"{ap_content}{batch_trailer}"
            cls._create_file_and_upload(ap_content)

    @classmethod
    def _create_routing_slip_refund_file(
        cls,
    ):  # pylint:disable=too-many-locals, too-many-statements
        """Create AP file for routing slip refunds (unapplied routing slip amounts) and upload to CGI."""
        cls.ap_type = EjvFileType.REFUND
        routing_slips_dao: List[RoutingSlipModel] = (
            db.session.query(RoutingSlipModel)
            .filter(RoutingSlipModel.status == RoutingSlipStatus.REFUND_AUTHORIZED.value)
            .filter(RoutingSlipModel.refund_amount > 0)
            .all()
        )

        current_app.logger.info(f"Found {len(routing_slips_dao)} to refund.")
        if not routing_slips_dao:
            return

        for routing_slips in list(batched(routing_slips_dao, 250)):
            ejv_file_model: EjvFileModel = EjvFileModel(
                file_type=cls.ap_type.value,
                file_ref=cls.get_file_name(),
                disbursement_status_code=DisbursementStatus.UPLOADED.value,
            ).flush()

            batch_number: str = cls.get_batch_number(ejv_file_model.id)
            ap_content: str = cls.get_batch_header(batch_number)
            batch_total = 0
            total_line_count: int = 0
            for rs in routing_slips:
                current_app.logger.info(f"Creating refund for {rs.number}, Amount {rs.refund_amount}.")
                refund: RefundModel = RefundModel.find_by_routing_slip_id(rs.id)
                ap_header = APHeader(
                    total=rs.refund_amount,
                    invoice_number=rs.number,
                    invoice_date=datetime.now(tz=timezone.utc)
                )
                ap_content = f"{ap_content}{cls.get_ap_header(ap_header)}"
                ap_line = APLine(total=rs.refund_amount, invoice_number=rs.number, line_number=1)
                ap_content = f"{ap_content}{cls.get_ap_invoice_line(ap_line)}"
                ap_content = f"{ap_content}{cls.get_ap_address(refund.details, rs.number)}"
                total_line_count += 3
                if ap_comment := cls.get_rs_ap_comment(refund.details, rs.number):
                    ap_content = f"{ap_content}{ap_comment:<40}"
                    total_line_count += 1
                batch_total += rs.refund_amount
                rs.status = RoutingSlipStatus.REFUND_UPLOADED.value
            batch_trailer = cls.get_batch_trailer(batch_number, float(batch_total), control_total=total_line_count)
            ap_content = f"{ap_content}{batch_trailer}"

            cls._create_file_and_upload(ap_content)

    @classmethod
    def get_invoices_for_disbursement(cls, partner):
        """Return invoices for disbursement. Used by EJV and AP."""
        disbursement_date = datetime.now(tz=timezone.utc).replace(tzinfo=None) - timedelta(
            days=current_app.config.get("DISBURSEMENT_DELAY_IN_DAYS")
        )
        invoices: List[InvoiceModel] = (
            db.session.query(InvoiceModel)
            .filter(InvoiceModel.invoice_status_code == InvoiceStatus.PAID.value)
            .filter(
                InvoiceModel.payment_method_code.notin_(
                    [
                        PaymentMethod.INTERNAL.value,
                        PaymentMethod.DRAWDOWN.value,
                        PaymentMethod.EFT.value,
                    ]
                )
            )
            .filter(
                (InvoiceModel.disbursement_status_code.is_(None))
                | (InvoiceModel.disbursement_status_code == DisbursementStatus.ERRORED.value)
            )
            .filter(~InvoiceModel.receipts.any(cast(ReceiptModel.receipt_date, Date) >= disbursement_date.date()))
            .filter(InvoiceModel.corp_type_code == partner.code)
            .all()
        )
        current_app.logger.info(invoices)
        return invoices

    @classmethod
    def get_invoices_for_refund_reversal(cls, partner):
        """Return invoices for refund reversal."""
        # REFUND_REQUESTED for credit card payments, CREDITED for AR and REFUNDED for other payments.
        refund_inv_statuses = (
            InvoiceStatus.REFUNDED.value,
            InvoiceStatus.REFUND_REQUESTED.value,
            InvoiceStatus.CREDITED.value,
        )

        invoices: List[InvoiceModel] = (
            db.session.query(InvoiceModel)
            .filter(InvoiceModel.invoice_status_code.in_(refund_inv_statuses))
            .filter(
                InvoiceModel.payment_method_code.notin_(
                    [
                        PaymentMethod.INTERNAL.value,
                        PaymentMethod.DRAWDOWN.value,
                        PaymentMethod.EFT.value,
                    ]
                )
            )
            .filter(InvoiceModel.disbursement_status_code == DisbursementStatus.COMPLETED.value)
            .filter(InvoiceModel.corp_type_code == partner.code)
            .all()
        )
        current_app.logger.info(invoices)
        return invoices

    @classmethod
    def _create_non_gov_disbursement_file(cls):  # pylint:disable=too-many-locals
        """Create AP file for disbursement for non government entities without a GL code via EFT and upload to CGI."""
        cls.ap_type = EjvFileType.NON_GOV_DISBURSEMENT
        bca_partner = CorpTypeModel.find_by_code("BCA")
        # TODO these two functions need to be reworked when we onboard BCA again.
        total_invoices: List[InvoiceModel] = cls.get_invoices_for_disbursement(
            bca_partner
        ) + cls.get_invoices_for_refund_reversal(bca_partner)

        current_app.logger.info(f"Found {len(total_invoices)} to disburse.")
        if not total_invoices:
            return

        # 250 MAX is all the transactions the feeder can take per batch.
        for invoices in list(batched(total_invoices, 250)):
            bca_distribution = cls._get_bca_distribution_string()
            ejv_file_model: EjvFileModel = EjvFileModel(
                file_type=cls.ap_type.value,
                file_ref=cls.get_file_name(),
                disbursement_status_code=DisbursementStatus.UPLOADED.value,
            ).flush()
            # Create a single header record for this file, provides query ejv_file -> ejv_header -> ejv_invoice_links
            # Note the inbox file doesn't include ejv_header when submitting.
            ejv_header_model: EjvFileModel = EjvHeaderModel(
                partner_code="BCA",
                disbursement_status_code=DisbursementStatus.UPLOADED.value,
                ejv_file_id=ejv_file_model.id,
            ).flush()

            batch_number: str = cls.get_batch_number(ejv_file_model.id)
            ap_content: str = cls.get_batch_header(batch_number)
            batch_total = 0
            control_total: int = 0
            for inv in invoices:
                disbursement_invoice_total = inv.total - inv.service_fees
                batch_total += disbursement_invoice_total
                if disbursement_invoice_total == 0:
                    continue
                ap_header = APHeader(
                    total=disbursement_invoice_total,
                    invoice_number=inv.id,
                    invoice_date=inv.created_on
                )
                ap_content = f"{ap_content}{cls.get_ap_header(ap_header)}"
                control_total += 1
                line_number: int = 0
                for line_item in inv.payment_line_items:
                    if line_item.total == 0:
                        continue
                    ap_line = APLine.from_invoice_and_line_item(inv, line_item, line_number + 1, bca_distribution)
                    ap_content = f"{ap_content}{cls.get_ap_invoice_line(ap_line)}"
                    line_number += 1
                control_total += line_number
            batch_trailer: str = cls.get_batch_trailer(batch_number, batch_total, control_total=control_total)
            ap_content = f"{ap_content}{batch_trailer}"

            for inv in invoices:
                db.session.add(
                    EjvLinkModel(
                        link_id=inv.id,
                        link_type=EJVLinkType.INVOICE.value,
                        ejv_header_id=ejv_header_model.id,
                        disbursement_status_code=DisbursementStatus.UPLOADED.value,
                    )
                )
                inv.disbursement_status_code = DisbursementStatus.UPLOADED.value
            db.session.flush()

            cls._create_file_and_upload(ap_content)

    @classmethod
    def _create_file_and_upload(cls, ap_content):
        file_path_with_name, trg_file_path, file_name = cls.create_inbox_and_trg_files(ap_content)
        cls.upload(ap_content, file_name, file_path_with_name, trg_file_path)
        db.session.commit()
        # Sleep to prevent collision on file name.
        time.sleep(1)

    @classmethod
    def _get_bca_distribution_string(cls) -> str:
        valid_date = date.today()
        d = (
            db.session.query(DistributionCodeModel)
            .filter(DistributionCodeModel.name == "BC Assessment")
            .filter(DistributionCodeModel.start_date <= valid_date)
            .filter((DistributionCodeModel.end_date.is_(None)) | (DistributionCodeModel.end_date >= valid_date))
            .one_or_none()
        )
        return f"{d.client}{d.responsibility_centre}{d.service_line}{d.stob}{d.project_code}"
