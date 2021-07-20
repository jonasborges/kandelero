from dataclasses import dataclass
from decimal import Decimal
from itertools import cycle

from .calculations import MIN_VALUE, ZERO, round_down, safe_div


class Candlestick:
    def __init__(
        self,
        open: Decimal,
        high: Decimal,
        low: Decimal,
        close: Decimal,
    ):
        self.open = round_down(Decimal(open))
        self.high = round_down(Decimal(high))
        self.low = round_down(Decimal(low))
        self.close = round_down(Decimal(close))

        self._body_proportion = round_down(
            safe_div(dividend=self.body_len, divisor=self.full_len)
        )
        self._wick_proportion = round_down(
            safe_div(dividend=self.wick_len, divisor=self.full_len)
        )
        self._tail_proportion = round_down(
            safe_div(dividend=self.tail_len, divisor=self.full_len)
        )

        sum_parts = (
            self._body_proportion + self._wick_proportion + self._tail_proportion
        )

        if sum_parts > ZERO:
            diff = Decimal(1) - sum_parts

            parts = cycle(
                (
                    "_body_proportion",
                    "_wick_proportion",
                    "_tail_proportion",
                )
            )

            step = MIN_VALUE
            while diff > ZERO:
                part_name = next(parts)
                current_value = getattr(self, part_name)

                if current_value == ZERO:
                    # do not increase a part that is non existent
                    # for example: candle with
                    # no tail body_proportion = 0.02, wick_proportion=0.96
                    continue

                current_value += step
                setattr(self, part_name, current_value)
                diff -= step

    @property
    def full_len(self) -> Decimal:
        return self.high - self.low

    @property
    def body_len(self) -> Decimal:
        return round_down(abs(self.open - self.close))

    @property
    def wick_len(self) -> Decimal:
        return round_down(self.high - max(self.open, self.close))

    @property
    def tail_len(self) -> Decimal:
        return round_down(min(self.open, self.close) - self.low)

    @property
    def is_bullish(self) -> bool:
        return self.open < self.close

    @property
    def is_bearish(self) -> bool:
        return self.open > self.close

    @property
    def is_valid_candle(self) -> bool:
        low_is_lowest = min((self.open, self.high, self.low, self.close)) == self.low
        high_is_highest = max((self.open, self.high, self.low, self.close)) == self.high

        positive_proportions = all(
            v >= ZERO
            for v in (
                self.body_proportion,
                self.wick_proportion,
                self.tail_proportion,
            )
        )

        # flat candles will have proportion == ZERO
        correct_proportions = (
            sum(
                (
                    self.body_proportion,
                    self.wick_proportion,
                    self.tail_proportion,
                )
            )
            in (ZERO, Decimal(1))
        )

        positive_lengths = all(
            v >= ZERO
            for v in (
                self.full_len,
                self.body_len,
                self.wick_len,
                self.tail_len,
            )
        )
        return (
            low_is_lowest
            and high_is_highest
            and positive_proportions
            and positive_lengths
            and correct_proportions
        )

    @property
    def body_proportion(self) -> Decimal:
        return self._body_proportion

    @property
    def wick_proportion(self) -> Decimal:
        return self._wick_proportion

    @property
    def tail_proportion(self) -> Decimal:
        return self._tail_proportion

    @property
    def middle_point(self):
        """Exact value between open and close"""
        distance_from_middle = self.body_len / 2

        if self.is_bearish:
            return self.close + distance_from_middle
        elif self.is_bullish:
            return self.open + distance_from_middle
