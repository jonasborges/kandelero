from typing import Callable, List

from kandelero.candlestick import Candlestick


def find_patterns(
    comparators: List[Callable],
    previous: Candlestick,
    current: Candlestick,
) -> List[str]:
    return [comparator for comparator in comparators if comparator(previous, current)]
