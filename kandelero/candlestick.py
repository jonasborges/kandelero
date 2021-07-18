from dataclasses import dataclass
from decimal import Decimal
from itertools import cycle

from .calculations import ZERO, round_down, safe_div


class Candlestick:
    def __init__(
        self,
        open: Decimal,
        high: Decimal,
        low: Decimal,
        close: Decimal,
    ):
        self.open = Decimal(open)
        self.high = Decimal(high)
        self.low = Decimal(low)
        self.close = Decimal(close)

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

            step = Decimal("0.0001")
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
        low_is_lowest = all(v >= self.low for v in (self.high, self.close, self.open))
        high_is_highest = all(v <= self.high for v in (self.low, self.close, self.open))

        positive_proportions = all(
            v >= ZERO
            for v in (
                self.body_proportion,
                self.wick_proportion,
                self.tail_proportion,
            )
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
