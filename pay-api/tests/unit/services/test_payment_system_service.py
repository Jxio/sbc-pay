# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests to assure the Payment Service.

Test-Suite to ensure that the FeeSchedule Service is working as expected.
"""

import pytest

from pay_api.services.base_payment_system import PaymentSystemService


def test_base_payment_system(session):
    """Assert that the sub-classes are created."""
    paybc_impl = type(
        'PaymentSystemService',
        (PaymentSystemService, object),
        {
            'create_account': lambda self: print('Inside create_account'),
            'create_invoice': lambda self: print('Inside create_invoice'),
            'cancel_invoice': lambda self: print('Inside cancel_invoice'),
            'get_receipt': lambda self: print('Inside get_receipt'),
            'get_payment_system_code': lambda self: print('Inside get_payment_system_code')
        }
    )()
    paybc_impl.create_account()

    with pytest.raises(Exception) as excinfo:
        paybc_impl = type(
            'PaymentSystemService',
            (PaymentSystemService, object),
            {

            }
        )()
        paybc_impl.create_account()
        assert excinfo is not None