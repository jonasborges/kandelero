import pytest
from hypothesis import assume, given
from hypothesis import strategies as st
from kandelero import Candlestick
from kandelero.patterns.comparators import is_bearish_engulfing, is_bullish_engulfing


@pytest.mark.bearish_pattern
@pytest.mark.happy_path
@given(
    data=st.data(),
)
def test_is_bearish_engulfing(data, valid_decimal, generate_values):
    shortest_args = generate_values(data, valid_decimal)
    longest_args = generate_values(data, valid_decimal)
    shortest = Candlestick(**shortest_args)
    longest = Candlestick(**longest_args)

    assume(shortest.is_bullish)
    assume(longest.is_bearish)

    assume(
        longest.close < shortest.open and longest.open >= shortest.close
    )  # engulfing
    assert is_bearish_engulfing(shortest, longest)


@pytest.mark.bullish_pattern
@pytest.mark.happy_path
@given(
    data=st.data(),
)
def test_is_bullish_engulfing(data, valid_decimal, generate_values):
    shortest_args = generate_values(data, valid_decimal)
    longest_args = generate_values(data, valid_decimal)
    shortest = Candlestick(**shortest_args)
    longest = Candlestick(**longest_args)
    assume(
        longest.close > shortest.open and longest.open <= shortest.close
    )  # engulfing

    assume(shortest.is_bearish)
    assume(longest.is_bullish)
    assert is_bullish_engulfing(shortest, longest)
