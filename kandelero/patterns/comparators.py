from dataclasses import dataclass
from functools import wraps
from typing import Callable

from kandelero import patterns
from kandelero.candlestick import Candlestick
from kandelero.context import Bottom, MarketContext, Top
from kandelero.context.market_context import PriceLevel
from kandelero.patterns.names import get_pattern_name

from .helpers import (
    is_bearish_breakout_attempt,
    is_bullish_breakout_attempt,
    is_gap_down,
    is_gap_up,
    is_hammer_like,
    is_harami_size,
    is_inverted_hammer_like,
)


@dataclass
class PatternFound:
    comparator: Callable
    previous: Candlestick
    current: Candlestick
    price_level: PriceLevel

    def __post_init__(self):
        self.name = get_pattern_name(self.comparator)


def market_context_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    wrapper.market_context_required = True
    return wrapper


@dataclass
class ComparatorResponse:
    found: bool
    pattern: callable

    def get_details(self):
        return get_pattern_name(self.pattern)

    def __bool__(self):
        return self.found


@dataclass
class ComparatorResponseWithContext(ComparatorResponse):
    pattern: PatternFound = None

    def get_details(self):
        p = self.pattern
        return " - ".join(
            (
                p.name,
                p.price_level.candlestick.timestamp.isoformat().replace("T", " "),
                f"{p.price_level.__class__.__name__}: {p.price_level.value}",
            )
        )


def comparator_response(func: Callable):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response: bool = func(*args, **kwargs)
        return ComparatorResponse(found=response, pattern=func)

    return wrapper


@comparator_response
def is_doji(candlestick: Candlestick) -> bool:
    return candlestick.open == candlestick.close


@comparator_response
def is_bullish_engulfing(previous: Candlestick, current: Candlestick) -> bool:
    """Engulfs previous candle body. Wick and tail not included"""
    return (
        previous.is_bearish
        and current.is_bullish
        and current.open <= previous.close
        and current.close > previous.open
    )


@comparator_response
def is_bearish_engulfing(previous: Candlestick, current: Candlestick) -> bool:
    """Engulfs previous candle body. Wick and tail not included"""
    return (
        previous.is_bullish
        and current.is_bearish
        and current.open >= previous.close
        and current.close < previous.open
    )


@comparator_response
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


@comparator_response
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


@comparator_response
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


@comparator_response
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


@comparator_response
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


@comparator_response
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


@comparator_response
def is_hammer(candlestick: Candlestick) -> bool:
    return is_hammer_like(candlestick=candlestick)


@comparator_response
def is_inverted_hammer(candlestick: Candlestick) -> bool:
    return is_inverted_hammer_like(candlestick=candlestick)


@comparator_response
def is_hanging_man(previous: Candlestick, current: Candlestick) -> bool:
    return is_gap_up(previous=previous, current=current) and is_hammer_like(
        candlestick=current
    )


@comparator_response
def is_shooting_star(previous: Candlestick, current: Candlestick) -> bool:
    return is_gap_up(previous=previous, current=current) and is_inverted_hammer_like(
        candlestick=current
    )


@comparator_response
def is_piercing_line(previous: Candlestick, current: Candlestick) -> bool:
    return (
        previous.is_bearish
        and current.is_bullish
        and current.open < previous.close
        # above the middle but not engulfing previous candle
        and previous.middle_point < current.close < previous.open
    )


@comparator_response
def is_dark_cloud_cover(previous: Candlestick, current: Candlestick) -> bool:
    return (
        previous.is_bullish
        and current.is_bearish
        and current.open > previous.close
        # below the middle but not engulfing previous candle
        and previous.open < current.close < previous.middle_point
    )


@market_context_required
def is_bull_trap(
    previous: Candlestick, current: Candlestick, market_context: MarketContext
) -> ComparatorResponse:
    for top in market_context.get_tops(before_date=previous.timestamp):
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
            return ComparatorResponseWithContext(
                found=True,
                pattern=PatternFound(
                    price_level=top,
                    previous=previous,
                    current=previous,
                    comparator=is_bull_trap,
                ),
            )
    return ComparatorResponseWithContext(found=False)


@market_context_required
def is_bear_trap(
    previous: Candlestick, current: Candlestick, market_context: MarketContext
) -> ComparatorResponse:
    for bottom in market_context.get_bottoms(before_date=previous.timestamp):
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
            return ComparatorResponseWithContext(
                found=True,
                pattern=PatternFound(
                    price_level=bottom,
                    previous=previous,
                    current=previous,
                    comparator=is_bear_trap,
                ),
            )
    return ComparatorResponseWithContext(found=False)


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
