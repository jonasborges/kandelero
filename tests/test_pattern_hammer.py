from decimal import Decimal

import pytest
from kandelero.candlestick import Candlestick
from kandelero.patterns.comparators import is_hammer


@pytest.mark.happy_path
@pytest.mark.parametrize(
    "obj",
    [
        Candlestick(
            open=Decimal("8290.65000"),
            high=Decimal("8346.95000"),
            low=Decimal("8083.85000"),
            close=Decimal("8346.95000"),
        ),
        Candlestick(
            open=Decimal("14757.15000"),
            high=Decimal("14757.15000"),
            low=Decimal("14753.15000"),
            close=Decimal("14755.95000"),
        ),
    ],
    ids=[
        "Nasdaq Daily: 2020-04-13|Bullish",
        "Nasdaq 1 Minute: 2021-07-16 18:38|Bearish",
    ],
)
def test_is_perfect_hammer(obj):
    assert is_hammer(obj), "Not a hammer: wick=%s|body=%s|tail=%s" % (
        obj.wick_proportion,
        obj.body_proportion,
        obj.tail_proportion,
    )
    assert (obj.is_bullish and obj.close == obj.high) or (
        obj.is_bearish and obj.open == obj.high
    )
    assert obj.is_valid_candle


@pytest.mark.happy_path
@pytest.mark.parametrize(
    "obj",
    [
        Candlestick(
            open=Decimal("14893.55000"),
            high=Decimal("14916.05000"),
            low=Decimal("14841.75000"),
            close=Decimal("14910.75000"),
        ),
        Candlestick(
            open=Decimal("13205.00000"),
            high=Decimal("13246.05000"),
            low=Decimal("12959.00000"),
            close=Decimal("13220.90000"),
        ),
        Candlestick(
            open=Decimal("14801.10000"),
            high=Decimal("14802.40000"),
            low=Decimal("14762.10000"),
            close=Decimal("14799.70000"),
        ),
    ],
    ids=[
        "Nasdaq 1h: 2021-07-13 19:00|Bullish",
        "Nasdaq Daily: 2021-05-19|Bullish",
        "Nasdaq 5 Minutes: 2021-07-16 10:00|Bearish",
    ],
)
def test_is_hammer_small_wick(obj):
    assert is_hammer(obj), "Not a hammer: wick=%s|body=%s|tail=%s" % (
        obj.wick_proportion,
        obj.body_proportion,
        obj.tail_proportion,
    )
    assert (obj.is_bullish and obj.close < obj.high) or (
        obj.is_bearish and obj.open < obj.high
    )
    assert obj.is_valid_candle


@pytest.mark.unhappy_path
@pytest.mark.parametrize(
    "obj",
    [
        Candlestick(  # looks like a hammer, close == high, but tail is not long enough
            open=Decimal("10580.07000"),
            high=Decimal("10710.42000"),
            low=Decimal("10524.85000"),
            close=Decimal("10710.42000"),
        ),
        Candlestick(  # looks like a hammer, open == high, but tail is not long enough
            open=Decimal("14899.40000"),
            high=Decimal("14899.40000"),
            low=Decimal("14889.50000"),
            close=Decimal("14894.70000"),
        ),
    ],
    ids=[
        "Nasdaq Daily: 2021-07-29|Bullish",
        "Nasdaq 5 Minutes: 2021-07-15 13:00|Bearish",
    ],
)
def test_is_not_perfect_hammer(obj):
    assert not is_hammer(obj), "Is a hammer: wick=%s|body=%s|tail=%s" % (
        obj.wick_proportion,
        obj.body_proportion,
        obj.tail_proportion,
    )
    assert obj.is_valid_candle


@pytest.mark.unhappy_path
@pytest.mark.parametrize(
    "obj",
    [
        Candlestick(  # looks like a hammer but tail is not long enough
            open=Decimal("12785.50000"),
            high=Decimal("12822.50000"),
            low=Decimal("12733.30000"),
            close=Decimal("12817.65000"),
        ),
        Candlestick(  # looks like a hammer but wick is too long
            open=Decimal("12322.04000"),
            high=Decimal("12466.10000"),
            low=Decimal("12175.66000"),
            close=Decimal("12409.86000"),
        ),
        Candlestick(  # looks like a hammer but tail is not long enough
            open=Decimal("14766.05000"),
            high=Decimal("14766.55000"),
            low=Decimal("14762.15000"),
            close=Decimal("14764.45000"),
        ),
    ],
    ids=[
        "Nasdaq Daily: 2021-01-18|Bullish",
        "Nasdaq Daily: 2020-02-09|Bullish",
        "Nasdaq Daily: 2021-07-16 18:32|Bearish",
    ],
)
def test_is_not_hammer_small_wick(obj):
    assert not is_hammer(obj), "Is a hammer: wick=%s|body=%s|tail=%s" % (
        obj.wick_proportion,
        obj.body_proportion,
        obj.tail_proportion,
    )
    assert obj.is_valid_candle
