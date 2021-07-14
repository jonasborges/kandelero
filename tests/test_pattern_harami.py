import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from kandelero import Candlestick
from kandelero.patterns.comparators import is_bearish_harami, is_bullish_harami


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
def test_is_bullish_harami(valid_decimal, data):
    previous = Candlestick(
        open=data.draw(valid_decimal),
        high=data.draw(valid_decimal),
        low=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(previous.close < previous.open)  # bearish candle

    current = Candlestick(
        open=data.draw(valid_decimal),
        high=data.draw(valid_decimal),
        low=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(current.close > current.open)  # bullish candle

    current_open_inside_previous = previous.close <= current.open <= previous.open
    current_close_inside_previous = previous.close <= current.close <= previous.open
    assume(current_open_inside_previous and current_close_inside_previous)

    assume(previous.body_len >= (current.body_len * 2))

    assert is_bullish_harami(previous=previous, current=current)


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
def test_is_bearish_harami(valid_decimal, data):
    previous = Candlestick(
        open=data.draw(valid_decimal),
        high=data.draw(valid_decimal),
        low=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(previous.close > previous.open)  # bullish candle

    current = Candlestick(
        open=data.draw(valid_decimal),
        high=data.draw(valid_decimal),
        low=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(current.close < current.open)  # bearish candle

    current_open_inside_previous = previous.open <= current.open <= previous.close
    current_close_inside_previous = previous.open <= current.close <= previous.close
    assume(current_open_inside_previous and current_close_inside_previous)

    assume(previous.body_len >= current.body_len * 2)

    assert is_bearish_harami(previous=previous, current=current)


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
def test_no_bullish_harami(valid_decimal, data):
    previous = Candlestick(
        open=data.draw(valid_decimal),
        high=data.draw(valid_decimal),
        low=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(previous.close < previous.open)  # bearish candle

    current = Candlestick(
        open=data.draw(valid_decimal),
        high=data.draw(valid_decimal),
        low=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(current.close > current.open)  # bullish candle

    current_open_inside_previous = previous.close <= current.open <= previous.open
    current_close_inside_previous = previous.close <= current.close <= previous.open
    assume(
        previous.body_len < (current.body_len * 2)
        or not (current_open_inside_previous and current_close_inside_previous)
    )

    assert not is_bullish_harami(previous=previous, current=current)


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
def test_no_bearish_harami(valid_decimal, data):
    previous = Candlestick(
        open=data.draw(valid_decimal),
        high=data.draw(valid_decimal),
        low=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(previous.close > previous.open)  # bullish candle

    current = Candlestick(
        open=data.draw(valid_decimal),
        high=data.draw(valid_decimal),
        low=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(current.close < current.open)  # bearish candle

    current_open_inside_previous = previous.open <= current.open <= previous.close
    current_close_inside_previous = previous.open <= current.close <= previous.close
    assume(
        previous.body_len < (current.body_len * 2)
        or not (current_open_inside_previous and current_close_inside_previous)
    )

    assert not is_bearish_harami(previous=previous, current=current)
