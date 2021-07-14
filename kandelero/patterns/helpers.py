from kandelero.candlestick import Candlestick


def is_gap(lowest: Candlestick, upmost: Candlestick) -> bool:
    return max(lowest.open, lowest.close) < min(upmost.open, upmost.close)


def is_gap_up(previous: Candlestick, current: Candlestick) -> bool:
    return is_gap(lowest=previous, upmost=current)


def is_gap_down(previous: Candlestick, current: Candlestick) -> bool:
    return is_gap(lowest=current, upmost=previous)
