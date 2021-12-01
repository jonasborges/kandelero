import pytest

from kandelero.patterns import comparators
from kandelero.patterns.names import get_pattern_name


@pytest.mark.parametrize(
    "comparator, expected_name",
    (
        (comparators.is_bearish_engulfing, "Bearish Engulfing"),
        (comparators.is_bearish_harami, "Bearish Harami"),
        (comparators.is_bearish_kicker, "Bearish Kicker"),
        (comparators.is_bullish_engulfing, "Bullish Engulfing"),
        (comparators.is_bullish_harami, "Bullish Harami"),
        (comparators.is_bullish_kicker, "Bullish Kicker"),
        (comparators.is_hammer, "Hammer"),
        (comparators.is_inverted_hammer, "Inverted Hammer"),
        (comparators.is_doji, "Doji"),
        (comparators.is_bullish_harami_cross, "Bullish Harami Cross"),
        (comparators.is_bearish_harami_cross, "Bearish Harami Cross"),
        (comparators.is_hanging_man, "Hanging Man"),
        (comparators.is_shooting_star, "Shooting Star"),
        (comparators.is_piercing_line, "Piercing Line"),
        (comparators.is_dark_cloud_cover, "Dark Cloud Cover"),
        (comparators.is_bear_trap, "Bear Trap"),
        (comparators.is_bull_trap, "Bull Trap"),
    ),
)
def test_get_pattern_name(comparator, expected_name):
    assert get_pattern_name(comparator) == expected_name
