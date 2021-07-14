import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from kandelero import Candlestick
from kandelero.patterns.comparators import is_bearish_kicker, is_bullish_kicker


@pytest.mark.bearish_pattern
@pytest.mark.happy_path
@settings(
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    )
)
@given(
    data=st.data(),
)
def test_is_bearish_kicker(valid_decimal, data):
    previous = Candlestick(
        high=data.draw(valid_decimal),
        low=data.draw(valid_decimal),
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(previous.close > previous.open)  # bullish candle

    current = Candlestick(
        high=data.draw(valid_decimal),
        low=data.draw(valid_decimal),
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(current.close < current.open)  # bearish candle

    assume(current.open < previous.open and current.high < previous.low)  # gap

    assert is_bearish_kicker(previous, current)
    assert previous.is_bullish
    assert current.is_bearish


@pytest.mark.bearish_pattern
@pytest.mark.unhappy_path
@settings(
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    )
)
@given(
    data=st.data(),
)
def test_no_bearish_kicker(valid_decimal, data):
    previous = Candlestick(
        high=data.draw(valid_decimal),
        low=data.draw(valid_decimal),
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )

    current = Candlestick(
        high=data.draw(valid_decimal),
        low=data.draw(valid_decimal),
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(current.close < current.open)  # bearish candle

    assume(
        not previous.is_bullish
        or not current.is_bearish
        or current.high >= previous.low
    )

    assert not is_bearish_kicker(previous, current)


@pytest.mark.bullish_pattern
@pytest.mark.happy_path
@settings(
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    )
)
@given(
    data=st.data(),
)
def test_is_bullish_kicker(valid_decimal, data):
    previous = Candlestick(
        high=data.draw(valid_decimal),
        low=data.draw(valid_decimal),
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(previous.close < previous.open)  # bearish candle

    current = Candlestick(
        high=data.draw(valid_decimal),
        low=data.draw(valid_decimal),
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(current.close > current.open)  # bullish candle

    assume(current.open > previous.open and current.low > previous.high)  # gap

    assert is_bullish_kicker(previous, current)
    assert previous.is_bearish
    assert current.is_bullish


@pytest.mark.bullish_pattern
@pytest.mark.unhappy_path
@settings(
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    )
)
@given(
    data=st.data(),
)
def test_no_bullish_kicker(valid_decimal, data):
    previous = Candlestick(
        high=data.draw(valid_decimal),
        low=data.draw(valid_decimal),
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )

    current = Candlestick(
        high=data.draw(valid_decimal),
        low=data.draw(valid_decimal),
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(current.close > current.open)  # bullish candle

    assume(
        not previous.is_bearish
        or not current.is_bullish
        or current.low <= previous.high
    )

    assert not is_bullish_kicker(previous, current)
