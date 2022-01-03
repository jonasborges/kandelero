from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Tuple, Union

import pandas as pd

from kandelero import Candlestick
from kandelero.utils import get_df


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
class PriceLevel:
    value: Decimal  # ideal value
    value_range: List[Decimal]  # acceptable range
    timeframe: TimeFrame
    candlestick: Candlestick
    hit_count: int = 1

    def __post_init__(self):
        self._links: List[PriceLevel] = []
        self._first_occurence = None

    def link_new_occurence(self, new_occurence: "PriceLevel"):
        self._links.append(new_occurence)
        self.hit_count += 1

        new_occurence._first_occurence = self

    def get_hit_count(self, since_beginning: bool = True):

        if since_beginning:
            # when we are checking the last occurence of a price level its
            # hit count will be always=1. We must looking back in time get
            # the hit_count from the first_occurence of that PriceLevel
            # which is the one that had it hit_count being increase since
            # the beginning.
            if self._first_occurence:
                return self._first_occurence.hit_count

        return self.hit_count

    def is_contained_in(self, other: "PriceLevel"):
        if other.timeframe == TimeFrame.ONE_WEEK:
            max_date = other.candlestick.timestamp + timedelta(days=6)
            if other.candlestick.timestamp <= self.candlestick.timestamp <= max_date:
                return True
        else:
            return False


class Top(PriceLevel):
    pass


class Bottom(PriceLevel):
    pass


timeframes = [
    "OneWeek",
    "OneDay",
    "OneHour",
    "FifteenMinutes",
    "FiveMinutes",
    "OneMinute",
]


class MarketContext:
    def __init__(
        self,
        symbol: str,
        tops: List[Top] = None,
        bottoms: List[Bottom] = None,
        date_filter: Union[datetime, str, None] = None,
        df_set: Dict[str, pd.DataFrame] = None,
        load_df=False,
        find_price_levels=False,
    ):
        df_set = df_set or []
        self.df_set = df_set
        if load_df:
            self.df_set = df_set or {
                tf: get_df(symbol=symbol, timeframe=tf, date_filter=date_filter)
                for tf in timeframes
            }

        self._tops = {}
        self._bottoms = {}

        # tops/bottoms, MUST be sorted by candlestick.timestamp ASC
        # otherwise first time occurences that we identify will be wrong.
        tops = sorted(tops or [], key=self.price_level_sortkey)
        bottoms = sorted(bottoms or [], key=self.price_level_sortkey)

        for top in tops:
            self.add_new_price_level(top)
        for bottom in bottoms:
            self.add_new_price_level(bottom)

        if find_price_levels and (not tops and not bottoms):
            self.find_price_levels()

    @staticmethod
    def price_level_sortkey(price_level: PriceLevel):
        return price_level.candlestick.timestamp

    def get_candles(
        self, timeframe: str, date_filter: Union[datetime, str, None] = None
    ) -> List[Candlestick]:
        df = self.df_set[timeframe]
        if date_filter:
            df = df[df.date >= date_filter]
        for __, candle_row in df.iterrows():
            yield Candlestick(
                open=candle_row.open,
                high=candle_row.high,
                low=candle_row.low,
                close=candle_row.close,
                timestamp=candle_row.date,
            )

    def get_candles_for_pattern_matching(
        self, timeframe: str, date_filter: Union[datetime, str, None] = None
    ) -> Tuple[Candlestick]:
        candles = []

        for candle in self.get_candles(timeframe=timeframe, date_filter=date_filter):
            if len(candles) == 0:
                candles.append(candle)
                continue
            elif len(candles) == 1:
                candles.append(candle)
            elif len(candles) == 2:
                candles.append(candle)
                candles.pop(0)

            previous, current = candles
            yield previous, current

    def get_tops(self, before_date: datetime):
        # avoid retrieving price levels in the future
        return [t for t in self._tops.values() if t.candlestick.timestamp < before_date]

    def get_bottoms(self, before_date: datetime):
        # avoid retrieving price levels in the future
        return [
            b for b in self._bottoms.values() if b.candlestick.timestamp < before_date
        ]

    def get_store(self, price_level: PriceLevel) -> dict:
        if isinstance(price_level, Top):
            return self._tops
        elif isinstance(price_level, Bottom):
            return self._bottoms
        else:
            raise ValueError(
                f"Impossible to find MarketContext store for {price_level}"
            )

    def is_duplicate(self, first_occurence: PriceLevel, new_occurence: PriceLevel):
        # check if is exact same price level, but in a different timeframe
        conditions = (
            int(first_occurence.timeframe.value) > int(new_occurence.timeframe.value),
            new_occurence.is_contained_in(first_occurence),
        )
        return all(conditions)

    def add_new_price_level(self, price_level: PriceLevel):
        store = self.get_store(price_level)

        try:
            store[price_level.value]
        except KeyError:
            # new price level, never seen before
            store[price_level.value] = price_level
        else:
            first_occurence = store[price_level.value]
            new_occurence = price_level

            # existing price level, check for duplicate
            # it might be same price level, but different day
            # or even different year.
            if self.is_duplicate(first_occurence, new_occurence):
                return

            # if not duplicate, we'll increase the count for
            # how many times that price level was hit.
            first_occurence.link_new_occurence(new_occurence)

    def find_price_levels(self):
        # ignoring tops on timeframes lower than 15 min.

        timeframes = [
            ("OneWeek", TimeFrame.ONE_WEEK),
            ("OneDay", TimeFrame.ONE_DAY),
        ]

        for tf, enum_tf in timeframes:
            for candle in self.get_candles(timeframe=tf):
                # get highs for every single week and day and assume them as tops

                # timestamp for weekly candles is the beginning of the week,
                # so Bear/Bull trap is triggering patterns with dates in the future,
                # since the last day of the week can set new Top/Bottoms for the week,
                # while the original datetime still in the past
                if tf == "OneWeek":
                    candle.timestamp += timedelta(days=5)
                self.add_new_price_level(
                    Top(
                        value=candle.high,
                        value_range=(),
                        timeframe=enum_tf,
                        candlestick=candle,
                    )
                )
                self.add_new_price_level(
                    Bottom(
                        value=candle.low,
                        value_range=(),
                        timeframe=enum_tf,
                        candlestick=candle,
                    )
                )
