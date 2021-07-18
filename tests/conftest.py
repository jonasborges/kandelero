import os

import pytest
from hypothesis import HealthCheck, assume, settings
from hypothesis import strategies as st
from kandelero.calculations import DECIMAL_PLACES, MAX_VALUE, MIN_VALUE

settings.register_profile(
    "ci",
    max_examples=2000,
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    ),
)
settings.register_profile(
    "default",
    max_examples=1000,
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    ),
)
settings.register_profile("dev", max_examples=10)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "default"))


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


@pytest.fixture(scope="session")
def generate_values():
    def _gen(data, valid_decimal):
        result = dict(
            high=data.draw(valid_decimal),
            low=data.draw(valid_decimal),
            open=data.draw(valid_decimal),
            close=data.draw(valid_decimal),
        )
        assume(max(result.values()) == result["high"])
        assume(min(result.values()) == result["low"])
        return result

    return _gen
