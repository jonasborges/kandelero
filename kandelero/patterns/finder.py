from decimal import Context
from typing import Callable, List, Optional

from kandelero.candlestick import Candlestick
from kandelero.context.market_context import MarketContext
from kandelero.patterns.comparators import ComparatorResponse, PatternFound


def get_comparator_params(
    comparator: Callable,
    regular_params: dict,
    market_context: Optional[MarketContext] = None,
):
    market_context_params = {
        "market_context": market_context,
        **regular_params,
    }
    if market_context and getattr(comparator, "market_context_required", None):
        return market_context_params
    return regular_params


def find_patterns(
    comparators: List[Callable],
    previous: Candlestick,
    current: Candlestick,
    market_context: Optional[MarketContext] = None,
) -> List[PatternFound]:
    regular_params = dict(previous=previous, current=current)

    for comparator in comparators:
        response: ComparatorResponse = comparator(
            **(
                get_comparator_params(
                    comparator=comparator,
                    regular_params=regular_params,
                    market_context=market_context,
                )
            )
        )
        if response.found:
            yield response.get_details()
