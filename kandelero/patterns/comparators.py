from kandelero.candlestick import Candlestick

from .helpers import (
    is_gap_down,
    is_gap_up,
    is_hammer_like,
    is_harami_size,
    is_inverted_hammer_like,
)


def is_bullish_engulfing(previous: Candlestick, current: Candlestick) -> bool:
    """Engulfs previous candle body. Wick and tail not included"""
    return (
        previous.is_bearish
        and current.is_bullish
        and current.open <= previous.close
        and current.close > previous.open
    )


def is_bearish_engulfing(previous: Candlestick, current: Candlestick) -> bool:
    """Engulfs previous candle body. Wick and tail not included"""
    return (
        previous.is_bullish
        and current.is_bearish
        and current.open >= previous.close
        and current.close < previous.open
    )


def is_bullish_kicker(previous: Candlestick, current: Candlestick) -> bool:
    return (
        previous.is_bearish
        and current.is_bullish
        and is_gap_up(
            previous=previous,
            current=current,
        )
        and current.low > previous.high
    )


def is_bearish_kicker(previous: Candlestick, current: Candlestick) -> bool:
    return (
        previous.is_bullish
        and current.is_bearish
        and is_gap_down(
            previous=previous,
            current=current,
        )
        and current.high < previous.low
    )


def is_bullish_harami(previous: Candlestick, current: Candlestick) -> bool:
    current_open_inside_previous = previous.close <= current.open <= previous.open
    current_close_inside_previous = previous.close <= current.close <= previous.open
    return (
        previous.is_bearish
        and current.is_bullish
        and current_open_inside_previous
        and current_close_inside_previous
        and is_harami_size(
            previous=previous,
            current=current,
        )
    )


def is_bearish_harami(previous: Candlestick, current: Candlestick) -> bool:
    current_open_inside_previous = previous.open <= current.open <= previous.close
    current_close_inside_previous = previous.open <= current.close <= previous.close

    return (
        previous.is_bullish
        and current.is_bearish
        and current_open_inside_previous
        and current_close_inside_previous
        and is_harami_size(
            previous=previous,
            current=current,
        )
    )


def is_hammer(candlestick: Candlestick) -> bool:
    return is_hammer_like(candlestick=candlestick)


def is_inverted_hammer(candlestick: Candlestick) -> bool:
    return is_inverted_hammer_like(candlestick=candlestick)


COMPARATORS = [
    is_bearish_engulfing,
    is_bullish_engulfing,
    is_bullish_kicker,
    is_bearish_kicker,
    is_bearish_harami,
    is_bullish_harami,
]


SINGLE_CANDLE_COMPARATORS = [
    is_hammer,
    is_inverted_hammer,
]
