import pytest
from hypothesis import assume, given
from hypothesis import strategies as st
from kandelero import Candlestick
from kandelero.patterns.comparators import is_bearish_harami, is_bullish_harami


@pytest.mark.bullish_pattern
@pytest.mark.happy_path
@given(
    data=st.data(),
)
def test_is_bullish_harami(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)
    assume(previous.is_bearish)
    assume(current.is_bullish)

    # harami properties
    current_open_inside_previous = previous.close <= current.open <= previous.open
    current_close_inside_previous = previous.close <= current.close <= previous.open
    assume(current_open_inside_previous and current_close_inside_previous)
    assume(previous.body_len >= (current.body_len * 2))
    assert is_bullish_harami(previous=previous, current=current)


@pytest.mark.bearish_pattern
@pytest.mark.happy_path
@given(
    data=st.data(),
)
def test_is_bearish_harami(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)

    assume(previous.is_bullish)
    assume(current.is_bearish)

    # harami properties
    current_open_inside_previous = previous.open <= current.open <= previous.close
    current_close_inside_previous = previous.open <= current.close <= previous.close
    assume(current_open_inside_previous and current_close_inside_previous)
    assume(previous.body_len >= current.body_len * 2)
    assert is_bearish_harami(previous=previous, current=current)


@pytest.mark.bullish_pattern
@pytest.mark.unhappy_path
@given(
    data=st.data(),
)
def test_no_bullish_harami(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)

    assume(previous.is_bearish)
    assume(current.is_bullish)

    # harami properties
    current_open_inside_previous = previous.close <= current.open <= previous.open
    current_close_inside_previous = previous.close <= current.close <= previous.open
    assume(
        previous.body_len < (current.body_len * 2)
        or not (current_open_inside_previous and current_close_inside_previous)
    )
    assert not is_bullish_harami(previous=previous, current=current)


@pytest.mark.bearish_pattern
@pytest.mark.unhappy_path
@given(
    data=st.data(),
)
def test_no_bearish_harami(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)

    assume(previous.is_bullish)
    assume(current.is_bearish)

    current_open_inside_previous = previous.open <= current.open <= previous.close
    current_close_inside_previous = previous.open <= current.close <= previous.close
    assume(
        previous.body_len < (current.body_len * 2)
        or not (current_open_inside_previous and current_close_inside_previous)
    )
    assert not is_bearish_harami(previous=previous, current=current)
