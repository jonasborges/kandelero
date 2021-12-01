from decimal import Context
from typing import Callable, List, Optional

from kandelero.candlestick import Candlestick
from kandelero.context.market_context import MarketContext


def find_patterns(
    comparators: List[Callable],
    previous: Candlestick,
    current: Candlestick,
    market_context: Optional[MarketContext] = None,
) -> List[str]:
    params = dict(previous=previous, current=current)
    if market_context:
        params["market_context"] = market_context
    return [comparator for comparator in comparators if comparator(**params)]
