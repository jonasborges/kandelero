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
                open=Decimal("7637.13000"),
                high=Decimal("7740.85000"),
                low=Decimal("7624.52000"),
                close=Decimal("7708.29000"),
            ),
            Candlestick(
                open=Decimal("7709.68000"),
                high=Decimal("7742.18000"),
                low=Decimal("7644.69000"),
                close=Decimal("7646.62000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("7649.63000"),
                high=Decimal("7756.90000"),
                low=Decimal("7645.78000"),
                close=Decimal("7745.39000"),
            ),
            Candlestick(
                open=Decimal("7745.83000"),
                high=Decimal("7771.83000"),
                low=Decimal("7644.23000"),
                close=Decimal("7693.98000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("9398.45000"),
                high=Decimal("9650.45000"),
                low=Decimal("9316.35000"),
                close=Decimal("9618.01000"),
            ),
            Candlestick(
                open=Decimal("9640.62999"),
                high=Decimal("9752.92000"),
                low=Decimal("9398.79000"),
                close=Decimal("9447.95000"),
            ),
        ],
    ),
    ids=[
        "Nasdaq 1 Day: 2019-08-19 -> 2019-08-20",
        "Nasdaq 1 Day: 2019-08-21 -> 2019-08-22",
        "Nasdaq 1 Week: 2020-03-15 -> 2020-03-22",
    ],
)
def test_is_piercing_line(previous, current):
    assert is_dark_cloud_cover(previous=previous, current=current)

    # Dark Cloud Cover is the opposite of Piercing Line
    # so reversing the chart (going from future to past candles)
    # should result in a Piercing Line
    assert is_piercing_line(previous=current, current=previous)
