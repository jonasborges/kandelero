from decimal import Decimal

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st
from kandelero import Candlestick
from kandelero.calculations import MAX_VALUE, MIN_VALUE

DECIMAL = st.decimals(
    min_value=MIN_VALUE,
    max_value=MAX_VALUE,
    allow_nan=False,
    allow_infinity=False,
    places=4,
)

DEFAULT_SCENARIO = (
    DECIMAL,
    DECIMAL,
    DECIMAL,
    DECIMAL,
)


@given(*DEFAULT_SCENARIO)
def test_is_bullish(open, high, low, close):
    # is_valid_candle
    assume(high >= open)
    assume(high >= low)
    assume(high >= close)
    assume(low <= open)
    assume(low <= close)

    # is bullish
    assume(close > open)
    obj = Candlestick(open=open, high=high, low=low, close=close)

    assert obj.is_bullish
    assert not obj.is_bearish


@given(*DEFAULT_SCENARIO)
def test_is_bearish(open, high, low, close):
    assume(high >= open)
    assume(high >= low)
    assume(high >= close)
    assume(low <= open)
    assume(low <= close)
    assume(close < open)
    obj = Candlestick(open=open, high=high, low=low, close=close)

    assert not obj.is_bullish
    assert obj.is_bearish


@given(DECIMAL, DECIMAL, DECIMAL)
def test_neither_bear_nor_bull(value, high, low):
    open = close = value
    assume(high >= open)
    assume(high >= low)
    assume(high >= close)
    assume(low <= open)
    assume(low <= close)
    obj = Candlestick(open=open, high=high, low=low, close=close)

    assert not obj.is_bullish
    assert not obj.is_bearish


@given(
    DECIMAL,
    DECIMAL,
    DECIMAL,
    DECIMAL,
)
def test_bear_or_bull(open, high, low, close):
    assume(high >= open)
    assume(high >= low)
    assume(high >= close)
    assume(low <= open)
    assume(low <= close)

    assume(close != open)
    obj = Candlestick(open=open, high=high, low=low, close=close)

    assert any(x for x in (obj.is_bullish, obj.is_bearish))
    assert not all(x for x in (obj.is_bullish, obj.is_bearish))


@given(*DEFAULT_SCENARIO)
def test_properties(open, high, low, close):
    assume(high >= open)
    assume(high >= low)
    assume(high >= close)
    assume(low <= open)
    assume(low <= close)
    obj = Candlestick(open=open, high=high, low=low, close=close)

    assert obj.full_len == obj.body_len + obj.wick_len + obj.tail_len
    assert obj.full_len - (obj.body_len + obj.wick_len + obj.tail_len) == 0
    assert obj.body_len == obj.full_len - obj.wick_len - obj.tail_len
    assert obj.wick_len == obj.full_len - obj.body_len - obj.tail_len
    assert obj.tail_len == obj.full_len - obj.body_len - obj.wick_len

    assert obj.wick_len + obj.tail_len == obj.full_len - obj.body_len
    assert obj.is_valid_candle


@given(*DEFAULT_SCENARIO)
def test_proportions(open, high, low, close):
    assume(high >= open)
    assume(high >= low)
    assume(high >= close)
    assume(low <= open)
    assume(low <= close)

    obj = Candlestick(open=open, high=high, low=low, close=close)

    is_flat_candle = open == high == low == close

    assert obj.is_valid_candle
    if is_flat_candle:
        assert (
            obj.body_proportion + obj.tail_proportion + obj.wick_proportion == 0
            and is_flat_candle
        ), "%s is not 0" % (
            obj.body_proportion + obj.tail_proportion + obj.wick_proportion
        )
    else:
        assert (
            obj.body_proportion + obj.tail_proportion + obj.wick_proportion == 1
            and not (is_flat_candle)
        ), "%s is not 1" % (
            obj.body_proportion + obj.tail_proportion + obj.wick_proportion
        )


@pytest.mark.parametrize(
    "obj",
    [
        Candlestick(
            open=Decimal("500"),
            high=Decimal("11600"),
            low=Decimal("100"),
            close=Decimal("200"),
        ),
        Candlestick(
            open=Decimal("2"),
            high=Decimal("4"),
            low=Decimal("1"),
            close=Decimal("3"),
        ),
        Candlestick(
            open=Decimal("2"),
            high=Decimal("4"),
            low=Decimal("1"),
            close=Decimal("2"),
        ),
        Candlestick(
            open=Decimal("0.0001"),
            high=Decimal("0.0002"),
            low=Decimal("0.0001"),
            close=Decimal("0.0001"),
        ),
    ],
)
def test_special_cases_proportions(obj):
    assert obj.body_proportion + obj.tail_proportion + obj.wick_proportion == 1


@pytest.mark.parametrize(
    "obj",
    [
        Candlestick(
            open=MAX_VALUE,
            high=MAX_VALUE,
            low=MAX_VALUE,
            close=MAX_VALUE,
        ),
        Candlestick(
            open=MIN_VALUE,
            high=MIN_VALUE,
            low=MIN_VALUE,
            close=MIN_VALUE,
        ),
    ],
)
def test_special_cases_proportions_zero(obj):
    assert obj.body_proportion + obj.tail_proportion + obj.wick_proportion == 0
