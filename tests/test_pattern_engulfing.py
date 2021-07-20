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
                open=Decimal("14638.5000"),
                high=Decimal("14638.5000"),
                low=Decimal("14635.5000"),
                close=Decimal("14636.0000"),
            ),
            Candlestick(  # engulfing candle body only
                open=Decimal("14635.9000"),
                high=Decimal("14641.2000"),
                low=Decimal("14635.9000"),
                close=Decimal("14641.2000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("14638.6000"),
                high=Decimal("14639.0000"),
                low=Decimal("14636.4000"),
                close=Decimal("14636.6000"),
            ),
            Candlestick(  # engulfing full candle length
                open=Decimal("14636.4000"),
                high=Decimal("14644.1000"),
                low=Decimal("14635.5000"),
                close=Decimal("14643.1000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("14478.4500"),
                high=Decimal("14481.8500"),
                low=Decimal("14473.1500"),
                close=Decimal("14473.3500"),
            ),
            Candlestick(  # engulfing full candle length
                open=Decimal("14472.8500"),
                high=Decimal("14483.6500"),
                low=Decimal("14471.3500"),
                close=Decimal("14483.6500"),
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
                open=Decimal("14623.0000"),
                high=Decimal("14624.7000"),
                low=Decimal("14621.6000"),
                close=Decimal("14623.6000"),
            ),
            Candlestick(  # engulfing full candle length
                open=Decimal("14625.3000"),
                high=Decimal("14625.7000"),
                low=Decimal("14613.6000"),
                close=Decimal("14615.2000"),
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
