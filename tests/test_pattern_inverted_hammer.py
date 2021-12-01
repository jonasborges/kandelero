from decimal import Decimal

import pytest

from kandelero.candlestick import Candlestick
from kandelero.patterns.comparators import is_inverted_hammer


@pytest.mark.happy_path
@pytest.mark.parametrize(
    "obj",
    [
        Candlestick(
            open=Decimal("14672.60000"),
            high=Decimal("14675.80000"),
            low=Decimal("14672.40000"),
            close=Decimal("14672.40000"),
        ),
        Candlestick(
            open=Decimal("14682.75000"),
            high=Decimal("14691.75000"),
            low=Decimal("14682.75000"),
            close=Decimal("14683.25000"),
        ),
        Candlestick(  # this one is perfect
            open=Decimal("14867.65000"),
            high=Decimal("14873.35000"),
            low=Decimal("14866.25000"),
            close=Decimal("14866.25000"),
        ),
    ],
    ids=[
        "Nasdaq 1 Minute: 2021-07-16 21:13|Bearish",
        "Nasdaq 1 Minute: 2021-07-16 20:32|Bullish",
        "Nasdaq 1 Minute: 2021-07-16 14:35|Bearish",
    ],
)
def test_is_perfect_inverted_hammer(obj):
    assert is_inverted_hammer(obj), "Not a inverted hammer: wick=%s|body=%s|tail=%s" % (
        obj.wick_proportion,
        obj.body_proportion,
        obj.tail_proportion,
    )
    assert (obj.is_bearish and obj.close == obj.low) or (
        obj.is_bullish and obj.open == obj.low
    )
    assert obj.is_valid_candle


@pytest.mark.happy_path
@pytest.mark.parametrize(
    "obj",
    [
        Candlestick(
            open=Decimal("9995.60000"),
            high=Decimal("10120.90000"),
            low=Decimal("9931.00000"),
            close=Decimal("9935.80000"),
        ),
        Candlestick(
            open=Decimal("9326.30000"),
            high=Decimal("9421.00000"),
            low=Decimal("9289.80000"),
            close=Decimal("9302.20000"),
        ),
        Candlestick(
            open=Decimal("14672.85000"),
            high=Decimal("14684.95000"),
            low=Decimal("14671.15000"),
            close=Decimal("14672.05000"),
        ),
        Candlestick(
            open=Decimal("14681.75000"),
            high=Decimal("14689.55000"),
            low=Decimal("14680.85000"),
            close=Decimal("14683.05000"),
        ),
    ],
    ids=[
        "Nasdaq Daily: 2020-06-19|Bearish",
        "Nasdaq Daily: 2020-05-19|Bearish",
        "Nasdaq 1 Minute: 2021-07-16 20:50|Bearish",
        "Nasdaq 1 Minute: 2021-07-16 20:43|Bullish",
    ],
)
def test_is_inverted_hammer_small_tail(obj):
    assert is_inverted_hammer(obj), "Not a inverted hammer: wick=%s|body=%s|tail=%s" % (
        obj.wick_proportion,
        obj.body_proportion,
        obj.tail_proportion,
    )
    assert obj.close > obj.low
    assert obj.is_valid_candle


@pytest.mark.unhappy_path
@pytest.mark.parametrize(
    "obj",
    [
        Candlestick(  # looks like an inverted hammer, close == low, but wick is not long enough
            open=Decimal("14693.35000"),
            high=Decimal("14695.55000"),
            low=Decimal("14691.15000"),
            close=Decimal("14691.15000"),
        ),
    ],
    ids=[
        "Nasdaq 1 Minute: 2021-07-16 20:41|Bearish",
    ],
)
def test_is_not_perfect_inverted_hammer(obj):
    assert not is_inverted_hammer(
        obj
    ), "Is a inverted hammer: wick=%s|body=%s|tail=%s" % (
        obj.wick_proportion,
        obj.body_proportion,
        obj.tail_proportion,
    )
    assert obj.is_valid_candle


@pytest.mark.unhappy_path
@pytest.mark.parametrize(
    "obj",
    [
        Candlestick(  # looks like an inverted hammer, but wick is not long enough
            open=Decimal("10607.80000"),
            high=Decimal("10704.70000"),
            low=Decimal("10517.57000"),
            close=Decimal("10539.45000"),
        ),
    ],
    ids=[
        "Nasdaq Daily: 2020-07-07|Bearish",
    ],
)
def test_is_not_inverted_hammer_small_tail(obj):
    assert not is_inverted_hammer(
        obj
    ), "Is a inverted hammer: wick=%s|body=%s|tail=%s" % (
        obj.wick_proportion,
        obj.body_proportion,
        obj.tail_proportion,
    )
    assert obj.is_valid_candle
