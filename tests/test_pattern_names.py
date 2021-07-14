import pytest

from kandelero.patterns import comparators
from kandelero.patterns.names import get_pattern_name


@pytest.mark.parametrize(
    "comparator, expected_name",
    (
        (comparators.is_bearish_engulfing, "Bearish Engulfing"),
        (comparators.is_bearish_kicker, "Bearish Kicker"),
        (comparators.is_bullish_engulfing, "Bullish Engulfing"),
        (comparators.is_bullish_kicker, "Bullish Kicker"),
    ),
)
def test_get_pattern_name(comparator, expected_name):
    assert get_pattern_name(comparator) == expected_name
