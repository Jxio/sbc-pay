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
"""Error definitions."""
from enum import Enum
from http import HTTPStatus


class Error(Enum):
    """Error Codes."""

    INVALID_CORP_OR_FILING_TYPE = "INVALID_CORP_OR_FILING_TYPE", HTTPStatus.BAD_REQUEST

    INVALID_PAYMENT_ID = "INVALID_PAYMENT_ID", HTTPStatus.BAD_REQUEST

    INVALID_PAYMENT_METHOD = "INVALID_PAYMENT_METHOD", HTTPStatus.BAD_REQUEST

    INVALID_TRANSACTION = "INVALID_TRANSACTION", HTTPStatus.BAD_REQUEST

    INVALID_REFUND = "INVALID_REFUND", HTTPStatus.BAD_REQUEST

    INVALID_REDIRECT_URI = "INVALID_REDIRECT_URI", HTTPStatus.BAD_REQUEST

    INVALID_TRANSACTION_ID = "INVALID_TRANSACTION_ID", HTTPStatus.BAD_REQUEST

    INVALID_ACCOUNT_ID = "INVALID_ACCOUNT_ID", HTTPStatus.BAD_REQUEST

    COMPLETED_PAYMENT = "COMPLETED_PAYMENT", HTTPStatus.BAD_REQUEST

    ACCOUNT_IN_PAD_CONFIRMATION_PERIOD = (
        "ACCOUNT_IN_PAD_CONFIRMATION_PERIOD",
        HTTPStatus.BAD_REQUEST,
    )

    PAD_CURRENTLY_NSF = "PAD_CURRENTLY_NSF", HTTPStatus.BAD_REQUEST

    CANCELLED_PAYMENT = "CANCELLED_PAYMENT", HTTPStatus.BAD_REQUEST

    INVALID_INVOICE_ID = "INVALID_INVOICE_ID", HTTPStatus.BAD_REQUEST

    FEE_OVERRIDE_NOT_ALLOWED = "FEE_OVERRIDE_NOT_ALLOWED", HTTPStatus.UNAUTHORIZED

    INCOMPLETE_ACCOUNT_SETUP = "INCOMPLETE_ACCOUNT_SETUP", HTTPStatus.UNAUTHORIZED

    BCOL_UNAVAILABLE = "BCOL_UNAVAILABLE", HTTPStatus.BAD_REQUEST
    BCOL_ACCOUNT_CLOSED = "BCOL_ACCOUNT_CLOSED", HTTPStatus.BAD_REQUEST
    BCOL_USER_REVOKED = "BCOL_USER_REVOKED", HTTPStatus.BAD_REQUEST
    BCOL_ACCOUNT_REVOKED = "BCOL_ACCOUNT_REVOKED", HTTPStatus.BAD_REQUEST
    BCOL_ACCOUNT_INSUFFICIENT_FUNDS = (
        "BCOL_ACCOUNT_INSUFFICIENT_FUNDS",
        HTTPStatus.BAD_REQUEST,
    )
    BCOL_INVALID_ACCOUNT = "BCOL_INVALID_ACCOUNT", HTTPStatus.BAD_REQUEST
    BCOL_ERROR = "BCOL_ERROR", HTTPStatus.BAD_REQUEST

    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE", HTTPStatus.SERVICE_UNAVAILABLE
    INVALID_REQUEST = "INVALID_REQUEST", HTTPStatus.BAD_REQUEST, "Invalid Request"
    PATCH_INVALID_ACTION = "PATCH_INVALID_ACTION", HTTPStatus.BAD_REQUEST

    PAYMENT_SEARCH_TOO_MANY_RECORDS = (
        "PAYMENT_SEARCH_TOO_MANY_RECORDS",
        HTTPStatus.BAD_REQUEST,
    )

    DIRECT_PAY_INVALID_RESPONSE = "DIRECT_PAY_INVALID_RESPONSE", HTTPStatus.BAD_REQUEST

    ACCOUNT_EXISTS = "ACCOUNT_EXISTS", HTTPStatus.BAD_REQUEST

    OUTSTANDING_CREDIT = "OUTSTANDING_CREDIT", HTTPStatus.BAD_REQUEST
    TRANSACTIONS_IN_PROGRESS = "TRANSACTIONS_IN_PROGRESS", HTTPStatus.BAD_REQUEST
    FROZEN_ACCOUNT = "FROZEN_ACCOUNT", HTTPStatus.BAD_REQUEST

    CFS_INVOICES_MISMATCH = "CFS_INVOICES_MISMATCH", HTTPStatus.BAD_REQUEST

    EFT_PARTIAL_REFUND = "EFT_PARTIAL_REFUND", HTTPStatus.BAD_REQUEST
    EFT_CREDIT_AMOUNT_UNEXPECTED = (
        "EFT_CREDIT_AMOUNT_UNEXPECTED",
        HTTPStatus.BAD_REQUEST,
    )
    EFT_INSUFFICIENT_CREDITS = "EFT_INSUFFICIENT_CREDITS", HTTPStatus.BAD_REQUEST
    EFT_PAYMENT_ACTION_ACCOUNT_ID_REQUIRED = (
        "EFT_PAYMENT_ACTION_ACCOUNT_ID_REQUIRED",
        HTTPStatus.BAD_REQUEST,
    )
    EFT_PAYMENT_ACTION_STATEMENT_ID_REQUIRED = (
        "EFT_PAYMENT_ACTION_STATEMENT_ID_REQUIRED",
        HTTPStatus.BAD_REQUEST,
    )
    EFT_PAYMENT_ACTION_UNPAID_STATEMENT = (
        "EFT_PAYMENT_ACTION_UNPAID_STATEMENT",
        HTTPStatus.BAD_REQUEST,
    )
    EFT_PAYMENT_ACTION_REVERSAL_EXCEEDS_SIXTY_DAYS = (
        "EFT_PAYMENT_ACTION_REVERSAL_EXCEEDS_SIXTY_DAYS",
        HTTPStatus.BAD_REQUEST,
    )
    EFT_PAYMENT_ACTION_CREDIT_LINK_STATUS_INVALID = (
        "EFT_PAYMENT_ACTION_CREDIT_LINK_STATUS_INVALID",
        HTTPStatus.BAD_REQUEST,
    )
    EFT_PAYMENT_INVOICE_REVERSE_UNEXPECTED_STATUS = (
        "EFT_PAYMENT_INVOICE_REVERSE_UNEXPECTED_STATUS",
        HTTPStatus.BAD_REQUEST,
    )
    EFT_PAYMENT_ACTION_UNSUPPORTED = (
        "EFT_PAYMENT_ACTION_UNSUPPORTED",
        HTTPStatus.BAD_REQUEST,
    )
    EFT_SHORT_NAME_EXISTS = "EFT_SHORT_NAME_EXISTS", HTTPStatus.BAD_REQUEST
    EFT_SHORT_NAME_ACCOUNT_ID_REQUIRED = (
        "EFT_SHORT_NAME_ACCOUNT_ID_REQUIRED",
        HTTPStatus.BAD_REQUEST,
    )
    EFT_SHORT_NAME_ALREADY_MAPPED = (
        "EFT_SHORT_NAME_ALREADY_MAPPED",
        HTTPStatus.BAD_REQUEST,
    )
    EFT_SHORT_NAME_LINK_INVALID_STATUS = (
        "EFT_SHORT_NAME_LINK_INVALID_STATUS",
        HTTPStatus.BAD_REQUEST,
    )
    EFT_SHORT_NAME_NOT_LINKED = "EFT_SHORT_NAME_NOT_LINKED", HTTPStatus.BAD_REQUEST
    EFT_SHORT_NAME_OUTSTANDING_BALANCE = (
        "EFT_SHORT_NAME_OUTSTANDING_BALANCE",
        HTTPStatus.BAD_REQUEST,
    )
    EFT_INVOICES_OVERDUE = "EFT_INVOICES_OVERDUE", HTTPStatus.BAD_REQUEST
    EFT_REFUND_SAME_USER_APPROVAL_FORBIDDEN = "EFT_REFUND_SAME_USER_APPROVAL_FORBIDDEN", HTTPStatus.FORBIDDEN

    FAS_INVALID_PAYMENT_METHOD = "FAS_INVALID_PAYMENT_METHOD", HTTPStatus.BAD_REQUEST
    FAS_INVALID_ROUTING_SLIP_NUMBER = (
        "FAS_INVALID_ROUTING_SLIP_NUMBER",
        HTTPStatus.BAD_REQUEST,
    )
    FAS_INVALID_ROUTING_SLIP_DIGITS = (
        "FAS_INVALID_ROUTING_SLIP_DIGITS",
        HTTPStatus.BAD_REQUEST,
    )
    FAS_INVALID_RS_STATUS_CHANGE = (
        "FAS_INVALID_RS_STATUS_CHANGE",
        HTTPStatus.BAD_REQUEST,
    )
    REFUND_PAYMENT_LINE_ITEM_INVALID = "REFUND_PAYMENT_LINE_ITEM_INVALID", HTTPStatus.BAD_REQUEST
    REFUND_AMOUNT_INVALID = "REFUND_AMOUNT_INVALID", HTTPStatus.BAD_REQUEST
    PARTIAL_REFUND_DISBURSEMENTS_UNSUPPORTED = "PARTIAL_REFUND_DISBURSEMENTS_UNSUPPORTED", HTTPStatus.BAD_REQUEST

    ROUTING_SLIP_REFUND = "ROUTING_SLIP_REFUND", HTTPStatus.BAD_REQUEST
    NO_FEE_REFUND = "NO_FEE_REFUND", HTTPStatus.BAD_REQUEST
    INVALID_CONSOLIDATED_REFUND = "INVALID_CONSOLIDATED_REFUND", HTTPStatus.BAD_REQUEST
    REFUND_ALREADY_FINALIZED = "REFUND_ALREADY_FINALIZED", HTTPStatus.BAD_REQUEST

    RS_ALREADY_A_PARENT = "RS_ALREADY_A_PARENT", HTTPStatus.BAD_REQUEST
    RS_ALREADY_LINKED = "RS_ALREADY_LINKED", HTTPStatus.BAD_REQUEST
    RS_PARENT_ALREADY_LINKED = "RS_PARENT_ALREADY_LINKED", HTTPStatus.BAD_REQUEST
    RS_CANT_LINK_TO_SAME = "RS_CANT_LINK_TO_SAME", HTTPStatus.BAD_REQUEST
    RS_CHILD_HAS_TRANSACTIONS = "RS_CHILD_HAS_TRANSACTIONS", HTTPStatus.BAD_REQUEST
    RS_IN_INVALID_STATUS = "RS_IN_INVALID_STATUS", HTTPStatus.BAD_REQUEST
    RS_CANT_LINK_NSF = "RS_CANT_LINK_NSF", HTTPStatus.BAD_REQUEST
    RS_HAS_TRANSACTIONS = "RS_HAS_TRANSACTIONS", HTTPStatus.BAD_REQUEST
    RS_INSUFFICIENT_FUNDS = "RS_INSUFFICIENT_FUNDS", HTTPStatus.BAD_REQUEST
    RS_DOESNT_EXIST = "RS_DOESNT_EXIST", HTTPStatus.BAD_REQUEST
    RS_NOT_ACTIVE = "RS_NOT_ACTIVE", HTTPStatus.BAD_REQUEST

    def __new__(cls, code, status, message=None, details=None):
        """Attributes for the enum."""
        obj = object.__new__(cls)
        obj.code = code
        obj.status = status
        obj.message = message
        obj.details = details if details else message
        return obj


def get_bcol_error(error_code: int):
    """Return error code corresponding to BC Online error code."""
    error: Error = Error.BCOL_ERROR
    if error_code == 7:
        error = Error.BCOL_UNAVAILABLE
    elif error_code == 20:
        error = Error.BCOL_ACCOUNT_CLOSED
    elif error_code == 21:
        error = Error.BCOL_USER_REVOKED
    elif error_code == 48:
        error = Error.BCOL_ACCOUNT_REVOKED
    elif error_code == 61:
        error = Error.BCOL_ACCOUNT_INSUFFICIENT_FUNDS
    elif error_code == 5:
        error = Error.BCOL_INVALID_ACCOUNT
    return error
