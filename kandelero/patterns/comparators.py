from kandelero.candlestick import Candlestick

from .helpers import is_gap_down, is_gap_up


def is_bullish_engulfing(previous: Candlestick, current: Candlestick):
    return (
        previous.is_bearish
        and current.is_bullish
        and current.open <= previous.close
        and current.close > previous.open
    )


def is_bearish_engulfing(previous: Candlestick, current: Candlestick):
    return (
        previous.is_bullish
        and current.is_bearish
        and current.open >= previous.close
        and current.close < previous.open
    )


def is_bullish_kicker(previous: Candlestick, current: Candlestick):
    return (
        previous.is_bearish
        and current.is_bullish
        and is_gap_up(previous, current)
        and current.low > previous.high
    )


def is_bearish_kicker(previous: Candlestick, current: Candlestick):
    return (
        previous.is_bullish
        and current.is_bearish
        and is_gap_down(previous, current)
        and current.high < previous.low
    )


COMPARATORS = [
    is_bearish_engulfing,
    is_bullish_engulfing,
    is_bullish_kicker,
    is_bearish_kicker,
]
