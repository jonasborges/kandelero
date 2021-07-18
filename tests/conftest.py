import pytest
from hypothesis import assume
from hypothesis import strategies as st
from kandelero.calculations import DECIMAL_PLACES, MAX_VALUE, MIN_VALUE


@pytest.fixture(scope="session")
def decimal_min_value():
    return MIN_VALUE


@pytest.fixture(scope="session")
def decimal_max_value():
    return MAX_VALUE


@pytest.fixture(scope="session")
def decimal_max_places():
    return DECIMAL_PLACES


@pytest.fixture(scope="session")
def valid_decimal(decimal_min_value, decimal_max_value, decimal_max_places):
    return st.decimals(
        min_value=decimal_min_value,
        max_value=decimal_max_value,
        allow_nan=False,
        allow_infinity=False,
        places=decimal_max_places,
    )
