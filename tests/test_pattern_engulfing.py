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
def test_is_bearish_engulfing(valid_decimal, decimal_min_value, data):
    shortest = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(shortest.close > shortest.open)  # bullish candle

    longest = Candlestick(
        high=None,
        low=None,
        open=data.draw(
            st.decimals(min_value=shortest.close, allow_infinity=False, allow_nan=False)
        ),
        close=data.draw(
            st.decimals(
                allow_infinity=False,
                allow_nan=False,
                max_value=shortest.open - decimal_min_value,
            )
        ),
    )
    assume(longest.close < longest.open)  # bearish candle

    assert is_bearish_engulfing(shortest, longest)
    assert shortest.is_bullish
    assert longest.is_bearish


@pytest.mark.bullish_pattern
@pytest.mark.happy_path
@given(
    data=st.data(),
)
def test_is_bullish_engulfing(valid_decimal, decimal_min_value, data):
    shortest = Candlestick(
        high=None,
        low=None,
        open=data.draw(valid_decimal),
        close=data.draw(valid_decimal),
    )
    assume(shortest.close < shortest.open)  # bearish candle

    longest = Candlestick(
        high=None,
        low=None,
        open=data.draw(
            st.decimals(
                max_value=shortest.close,
                allow_infinity=False,
                allow_nan=False,
                min_value=decimal_min_value,
            )
        ),
        close=data.draw(
            st.decimals(
                allow_infinity=False,
                allow_nan=False,
                min_value=shortest.open + decimal_min_value,
            )
        ),
    )
    assume(longest.close > longest.open)  # bullish candle

    assert is_bullish_engulfing(shortest, longest)
    assert shortest.is_bearish
    assert longest.is_bullish
