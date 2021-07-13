from decimal import Decimal

import pytest
from hypothesis import strategies as st
from kandelero import Candlestick


@pytest.fixture(scope="session")
def hammer():
    """Nasdaq Daily: 2020-04-13"""
    return Candlestick(
        open=Decimal("8290.65"),
        high=Decimal("8346.95"),
        low=Decimal("8083.85"),
        close=Decimal("8346.95"),
    )


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
def valid_decimal():
    return st.decimals(
        allow_nan=False,
        allow_infinity=False,
    )


@pytest.fixture(scope="session")
def valid_decimal_within_range(
    decimal_min_value, decimal_max_value, decimal_max_places
):
    return st.decimals(
        min_value=decimal_min_value,
        max_value=decimal_max_value,
        allow_nan=False,
        allow_infinity=False,
        places=decimal_max_places,
    )
