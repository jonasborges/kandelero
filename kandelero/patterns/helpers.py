from decimal import Decimal

from kandelero.candlestick import Candlestick


def is_hammer_like(candlestick: Candlestick) -> bool:
    return candlestick.tail_proportion > (
        candlestick.body_proportion * 2
    ) and candlestick.wick_proportion <= Decimal("0.1")


def is_inverted_hammer_like(candlestick: Candlestick) -> bool:
    return candlestick.wick_proportion > (
        candlestick.body_proportion * 2
    ) and candlestick.tail_proportion <= Decimal("0.1")


def is_gap(lowest: Candlestick, upmost: Candlestick) -> bool:
    return max(lowest.open, lowest.close) < min(upmost.open, upmost.close)


def is_gap_up(previous: Candlestick, current: Candlestick) -> bool:
    return is_gap(lowest=previous, upmost=current)


def is_gap_down(previous: Candlestick, current: Candlestick) -> bool:
    return is_gap(lowest=current, upmost=previous)


def is_harami_size(previous: Candlestick, current: Candlestick) -> bool:
    return current.body_len <= (previous.body_len * Decimal("0.5"))
