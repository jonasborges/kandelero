import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from kandelero import Candlestick
from kandelero.patterns.helpers import is_gap_down


@pytest.mark.happy_path
@settings(
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    )
)
@given(data=st.data())
def test_is_gap_down_both_bullish(data, valid_decimal):
    previous = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(previous.close > previous.open)  # bullish

    current = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(current.close > current.open)  # bullish

    current_open_below = current.close < previous.open
    assume(current_open_below)  # gap
    assert is_gap_down(previous=previous, current=current)


@pytest.mark.happy_path
@settings(
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    )
)
@given(data=st.data())
def test_is_gap_down_both_bearish(data, valid_decimal):
    previous = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(previous.close < previous.open)  # bearish

    current = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(current.close < current.open)  # bearish

    current_open_below = current.open < previous.close
    assume(current_open_below)  # gap
    assert is_gap_down(previous=previous, current=current)


@pytest.mark.happy_path
@settings(
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    )
)
@given(data=st.data())
def test_is_gap_down_bear_plus_bull(data, valid_decimal):
    previous = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(previous.close < previous.open)  # bearish

    current = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(current.close > current.open)  # bullish

    current_open_below = current.close < previous.close
    assume(current_open_below)  # gap
    assert is_gap_down(previous=previous, current=current)


@pytest.mark.happy_path
@settings(
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    )
)
@given(data=st.data())
def test_is_gap_down_bull_plus_bear(data, valid_decimal):
    previous = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(previous.close > previous.open)  # bullish

    current = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(current.close < current.open)  # bearish

    current_open_below = current.open < previous.open
    assume(current_open_below)  # gap
    assert is_gap_down(previous=previous, current=current)


@pytest.mark.unhappy_path
@settings(
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    )
)
@given(data=st.data())
def test_no_gap_down_both_bullish(data, valid_decimal):
    previous = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(previous.close > previous.open)  # bullish

    current = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(current.close > current.open)  # bullish

    current_open_inside_previous = previous.open <= current.open <= previous.close
    current_close_inside_previous = previous.open <= current.close <= previous.close
    assume(current_open_inside_previous or current_close_inside_previous)  # NO gap
    assert not is_gap_down(previous=previous, current=current)


@pytest.mark.unhappy_path
@settings(
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    )
)
@given(data=st.data())
def test_no_gap_down_both_bearish(data, valid_decimal):
    previous = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(previous.close < previous.open)  # bearish

    current = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(current.close < current.open)  # bearish

    current_open_inside_previous = previous.open <= current.open <= previous.close
    current_close_inside_previous = previous.close <= current.close <= previous.open
    assume(current_open_inside_previous or current_close_inside_previous)  # NO gap
    assert not is_gap_down(previous=previous, current=current)


@pytest.mark.unhappy_path
@settings(
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    )
)
@given(data=st.data())
def test_no_gap_down_bear_plus_bull(data, valid_decimal):
    previous = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(previous.close < previous.open)  # bearish

    current = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(current.close > current.open)  # bullish

    current_open_inside_previous = current.open >= previous.close
    current_close_inside_previous = previous.close <= current.close <= previous.open
    assume(current_open_inside_previous or current_close_inside_previous)  # NO gap
    assert not is_gap_down(previous=previous, current=current)


@pytest.mark.unhappy_path
@settings(
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    )
)
@given(data=st.data())
def test_no_gap_down_bull_plus_bear(data, valid_decimal):
    previous = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(previous.close > previous.open)  # bullish

    current = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(current.close < current.open)  # bearish

    current_open_inside_previous = previous.close <= current.open <= previous.close
    current_close_inside_previous = previous.open <= current.close <= previous.close
    assume(current_open_inside_previous or current_close_inside_previous)  # NO gap
    assert not is_gap_down(previous=previous, current=current)
