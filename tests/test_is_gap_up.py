import pytest
from hypothesis import assume, given
from hypothesis import strategies as st
from kandelero import Candlestick
from kandelero.patterns.helpers import is_gap_up


@pytest.mark.happy_path
@given(data=st.data())
def test_is_gap_up_both_bullish(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)

    assume(previous.is_bullish)
    assume(current.is_bullish)

    assume(previous.close < current.open)  # gap
    assert is_gap_up(previous=previous, current=current)


@pytest.mark.happy_path
@given(data=st.data())
def test_is_gap_up_both_bearish(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)

    assume(previous.is_bearish)

    assume(current.is_bearish)

    assume(current.close > previous.open)  # gap
    assert is_gap_up(previous=previous, current=current)


@pytest.mark.happy_path
@given(data=st.data())
def test_is_gap_up_bear_plus_bull(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)

    assume(previous.is_bearish)

    assume(current.is_bullish)

    assume(current.open > previous.open)  # gap
    assert is_gap_up(previous=previous, current=current)


@pytest.mark.happy_path
@given(data=st.data())
def test_is_gap_up_bull_plus_bear(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)

    assume(previous.is_bullish)

    assume(current.is_bearish)

    assume(current.close > previous.close)  # gap
    assert is_gap_up(previous=previous, current=current)
