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
                open=Decimal("14646.2000"),
                high=Decimal("14647.9000"),
                low=Decimal("14646.2000"),
                close=Decimal("14647.0000"),
            ),
            Candlestick(
                open=Decimal("14645.6000"),
                high=Decimal("14646.0000"),
                low=Decimal("14644.5000"),
                close=Decimal("14644.5000"),
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
    (),
    ids=[],
)
def test_is_bullish_kicker(previous, current):
    assert previous.is_bearish
    assert current.is_bullish
    assert is_bullish_kicker(previous, current)
