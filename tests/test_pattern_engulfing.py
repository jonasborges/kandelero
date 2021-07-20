from decimal import Decimal

import pytest
from kandelero import Candlestick
from kandelero.patterns.comparators import is_bearish_engulfing, is_bullish_engulfing


@pytest.mark.bullish_pattern
@pytest.mark.happy_path
@pytest.mark.parametrize(
    "shortest, longest",
    (
        [
            Candlestick(
                open=Decimal("14638.50000"),
                high=Decimal("14638.50000"),
                low=Decimal("14635.50000"),
                close=Decimal("14636.00000"),
            ),
            Candlestick(  # engulfing candle body only
                open=Decimal("14635.90000"),
                high=Decimal("14641.20000"),
                low=Decimal("14635.90000"),
                close=Decimal("14641.20000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("14638.60000"),
                high=Decimal("14639.00000"),
                low=Decimal("14636.40000"),
                close=Decimal("14636.60000"),
            ),
            Candlestick(  # engulfing full candle length
                open=Decimal("14636.40000"),
                high=Decimal("14644.10000"),
                low=Decimal("14635.50000"),
                close=Decimal("14643.10000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("14478.45000"),
                high=Decimal("14481.85000"),
                low=Decimal("14473.15000"),
                close=Decimal("14473.35000"),
            ),
            Candlestick(  # engulfing full candle length
                open=Decimal("14472.85000"),
                high=Decimal("14483.65000"),
                low=Decimal("14471.35000"),
                close=Decimal("14483.65000"),
            ),
        ],
    ),
    ids=[
        "Nasdaq 1 Minute: 2021-07-19 05:57 -> 05:58",
        "Nasdaq 1 Minute: 2021-07-19 08:39 -> 08:40",
        "Nasdaq 1 Minute: 2021-07-19 18:05 -> 18:06",
    ],
)
def test_is_bullish_engulfing(shortest, longest):
    assert shortest.is_bearish
    assert longest.is_bullish
    assert is_bullish_engulfing(shortest, longest)


@pytest.mark.bullish_pattern
@pytest.mark.happy_path
@pytest.mark.parametrize(
    "shortest, longest",
    (
        [
            Candlestick(
                open=Decimal("14623.00000"),
                high=Decimal("14624.70000"),
                low=Decimal("14621.60000"),
                close=Decimal("14623.60000"),
            ),
            Candlestick(  # engulfing full candle length
                open=Decimal("14625.30000"),
                high=Decimal("14625.70000"),
                low=Decimal("14613.60000"),
                close=Decimal("14615.20000"),
            ),
        ],
    ),
    ids=[
        "Nasdaq 1 Minute: 2021-07-19 11:59 -> 12:00",
    ],
)
def test_is_bearish_engulfing(shortest, longest):
    assert shortest.is_bullish
    assert longest.is_bearish
    assert is_bearish_engulfing(shortest, longest)
