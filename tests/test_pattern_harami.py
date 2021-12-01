from decimal import Decimal

import pytest

from kandelero import Candlestick
from kandelero.patterns.comparators import (
    is_bearish_harami,
    is_bearish_harami_cross,
    is_bullish_harami,
    is_bullish_harami_cross,
)


@pytest.mark.bearish_pattern
@pytest.mark.happy_path
@pytest.mark.parametrize(
    "previous, current",
    (
        [
            Candlestick(
                open=Decimal("14501.55000"),
                high=Decimal("14517.15000"),
                low=Decimal("14492.15000"),
                close=Decimal("14517.15000"),
            ),
            Candlestick(
                open=Decimal("14513.95000"),
                high=Decimal("14516.95000"),
                low=Decimal("14507.45000"),
                close=Decimal("14512.95000"),
            ),
        ],
    ),
    ids=[
        "Nasdaq 1 Minute: 2021-07-19 15:28 -> 15:29",
    ],
)
def test_is_bearish_harami(previous, current):
    assert previous.is_bullish
    assert current.is_bearish
    assert is_bearish_harami(previous, current)


@pytest.mark.bullish_pattern
@pytest.mark.happy_path
@pytest.mark.parametrize(
    "previous, current",
    (
        [
            Candlestick(
                open=Decimal("14498.25000"),
                high=Decimal("14499.55000"),
                low=Decimal("14487.05000"),
                close=Decimal("14490.35000"),
            ),
            Candlestick(
                open=Decimal("14491.05000"),
                high=Decimal("14496.85000"),
                low=Decimal("14485.25000"),
                close=Decimal("14491.45000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("14503.15000"),
                high=Decimal("14503.85000"),
                low=Decimal("14493.95000"),
                close=Decimal("14495.35000"),
            ),
            Candlestick(
                open=Decimal("14497.45000"),
                high=Decimal("14506.45000"),
                low=Decimal("14496.35000"),
                close=Decimal("14499.45000"),
            ),
        ],
    ),
    ids=[
        "Nasdaq 1 Minute: 2021-07-19 19:59 -> 20:00",
        "Nasdaq 1 Minute: 2021-07-19 20:49 -> 20:50",
    ],
)
def test_is_bullish_harami(previous, current):
    assert previous.is_bearish
    assert current.is_bullish
    result = is_bullish_harami(previous, current)
    assert result


@pytest.mark.bullish_pattern
@pytest.mark.happy_path
@pytest.mark.parametrize(
    "previous, current",
    (
        [
            Candlestick(
                open=Decimal("14676.75000"),
                high=Decimal("14680.15000"),
                low=Decimal("14673.15000"),
                close=Decimal("14673.85000"),
            ),
            Candlestick(
                open=Decimal("14673.85000"),
                high=Decimal("14675.25000"),
                low=Decimal("14667.35000"),
                close=Decimal("14673.85000"),
            ),
        ],
    ),
    ids=[
        "Nasdaq 1 Minute: 2021-07-20 16:31 -> 16:32",
    ],
)
def test_is_bullish_harami_cross(previous, current):
    assert previous.is_bearish
    assert not current.is_bearish and not current.is_bullish
    assert is_bullish_harami_cross(previous, current)


@pytest.mark.bearish_pattern
@pytest.mark.happy_path
@pytest.mark.parametrize(
    "previous, current",
    (
        [
            Candlestick(
                open=Decimal("14552.15000"),
                high=Decimal("14576.25000"),
                low=Decimal("14552.15000"),
                close=Decimal("14574.15000"),
            ),
            # that's doji (neither bullish nor bearish by itself)
            # but it will have a bearish connotation in this context
            Candlestick(
                open=Decimal("14570.45000"),
                high=Decimal("14576.25000"),
                low=Decimal("14559.45000"),
                close=Decimal("14570.45000"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("14747.05000"),
                high=Decimal("14750.75000"),
                low=Decimal("14746.55000"),
                close=Decimal("14750.75000"),
            ),
            Candlestick(  # this one is perfect
                open=Decimal("14750.55000"),
                high=Decimal("14751.85000"),
                low=Decimal("14749.05000"),
                close=Decimal("14750.55000"),
            ),
        ],
    ),
    ids=[
        "Nasdaq 1 Minute: 2021-07-19 14:44 -> 14:45",
        "Nasdaq 1 Minute: 2021-07-20 17:58 -> 17:59",
    ],
)
def test_is_bearish_harami_cross(previous, current):
    assert previous.is_bullish
    assert not current.is_bearish and not current.is_bullish
    assert is_bearish_harami_cross(previous, current)
