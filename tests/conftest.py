from decimal import Decimal

import pytest
from hypothesis import strategies as st


@pytest.fixture(scope="session")
def decimal_min_value():
    return Decimal("0.00000000000000000001")


@pytest.fixture(scope="session")
def decimal_max_value():
    return Decimal("900000000000000000000")


@pytest.fixture(scope="session")
def decimal_max_places():
    return 20


@pytest.fixture(scope="session")
def valid_decimal(decimal_min_value, decimal_max_value, decimal_max_places):
    return st.decimals(
        min_value=decimal_min_value,
        max_value=decimal_max_value,
        allow_nan=False,
        allow_infinity=False,
        places=decimal_max_places,
    )
