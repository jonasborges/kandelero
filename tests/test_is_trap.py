import pytest

from kandelero import Candlestick
from kandelero.context import Bottom, MarketContext, TimeFrame, Top
from kandelero.patterns.comparators import is_bear_trap, is_bull_trap


def bottoms():
    return


def test_is_bull_trap():

    # EURUSD - FIFTEEN_MINUTES
    previous = Candlestick(
        open=1.13737,
        high=1.13825,
        low=1.13730,
        close=1.13781,
        timestamp="2021-11-30T14:45:00",
    )
    current = Candlestick(
        open=1.13778,
        high=1.13825,
        low=1.13658,
        close=1.13722,
        timestamp="2021-11-30T15:00:00",
    )

    market_context = MarketContext(
        tops=[
            Top(
                value=1.13737,
                value_range=(),
                timeframe=TimeFrame.FIFTEEN_MINUTES,
                candlestick=Candlestick(
                    open=1.13695,
                    high=1.13737,
                    low=1.13673,
                    close=1.13685,
                    timestamp="2021-11-18T18:00:00",
                ),
            ),
        ],
        bottoms=[],
    )

    assert is_bull_trap(
        previous=previous, current=current, market_context=market_context
    )


def test_is_bear_trap():

    # EURGBP - ONE_MINUTE
    previous = Candlestick(
        open=0.84984,
        high=0.84987,
        low=0.84979,
        close=0.84982,
        timestamp="2021-12-01T07:40:00",
    )
    current = Candlestick(
        open=0.84982,
        high=0.84990,
        low=0.84981,
        close=0.84987,
        timestamp="2021-12-01T07:41:00",
    )

    market_context = MarketContext(
        tops=[],
        bottoms=[
            Bottom(
                value=0.84981,
                value_range=(),
                timeframe=TimeFrame.FIFTEEN_MINUTES,
                candlestick=Candlestick(
                    open=0.84992,
                    high=0.85112,
                    low=0.84981,
                    close=0.85109,
                    timestamp="2021-11-30T10:30:00",
                ),
            ),
        ],
    )

    assert is_bear_trap(
        previous=previous, current=current, market_context=market_context
    )
