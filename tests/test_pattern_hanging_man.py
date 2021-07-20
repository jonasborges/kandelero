from decimal import Decimal

import pytest
from kandelero import Candlestick
from kandelero.patterns.comparators import is_hanging_man


@pytest.mark.bearish_pattern
@pytest.mark.happy_path
@pytest.mark.parametrize(
    "previous, current",
    (
        [
            Candlestick(
                open=Decimal("14652.8000"),
                high=Decimal("14661.6000"),
                low=Decimal("14652.3000"),
                close=Decimal("14660.7000"),
            ),
            Candlestick(
                open=Decimal("14661.0000"),
                high=Decimal("14661.5000"),
                low=Decimal("14656.7000"),
                close=Decimal("14661.1000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("14506.0500"),
                high=Decimal("14512.5500"),
                low=Decimal("14499.2500"),
                close=Decimal("14512.5500"),
            ),
            Candlestick(
                open=Decimal("14513.5500"),
                high=Decimal("14514.5500"),
                low=Decimal("14501.7500"),
                close=Decimal("14514.0500"),
            ),
        ],
    ),
    ids=[
        "Nasdaq 1 Minute: 2021-07-19 08:29 -> 08:30",
        "Nasdaq 1 Minute: 2021-07-19 15:49 -> 15:50",
    ],
)
def test_is_hanging_man(previous, current):
    assert is_hanging_man(previous, current)
