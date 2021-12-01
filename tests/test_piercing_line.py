from decimal import Decimal

import pytest

from kandelero import Candlestick
from kandelero.patterns.comparators import is_dark_cloud_cover, is_piercing_line


@pytest.mark.bullish_pattern
@pytest.mark.happy_path
@pytest.mark.parametrize(
    "previous, current",
    (
        [
            Candlestick(
                open=Decimal("14180.20000"),
                high=Decimal("14209.20000"),
                low=Decimal("14018.95000"),
                close=Decimal("14045.80000"),
            ),
            Candlestick(
                open=Decimal("14034.90000"),
                high=Decimal("14149.05000"),
                low=Decimal("13968.65000"),
                close=Decimal("14143.20000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("7533.90000"),
                high=Decimal("7546.70000"),
                low=Decimal("7429.33000"),
                close=Decimal("7434.68000"),
            ),
            Candlestick(
                open=Decimal("7434.53000"),
                high=Decimal("7533.65000"),
                low=Decimal("7393.88000"),
                close=Decimal("7497.83000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("7568.93000"),
                high=Decimal("7605.18000"),
                low=Decimal("7518.90000"),
                close=Decimal("7521.25000"),
            ),
            Candlestick(
                open=Decimal("7497.78000"),
                high=Decimal("7563.88000"),
                low=Decimal("7445.53000"),
                close=Decimal("7561.43000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("6890.95000"),
                high=Decimal("6984.43000"),
                low=Decimal("6574.50000"),
                close=Decimal("6717.30000"),
            ),
            Candlestick(
                open=Decimal("6711.58000"),
                high=Decimal("6842.10000"),
                low=Decimal("6655.08000"),
                close=Decimal("6835.95000"),
            ),
        ],
    ),
    ids=[
        "Nasdaq 1 Day: 2021-06-18 -> 2021-06-19",
        "Nasdaq 1 Day: 2018-09-17 -> 2018-09-18",
        "Nasdaq 1 Day: 2018-09-21 -> 2018-09-24",
        "Nasdaq 1 Day: 2018-10-29 -> 2018-10-30",
    ],
)
def test_is_piercing_line(previous, current):
    assert is_piercing_line(previous=previous, current=current)

    # Piercing Line is the opposite of Dark Cloud Cover
    # so reversing the chart (going from future to past candles)
    # should result in a Dark Cloud Cover
    assert is_dark_cloud_cover(previous=current, current=previous)
