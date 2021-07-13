from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from kandelero import Candlestick

NOT_NAN_DECIMAL = st.decimals(
    allow_nan=False,
)

DECIMAL = st.decimals(
    min_value=0.00000000000000000001,
    max_value=900000000000000000000,
    allow_nan=False,
    allow_infinity=False,
    places=20,
)

DEFAULT_SCENARIO = (
    DECIMAL,
    DECIMAL,
    DECIMAL,
    DECIMAL,
)


@given(*DEFAULT_SCENARIO)
def test_is_bullish(open, high, low, close):
    assume(close > open)
    obj = Candlestick(open=open, high=high, low=low, close=close)
    assert obj.is_bullish
    assert not obj.is_bearish


@given(*DEFAULT_SCENARIO)
def test_is_bearish(open, high, low, close):
    assume(close < open)
    obj = Candlestick(open=open, high=high, low=low, close=close)
    assert not obj.is_bullish
    assert obj.is_bearish


@given(NOT_NAN_DECIMAL, NOT_NAN_DECIMAL, NOT_NAN_DECIMAL)
def test_neither_bear_nor_bull(value, high, low):
    open = close = value
    obj = Candlestick(open=open, high=high, low=low, close=close)
    assert not obj.is_bullish
    assert not obj.is_bearish


@settings(suppress_health_check=(HealthCheck.too_slow,))
@given(
    NOT_NAN_DECIMAL,
    st.decimals(),
    st.decimals(),
    NOT_NAN_DECIMAL,
)
def test_bear_or_bull(open, high, low, close):
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
