from decimal import Decimal
from unittest import mock

import pytest

from kandelero import context
from kandelero.candlestick import Candlestick
from kandelero.context.market_context import Bottom, MarketContext, TimeFrame, Top
from kandelero.patterns import CONTEXT_COMPARATORS, find_patterns
from kandelero.patterns.comparators import ComparatorResponse


@pytest.fixture
def false_comparators():
    return [
        mock.Mock(return_value=ComparatorResponse(found=False, pattern=None))
        for __ in range(10)
    ]


@pytest.fixture
def impossible_value():
    # candlesticks cannot have negative values
    return Decimal("-99999")


@pytest.fixture
def dummy_candlestick(impossible_value):
    return Candlestick(
        high=impossible_value,
        low=impossible_value,
        open=impossible_value,
        close=impossible_value,
        timestamp="2021-11-18T17:00:00",
    )


@pytest.fixture
def tops():
    return [
        Top(
            value=1.13737,
            value_range=(),
            timeframe=TimeFrame.TEN_MINUTES,
            candlestick=Candlestick(
                open=1.13695,
                high=1.13737,
                low=1.13673,
                close=1.13685,
                timestamp="2021-11-18T18:00:00",
            ),
        ),
    ]


@pytest.fixture
def bottoms():
    return [
        Bottom(
            value=1.13737,
            value_range=(),
            timeframe=TimeFrame.TEN_MINUTES,
            candlestick=Candlestick(
                open=1.13695,
                high=1.13737,
                low=1.13673,
                close=1.13685,
                timestamp="2021-11-18T18:00:00",
            ),
        ),
    ]


@pytest.fixture
def symbol():
    return "EURUSD"


@pytest.fixture
def market_context(symbol, tops, bottoms):
    return MarketContext(symbol=symbol, tops=tops, bottoms=bottoms)


def test_pattern_finder_no_pattern(dummy_candlestick, market_context):
    current = previous = dummy_candlestick
    result = find_patterns(
        comparators=CONTEXT_COMPARATORS,
        previous=previous,
        current=current,
        market_context=market_context,
    )
    assert list(result) == []


def test_pattern_finder_at_least_one_match(
    false_comparators, dummy_candlestick, market_context
):
    current = previous = dummy_candlestick

    always_true_comparator = mock.Mock(
        return_value=ComparatorResponse(found=True, pattern=None)
    )

    result = find_patterns(
        comparators=[always_true_comparator, *false_comparators],
        previous=previous,
        current=current,
        market_context=market_context,
    )
    result = list(result)
    assert len(result) == 1
