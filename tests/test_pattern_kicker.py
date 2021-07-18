import pytest
from hypothesis import assume, given
from hypothesis import strategies as st
from kandelero import Candlestick
from kandelero.patterns.comparators import is_bearish_kicker, is_bullish_kicker


@pytest.mark.bearish_pattern
@pytest.mark.happy_path
@given(
    data=st.data(),
)
def test_is_bearish_kicker(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)
    assume(previous.is_bullish)
    assume(current.is_bearish)

    assume(current.open < previous.open and current.high < previous.low)  # gap

    assert is_bearish_kicker(previous, current)


@pytest.mark.bearish_pattern
@pytest.mark.unhappy_path
@given(
    data=st.data(),
)
def test_no_bearish_kicker(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)

    assume(
        not previous.is_bullish
        or not current.is_bearish
        or (current.is_bearish and current.high >= previous.low)
    )

    assert not is_bearish_kicker(previous, current)


@pytest.mark.bullish_pattern
@pytest.mark.happy_path
@given(
    data=st.data(),
)
def test_is_bullish_kicker(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)
    assume(previous.is_bearish)
    assume(current.is_bullish)

    assume(current.open > previous.open and current.low > previous.high)  # gap
    assert is_bullish_kicker(previous, current)


@pytest.mark.bullish_pattern
@pytest.mark.unhappy_path
@given(
    data=st.data(),
)
def test_no_bullish_kicker(data, valid_decimal, generate_values):
    previous_args = generate_values(data, valid_decimal)
    current_args = generate_values(data, valid_decimal)
    previous = Candlestick(**previous_args)
    current = Candlestick(**current_args)

    assume(
        not previous.is_bearish
        or not current.is_bullish
        or (current.is_bullish and current.low <= previous.high)
    )

    assert not is_bullish_kicker(previous, current)
