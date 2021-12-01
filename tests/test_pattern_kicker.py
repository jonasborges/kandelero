from decimal import Decimal

import pytest

from kandelero import Candlestick
from kandelero.patterns.comparators import is_bearish_kicker, is_bullish_kicker


@pytest.mark.bearish_pattern
@pytest.mark.happy_path
@pytest.mark.parametrize(
    "previous, current",
    (
        [
            Candlestick(
                open=Decimal("14646.20000"),
                high=Decimal("14647.90000"),
                low=Decimal("14646.20000"),
                close=Decimal("14647.00000"),
            ),
            Candlestick(
                open=Decimal("14645.60000"),
                high=Decimal("14646.00000"),
                low=Decimal("14644.50000"),
                close=Decimal("14644.50000"),
            ),
        ],
    ),
    ids=[
        "Nasdaq 1 Minute: 2021-07-19 05:43 -> 05:44",
    ],
)
def test_is_bearish_kicker(previous, current):
    assert previous.is_bullish
    assert current.is_bearish
    assert is_bearish_kicker(previous, current)


@pytest.mark.bullish_pattern
@pytest.mark.happy_path
@pytest.mark.parametrize(
    "previous, current",
    (
        [
            Candlestick(
                open=Decimal("14717.00000"),
                high=Decimal("14717.00000"),
                low=Decimal("14715.00000"),
                close=Decimal("14715.50000"),
            ),
            Candlestick(
                open=Decimal("14720.60000"),
                high=Decimal("14726.00000"),
                low=Decimal("14719.70000"),
                close=Decimal("14725.80000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("29705.24000"),
                high=Decimal("29707.07000"),
                low=Decimal("29690.07000"),
                close=Decimal("29703.17000"),
            ),
            Candlestick(
                open=Decimal("29713.44000"),
                high=Decimal("29751.86000"),
                low=Decimal("29713.44000"),
                close=Decimal("29738.19000"),
            ),
        ],
    ),
    ids=[
        "Nasdaq 15 Minutes: 2021-07-19 21:15 -> 21:30",
        "Bitcoin 11 Minute: 2021-07-20 16:53 -> 16:54",
    ],
)
def test_is_bullish_kicker(previous, current):
    assert previous.is_bearish
    assert current.is_bullish
    assert is_bullish_kicker(previous, current)
