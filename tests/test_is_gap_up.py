import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from kandelero import Candlestick
from kandelero.patterns.helpers import is_gap_up


@pytest.mark.happy_path
@settings(
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    )
)
@given(data=st.data())
def test_is_gap_up_both_bullish(data, valid_decimal):
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

    assume(previous.close < current.open)  # gap
    assert is_gap_up(previous=previous, current=current)


@pytest.mark.happy_path
@settings(
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    )
)
@given(data=st.data())
def test_is_gap_up_both_bearish(data, valid_decimal):
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

    assume(current.close > previous.open)  # gap
    assert is_gap_up(previous=previous, current=current)


@pytest.mark.happy_path
@settings(
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    )
)
@given(data=st.data())
def test_is_gap_up_bear_plus_bull(data, valid_decimal):
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

    assume(current.open > previous.open)  # gap
    assert is_gap_up(previous=previous, current=current)


@pytest.mark.happy_path
@settings(
    suppress_health_check=(
        HealthCheck.filter_too_much,
        HealthCheck.too_slow,
    )
)
@given(data=st.data())
def test_is_gap_up_bull_plus_bear(data, valid_decimal):
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

    assume(current.close > previous.close)  # gap
    assert is_gap_up(previous=previous, current=current)
