from decimal import Decimal
from unittest import mock

import pytest

from kandelero.candlestick import Candlestick
from kandelero.patterns import COMPARATORS, find_patterns


@pytest.fixture
def false_comparators():
    return [mock.Mock(return_value=False) for __ in range(10)]


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
    )


def test_pattern_finder_no_pattern(dummy_candlestick):
    current = previous = dummy_candlestick
    result = find_patterns(comparators=COMPARATORS, previous=previous, current=current)
    assert result == []


def test_pattern_finder_at_least_one_match(false_comparators, dummy_candlestick):
    current = previous = dummy_candlestick

    always_true_comparator = mock.Mock(return_value=True)

    result = find_patterns(
        comparators=[always_true_comparator, *false_comparators],
        previous=previous,
        current=current,
    )
    assert len(result) == 1
    assert result[0] == always_true_comparator
