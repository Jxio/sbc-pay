# Copyright © 2024 Province of British Columbia
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
"""Enum definitions."""
from enum import Enum


class AuthHeaderType(Enum):
    """Authorization header types."""

    BASIC = 'Basic {}'
    BEARER = 'Bearer {}'


class ContentType(Enum):
    """Http Content Types."""

    JSON = 'application/json'
    FORM_URL_ENCODED = 'application/x-www-form-urlencoded'
    CSV = 'text/csv'
    PDF = 'application/pdf'


class PaymentStatus(Enum):
    """Payment status codes."""

    CREATED = 'CREATED'
    COMPLETED = 'COMPLETED'
    DELETED = 'DELETED'
    REFUNDED = 'REFUNDED'
    FAILED = 'FAILED'


class InvoiceStatus(Enum):
    """Invoice status codes."""

    CREATED = 'CREATED'
    APPROVED = 'APPROVED'
    PAID = 'PAID'
    DELETED = 'DELETED'
    UPDATE_REVENUE_ACCOUNT = 'GL_UPDATED'
    UPDATE_REVENUE_ACCOUNT_REFUND = 'GL_UPDATED_REFUND'
    DELETE_ACCEPTED = 'DELETE_ACCEPTED'
    SETTLEMENT_SCHEDULED = 'SETTLEMENT_SCHED'
    REFUND_REQUESTED = 'REFUND_REQUESTED'
    PARTIAL = 'PARTIAL_PAID'
    REFUNDED = 'REFUNDED'
    CANCELLED = 'CANCELLED'
    CREDITED = 'CREDITED'
    OVERDUE = 'OVERDUE'


class TransactionStatus(Enum):
    """Transaction status codes."""

    CREATED = 'CREATED'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    CANCELLED = 'CANCELLED'
    EVENT_FAILED = 'EVENT_FAILED'


class LineItemStatus(Enum):
    """Line Item status codes."""

    ACTIVE = 'ACTIVE'
    CANCELLED = 'CANCELLED'


class InvoiceReferenceStatus(Enum):
    """Line Invoice Reference status codes."""

    ACTIVE = 'ACTIVE'
    COMPLETED = 'COMPLETED'
    CANCELLED = 'CANCELLED'


class PaymentSystem(Enum):
    """Payment System Codes."""

    PAYBC = 'PAYBC'
    BCOL = 'BCOL'
    INTERNAL = 'INTERNAL'
    CGI = 'CGI'
    FAS = 'FAS'


class PaymentMethod(Enum):
    """Payment Method Codes."""

    CC = 'CC'
    DRAWDOWN = 'DRAWDOWN'
    INTERNAL = 'INTERNAL'
    DIRECT_PAY = 'DIRECT_PAY'
    EFT = 'EFT'
    WIRE = 'WIRE'
    ONLINE_BANKING = 'ONLINE_BANKING'
    PAD = 'PAD'
    EJV = 'EJV'
    CASH = 'CASH'
    CHEQUE = 'CHEQUE'


class Role(Enum):
    """User Role."""

    STAFF = 'staff'
    VIEWER = 'view'
    EDITOR = 'edit'
    SYSTEM = 'system'
    CREATE_SANDBOX_ACCOUNT = 'create_sandbox_account'
    MANAGE_GL_CODES = 'manage_gl_codes'
    PUBLIC_USER = 'public_user'
    EXCLUDE_SERVICE_FEES = 'exclude_service_fees'
    CREATE_CREDITS = 'create_credits'
    MANAGE_ACCOUNTS = 'manage_accounts'
    FAS_USER = 'fas_user'
    FAS_EDIT = 'fas_edit'
    FAS_REPORTS = 'fas_reports'
    FAS_SEARCH = 'fas_search'
    FAS_REFUND = 'fas_refund'
    FAS_VIEW = 'fas_view'
    FAS_CREATE = 'fas_create'
    FAS_LINK = 'fas_link'
    FAS_REFUND_APPROVER = 'fas_refund_approver'
    FAS_VOID = 'fas_void'
    FAS_CORRECTION = 'fas_correction'
    SANDBOX = 'sandbox'
    VIEW_ALL_TRANSACTIONS = 'view_all_transactions'
    MANAGE_EFT = 'manage_eft'


class Code(Enum):
    """Code value keys."""

    ERROR = 'errors'
    INVOICE_STATUS = 'invoice_statuses'
    CORP_TYPE = 'corp_types'
    FEE_CODE = 'fee_codes'
    ROUTING_SLIP_STATUS = 'routing_slip_statuses'


class AccountType(Enum):
    """Account types."""

    BASIC = 'BASIC'
    PREMIUM = 'PREMIUM'
    STAFF = 'STAFF'
    SBC_STAFF = 'SBC_STAFF'


class StatementFrequency(Enum):
    """Statement frequency."""

    DAILY = 'DAILY'
    WEEKLY = 'WEEKLY'
    MONTHLY = 'MONTHLY'

    @staticmethod
    def default_frequency():
        """Return the default frequency for statements."""
        return StatementFrequency.WEEKLY


class NotificationStatus(Enum):
    """Mail notification Status."""

    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    SUCCESS = 'SUCCESS'
    SKIP = 'SKIP'
    FAILED = 'FAILED'


class CfsAccountStatus(Enum):
    """Cfs Account Status."""

    PENDING = 'PENDING'
    PENDING_PAD_ACTIVATION = 'PENDING_PAD_ACTIVATION'
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    FREEZE = 'FREEZE'


class CorpType(Enum):
    """Corp Type."""

    BTR = 'BTR'
    ESRA = 'ESRA'
    MHR = 'MHR'
    NRO = 'NRO'
    PPR = 'PPR'
    VS = 'VS'
    CSO = 'CSO'
    RPT = 'RPT'


class DisbursementStatus(Enum):
    """Disbursement status codes."""

    UPLOADED = 'UPLOADED'
    ACKNOWLEDGED = 'ACKNOWLEDGED'
    ERRORED = 'ERRORED'
    COMPLETED = 'COMPLETED'
    REVERSED = 'REVERSED'


class Product(Enum):
    """Product."""

    BUSINESS = 'BUSINESS'
    NRO = 'NRO'


class RoutingSlipStatus(Enum):
    """Routing slip statuses."""

    ACTIVE = 'ACTIVE'
    COMPLETE = 'COMPLETE'
    NSF = 'NSF'
    LAST = 'LAST'
    LINKED = 'LINKED'
    REFUND_REQUESTED = 'REFUND_REQUESTED'
    REFUND_AUTHORIZED = 'REFUND_AUTHORIZED'
    REFUND_UPLOADED = 'REFUND_UPLOADED'
    REFUND_REJECTED = 'REFUND_REJECTED'
    REFUND_COMPLETED = 'REFUND_COMPLETED'
    WRITE_OFF_REQUESTED = 'WRITE_OFF_REQUESTED'
    WRITE_OFF_AUTHORIZED = 'WRITE_OFF_AUTHORIZED'
    WRITE_OFF_COMPLETED = 'WRITE_OFF_COMPLETED'
    HOLD = 'HOLD'  # new
    VOID = 'VOID'
    CORRECTION = 'CORRECTION'


class RoutingSlipCustomStatus(Enum):
    """Routing slip  custom statuses."""

    CANCEL_REFUND_REQUEST = 'CANCEL_REFUND_REQUEST', RoutingSlipStatus.ACTIVE.value
    CANCEL_WRITE_OFF_REQUEST = 'CANCEL_WRITE_OFF_REQUEST', RoutingSlipStatus.ACTIVE.value

    def __new__(cls, custom_status, original_status):
        """Attributes for the enum."""
        obj = object.__new__(cls)
        obj.custom_status = custom_status
        obj.original_status = original_status
        return obj

    @classmethod
    def from_key(cls, key):
        """Return instance from key of the enum."""
        try:
            return RoutingSlipCustomStatus[key]
        except KeyError:
            return None


class EjvFileType(Enum):
    """File types."""

    PAYMENT = 'PAYMENT'
    DISBURSEMENT = 'DISBURSEMENT'
    REFUND = 'REFUND'
    NON_GOV_DISBURSEMENT = 'NON_GOV_DISBURSEMENT'
    TRANSFER = 'TRANSFER'


class PatchActions(Enum):
    """Patch Actions."""

    UPDATE_STATUS = 'updateStatus'

    @classmethod
    def from_value(cls, value):
        """Return instance from value of the enum."""
        return PatchActions(value) if value in cls._value2member_map_ else None  # pylint: disable=no-member


class RefundsPartialType(Enum):
    """Refund partial types."""

    BASE_FEES = 'BASE_FEES'
    FUTURE_EFFECTIVE_FEES = 'FUTURE_EFFECTIVE_FEES'
    PRIORITY_FEES = 'PRIORITY_FEES'
    SERVICE_FEES = 'SERVICE_FEES'


class ReverseOperation(Enum):
    """Reverse Routing Slip Operation, determines comment."""

    NSF = 'NSF'
    LINK = 'LINK'
    VOID = 'VOID'
    CORRECTION = 'CORRECTION'


class CfsReceiptStatus(Enum):
    """Routing Slip Receipt Status."""

    REV = 'REV'


class EFTCreditInvoiceStatus(Enum):
    """EFT Credit Invoice Link Status."""

    COMPLETED = 'COMPLETED'
    PENDING = 'PENDING'
    PENDING_REFUND = 'PENDING_REFUND'
    REFUNDED = 'REFUNDED'


class EFTProcessStatus(Enum):
    """EFT Process Status."""

    COMPLETED = 'COMPLETED'
    IN_PROGRESS = 'INPROGRESS'
    FAILED = 'FAILED'
    PARTIAL = 'PARTIAL'


class EFTFileLineType(Enum):
    """EFT File (TDI17) Line types."""

    HEADER = 'HEADER'
    TRANSACTION = 'TRANSACTION'
    TRAILER = 'TRAILER'


class EFTGlTransferType(Enum):
    """EFT GL Transfer types for job processing."""

    PAYMENT = 'PAYMENT'
    REVERSAL = 'REVERSAL'
    TRANSFER = 'TRANSFER'


class EFTShortnameStatus(Enum):
    """EFT Short name statuses."""

    INACTIVE = 'INACTIVE'
    LINKED = 'LINKED'
    UNLINKED = 'UNLINKED'
    PENDING = 'PENDING'


class PaymentDetailsGlStatus(Enum):
    """Payment details GL status."""

    PAID = 'PAID'
    INPRG = 'INPRG'
    RJCT = 'RJCT'  # Should have refundglerrormessage
    CMPLT = 'CMPLT'


class QueueSources(Enum):
    """Queue sources for PAY."""

    PAY_API = 'pay-api'
    PAY_JOBS = 'pay-jobs'
    PAY_QUEUE = 'pay-queue'
    FTP_POLLER = 'ftp-poller'


class EJVLinkType(Enum):
    """EJV link types for ejv_link table."""

    INVOICE = 'invoice'
    REFUND = 'refund'


class StatementTemplate(Enum):
    """Statement report templates."""

    EFT_STATEMENT = 'eft_statement'
    STATEMENT_REPORT = 'statement_report'
