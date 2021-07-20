from decimal import Decimal

import pytest
from kandelero import Candlestick
from kandelero.patterns.comparators import is_shooting_star


@pytest.mark.bearish_pattern
@pytest.mark.happy_path
@pytest.mark.parametrize(
    "previous, current",
    (),
    ids=[],
)
def test_is_shooting_star(previous, current):
    assert is_shooting_star(previous, current)
