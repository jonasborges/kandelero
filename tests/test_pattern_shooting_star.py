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
                open=Decimal("14610.60000"),
                high=Decimal("14613.60000"),
                low=Decimal("14610.10000"),
                close=Decimal("14613.20000"),
            ),
            Candlestick(
                open=Decimal("14613.30000"),
                high=Decimal("14615.30000"),
                low=Decimal("14613.30000"),
                close=Decimal("14613.30000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("14616.30000"),
                high=Decimal("14619.80000"),
                low=Decimal("14615.80000"),
                close=Decimal("14618.30000"),
            ),
            Candlestick(
                open=Decimal("14618.50000"),
                high=Decimal("14621.90000"),
                low=Decimal("14618.50000"),
                close=Decimal("14619.30000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("14763.25000"),
                high=Decimal("14766.95000"),
                low=Decimal("14762.45000"),
                close=Decimal("14766.95000"),
            ),
            Candlestick(
                open=Decimal("14767.15000"),
                high=Decimal("14769.55000"),
                low=Decimal("14767.15000"),
                close=Decimal("14767.85000"),
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
