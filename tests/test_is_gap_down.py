import pytest
from hypothesis import assume, given
from hypothesis import strategies as st
from kandelero import Candlestick
from kandelero.patterns.helpers import is_gap_down


@pytest.mark.happy_path
@given(data=st.data())
def test_is_gap_down_both_bullish(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)

    assume(previous.is_bullish)
    assume(current.is_bullish)

    current_open_below = current.close < previous.open
    assume(current_open_below)  # gap
    assert is_gap_down(previous=previous, current=current)


@pytest.mark.happy_path
@given(data=st.data())
def test_is_gap_down_both_bearish(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)

    assume(previous.is_bearish)
    assume(current.is_bearish)

    current_open_below = current.open < previous.close
    assume(current_open_below)  # gap
    assert is_gap_down(previous=previous, current=current)


@pytest.mark.happy_path
@given(data=st.data())
def test_is_gap_down_bear_plus_bull(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)

    assume(previous.is_bearish)
    assume(current.is_bullish)

    current_open_below = current.close < previous.close
    assume(current_open_below)  # gap
    assert is_gap_down(previous=previous, current=current)


@pytest.mark.happy_path
@given(data=st.data())
def test_is_gap_down_bull_plus_bear(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)

    assume(previous.is_bullish)
    assume(current.is_bearish)

    current_open_below = current.open < previous.open
    assume(current_open_below)  # gap
    assert is_gap_down(previous=previous, current=current)


@pytest.mark.unhappy_path
@given(data=st.data())
def test_no_gap_down_both_bullish(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)

    assume(previous.is_bullish)
    assume(current.is_bullish)

    current_open_inside_previous = previous.open <= current.open <= previous.close
    current_close_inside_previous = previous.open <= current.close <= previous.close
    assume(current_open_inside_previous or current_close_inside_previous)  # NO gap
    assert not is_gap_down(previous=previous, current=current)


@pytest.mark.unhappy_path
@given(data=st.data())
def test_no_gap_down_both_bearish(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)

    assume(previous.is_bearish)
    assume(current.is_bearish)

    current_open_inside_previous = previous.open <= current.open <= previous.close
    current_close_inside_previous = previous.close <= current.close <= previous.open
    assume(current_open_inside_previous or current_close_inside_previous)  # NO gap
    assert not is_gap_down(previous=previous, current=current)


@pytest.mark.unhappy_path
@given(data=st.data())
def test_no_gap_down_bear_plus_bull(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)

    assume(previous.is_bearish)
    assume(current.is_bullish)

    current_open_inside_previous = current.open >= previous.close
    current_close_inside_previous = previous.close <= current.close <= previous.open
    assume(current_open_inside_previous or current_close_inside_previous)  # NO gap
    assert not is_gap_down(previous=previous, current=current)


@pytest.mark.unhappy_path
@given(data=st.data())
def test_no_gap_down_bull_plus_bear(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)

    assume(previous.is_bullish)
    assume(current.is_bearish)

    current_open_inside_previous = previous.close <= current.open <= previous.close
    current_close_inside_previous = previous.open <= current.close <= previous.close
    assume(current_open_inside_previous or current_close_inside_previous)  # NO gap
    assert not is_gap_down(previous=previous, current=current)
