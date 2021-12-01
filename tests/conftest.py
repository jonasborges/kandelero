import logging
import os

import pytest
from hypothesis import HealthCheck, assume, settings
from hypothesis import strategies as st

from kandelero.calculations import DECIMAL_PLACES, MAX_VALUE, MIN_VALUE

settings.register_profile(
    "ci",
    max_examples=100,
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    ),
)
settings.register_profile(
    "default",
    max_examples=50,
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    ),
)
settings.register_profile(
    "dev",
    max_examples=10,
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    ),
)
hypothesis_profile = os.getenv("HYPOTHESIS_PROFILE", "default")
settings.load_profile(hypothesis_profile)


def pytest_report_header(config, startdir):
    return [f"HYPOTHESIS_PROFILE: {hypothesis_profile}"]
