from decimal import Decimal

import pytest
from kandelero.candlestick import Candlestick
from kandelero.patterns.comparators import is_hammer


@pytest.mark.happy_path
@pytest.mark.parametrize(
    "obj",
    [
        Candlestick(
            open=Decimal("8290.65"),
            high=Decimal("8346.95"),
            low=Decimal("8083.85"),
            close=Decimal("8346.95"),
        ),
        Candlestick(
            open=Decimal("14757.15"),
            high=Decimal("14757.15"),
            low=Decimal("14753.15"),
            close=Decimal("14755.95"),
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
            open=Decimal("14893.55"),
            high=Decimal("14916.05"),
            low=Decimal("14841.75"),
            close=Decimal("14910.75"),
        ),
        Candlestick(
            open=Decimal("13205.00"),
            high=Decimal("13246.05"),
            low=Decimal("12959.00"),
            close=Decimal("13220.90"),
        ),
        Candlestick(
            open=Decimal("14801.10"),
            high=Decimal("14802.40"),
            low=Decimal("14762.10"),
            close=Decimal("14799.70"),
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
            open=Decimal("10580.07"),
            high=Decimal("10710.42"),
            low=Decimal("10524.85"),
            close=Decimal("10710.42"),
        ),
        Candlestick(  # looks like a hammer, open == high, but tail is not long enough
            open=Decimal("14899.40"),
            high=Decimal("14899.40"),
            low=Decimal("14889.50"),
            close=Decimal("14894.70"),
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
            open=Decimal("12785.50"),
            high=Decimal("12822.50"),
            low=Decimal("12733.30"),
            close=Decimal("12817.65"),
        ),
        Candlestick(  # looks like a hammer but wick is too long
            open=Decimal("12322.04"),
            high=Decimal("12466.10"),
            low=Decimal("12175.66"),
            close=Decimal("12409.86"),
        ),
        Candlestick(  # looks like a hammer but tail is not long enough
            open=Decimal("14766.05"),
            high=Decimal("14766.55"),
            low=Decimal("14762.15"),
            close=Decimal("14764.45"),
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
