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
                open=Decimal("14501.5500"),
                high=Decimal("14517.1500"),
                low=Decimal("14492.1500"),
                close=Decimal("14517.1500"),
            ),
            Candlestick(
                open=Decimal("14513.9500"),
                high=Decimal("14516.9500"),
                low=Decimal("14507.4500"),
                close=Decimal("14512.9500"),
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
                open=Decimal("14498.2500"),
                high=Decimal("14499.5500"),
                low=Decimal("14487.0500"),
                close=Decimal("14490.3500"),
            ),
            Candlestick(
                open=Decimal("14491.0500"),
                high=Decimal("14496.8500"),
                low=Decimal("14485.2500"),
                close=Decimal("14491.4500"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("14503.1500"),
                high=Decimal("14503.8500"),
                low=Decimal("14493.9500"),
                close=Decimal("14495.3500"),
            ),
            Candlestick(
                open=Decimal("14497.4500"),
                high=Decimal("14506.4500"),
                low=Decimal("14496.3500"),
                close=Decimal("14499.4500"),
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
                open=Decimal("14676.7500"),
                high=Decimal("14680.1500"),
                low=Decimal("14673.1500"),
                close=Decimal("14673.8500"),
            ),
            Candlestick(
                open=Decimal("14673.8500"),
                high=Decimal("14675.2500"),
                low=Decimal("14667.3500"),
                close=Decimal("14673.8500"),
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
                open=Decimal("14552.1500"),
                high=Decimal("14576.2500"),
                low=Decimal("14552.1500"),
                close=Decimal("14574.1500"),
            ),
            # that's doji (neither bullish nor bearish by itself)
            # but it will have a bearish connotation in this context
            Candlestick(
                open=Decimal("14570.4500"),
                high=Decimal("14576.2500"),
                low=Decimal("14559.4500"),
                close=Decimal("14570.4500"),
            ),
        ],
        [
            Candlestick(
                open=Decimal("14747.0500"),
                high=Decimal("14750.7500"),
                low=Decimal("14746.5500"),
                close=Decimal("14750.7500"),
            ),
            Candlestick(  # this one is perfect
                open=Decimal("14750.5500"),
                high=Decimal("14751.8500"),
                low=Decimal("14749.0500"),
                close=Decimal("14750.5500"),
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
