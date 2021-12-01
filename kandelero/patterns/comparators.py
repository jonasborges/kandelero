from kandelero.candlestick import Candlestick
from kandelero.context import Bottom, MarketContext, Top

from .helpers import (
    is_bearish_breakout_attempt,
    is_bullish_breakout_attempt,
    is_gap_down,
    is_gap_up,
    is_hammer_like,
    is_harami_size,
    is_inverted_hammer_like,
)


def is_doji(candlestick: Candlestick) -> bool:
    return candlestick.open == candlestick.close


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


def is_bearish_harami_cross(previous: Candlestick, current: Candlestick) -> bool:
    current_open_inside_previous = previous.open <= current.open <= previous.close
    current_close_inside_previous = previous.open <= current.close <= previous.close

    return (
        previous.is_bullish
        and current_open_inside_previous
        and current_close_inside_previous
        and is_doji(current)
        and is_harami_size(
            previous=previous,
            current=current,
        )
    )


def is_bullish_harami_cross(previous: Candlestick, current: Candlestick) -> bool:
    current_open_inside_previous = previous.close <= current.open <= previous.open
    current_close_inside_previous = previous.close <= current.close <= previous.open

    return (
        previous.is_bearish
        and current_open_inside_previous
        and current_close_inside_previous
        and is_doji(current)
        and is_harami_size(
            previous=previous,
            current=current,
        )
    )


def is_hammer(candlestick: Candlestick) -> bool:
    return is_hammer_like(candlestick=candlestick)


def is_inverted_hammer(candlestick: Candlestick) -> bool:
    return is_inverted_hammer_like(candlestick=candlestick)


def is_hanging_man(previous: Candlestick, current: Candlestick) -> bool:
    return is_gap_up(previous=previous, current=current) and is_hammer_like(
        candlestick=current
    )


def is_shooting_star(previous: Candlestick, current: Candlestick) -> bool:
    return is_gap_up(previous=previous, current=current) and is_inverted_hammer_like(
        candlestick=current
    )


def is_piercing_line(previous: Candlestick, current: Candlestick) -> bool:
    return (
        previous.is_bearish
        and current.is_bullish
        and current.open < previous.close
        # above the middle but not engulfing previous candle
        and previous.middle_point < current.close < previous.open
    )


def is_dark_cloud_cover(previous: Candlestick, current: Candlestick) -> bool:
    return (
        previous.is_bullish
        and current.is_bearish
        and current.open > previous.close
        # below the middle but not engulfing previous candle
        and previous.open < current.close < previous.middle_point
    )


def is_bull_trap(
    previous: Candlestick, current: Candlestick, market_context: MarketContext
) -> bool:
    for top in market_context.get_tops():
        closed_below_previous = current.close <= previous.low
        closed_below_top = current.close < top.value
        conditions = (
            previous.is_bullish,
            current.is_bearish,
            is_bullish_breakout_attempt(candlestick=previous, top=top),
            closed_below_previous,
            closed_below_top,
        )
        if all(conditions):
            return True
    return False


def is_bear_trap(
    previous: Candlestick, current: Candlestick, market_context: MarketContext
) -> bool:
    for bottom in market_context.get_bottoms():
        closed_above_previous = current.close >= previous.high
        closed_above_bottom = current.close > bottom.value
        conditions = (
            previous.is_bearish,
            current.is_bullish,
            is_bearish_breakout_attempt(candlestick=previous, bottom=bottom),
            closed_above_previous,
            closed_above_bottom,
        )
        if all(conditions):
            return True
    return False


COMPARATORS = [
    is_bearish_engulfing,
    is_bullish_engulfing,
    is_bullish_kicker,
    is_bearish_kicker,
    is_bearish_harami,
    is_bullish_harami,
    is_bullish_harami_cross,
    is_bearish_harami_cross,
    is_hanging_man,
    is_shooting_star,
    is_piercing_line,
    is_dark_cloud_cover,
]

CONTEXT_COMPARATORS = [
    is_bull_trap,
    is_bear_trap,
]


SINGLE_CANDLE_COMPARATORS = [
    is_hammer,
    is_inverted_hammer,
    is_doji,
]
