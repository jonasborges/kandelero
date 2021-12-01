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
                open=Decimal("14652.80000"),
                high=Decimal("14661.60000"),
                low=Decimal("14652.30000"),
                close=Decimal("14660.70000"),
            ),
            Candlestick(
                open=Decimal("14661.00000"),
                high=Decimal("14661.50000"),
                low=Decimal("14656.70000"),
                close=Decimal("14661.10000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("14506.05000"),
                high=Decimal("14512.55000"),
                low=Decimal("14499.25000"),
                close=Decimal("14512.55000"),
            ),
            Candlestick(
                open=Decimal("14513.55000"),
                high=Decimal("14514.55000"),
                low=Decimal("14501.75000"),
                close=Decimal("14514.05000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("14638.60000"),
                high=Decimal("14641.70000"),
                low=Decimal("14638.60000"),
                close=Decimal("14641.70000"),
            ),
            Candlestick(
                open=Decimal("14641.80000"),
                high=Decimal("14643.30000"),
                low=Decimal("14637.20000"),
                close=Decimal("14643.20000"),
            ),
        ],
    ),
    ids=[
        "Nasdaq 1 Minute: 2021-07-19 08:29 -> 08:30",
        "Nasdaq 1 Minute: 2021-07-19 15:49 -> 15:50",
        "Nasdaq 1 Minute: 2021-07-20 07:33 -> 07:34",
    ],
)
def test_is_hanging_man(previous, current):
    assert is_hanging_man(previous, current)
