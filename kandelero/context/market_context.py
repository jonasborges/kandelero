from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import List

from kandelero import Candlestick


class TimeFrame(Enum):
    ONE_MINUTE = 1
    FIVE_MINUTES = 5
    TEN_MINUTES = 10
    FIFTEEN_MINUTES = 15
    ONE_HOUR = 60
    FOUR_HOURS = ONE_HOUR * 4
    ONE_DAY = ONE_HOUR * 24
    ONE_WEEK = ONE_DAY * 7


@dataclass
class Top:
    value: Decimal  # ideal value
    value_range: List[Decimal]  # acceptable range
    timeframe: TimeFrame
    candlestick: Candlestick


@dataclass
class Bottom:
    value: Decimal  # ideal value
    value_range: List[Decimal]  # acceptable range
    timeframe: TimeFrame
    candlestick: Candlestick


class MarketContext:
    def __init__(
        self,
        tops: List[Top] = None,
        bottoms: List[Bottom] = None,
    ):
        self.tops = tops
        self.bottoms = bottoms

    def get_tops(self):
        return self.tops or [
            # EURUSD - FIFTEEN_MINUTES
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

    def get_bottoms(self):
        return self.bottoms or [
            # EURGBP - ONE_MINUTE
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
        ]
