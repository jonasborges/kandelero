from decimal import Decimal

import pytest
from kandelero import Candlestick
from kandelero.patterns.comparators import is_shooting_star


@pytest.mark.bearish_pattern
@pytest.mark.happy_path
@pytest.mark.parametrize(
    "previous, current",
    (
        [
            Candlestick(
                open=Decimal("14610.6000"),
                high=Decimal("14613.6000"),
                low=Decimal("14610.1000"),
                close=Decimal("14613.2000"),
            ),
            Candlestick(
                open=Decimal("14613.3000"),
                high=Decimal("14615.3000"),
                low=Decimal("14613.3000"),
                close=Decimal("14613.3000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("14616.3000"),
                high=Decimal("14619.8000"),
                low=Decimal("14615.8000"),
                close=Decimal("14618.3000"),
            ),
            Candlestick(
                open=Decimal("14618.5000"),
                high=Decimal("14621.9000"),
                low=Decimal("14618.5000"),
                close=Decimal("14619.3000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("14763.2500"),
                high=Decimal("14766.9500"),
                low=Decimal("14762.4500"),
                close=Decimal("14766.9500"),
            ),
            Candlestick(
                open=Decimal("14767.1500"),
                high=Decimal("14769.5500"),
                low=Decimal("14767.1500"),
                close=Decimal("14767.8500"),
            ),
        ],
    ),
    ids=[
        "Nasdaq 1 Minute: 2021-07-20 06:23 -> 05:24",
        "Nasdaq 1 Minute: 2021-07-20 12:38 -> 12:39",
        "Nasdaq 1 Minute: 2021-07-20 19:28 -> 19:29",
    ],
)
def test_is_shooting_star(previous, current):
    assert is_shooting_star(previous, current)
