from kandelero.candlestick import Candlestick


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
