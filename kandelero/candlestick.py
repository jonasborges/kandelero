from dataclasses import dataclass
from decimal import Decimal

TWOPLACES = Decimal(10) ** -2
ZERO = Decimal(0)


@dataclass(frozen=True)
class Candlestick:
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal

    @property
    def full_len(self) -> Decimal:
        return self.high - self.low

    @property
    def body_len(self) -> Decimal:
        return abs(self.open - self.close)

    @property
    def wick_len(self) -> Decimal:
        return self.high - max(self.open, self.close)

    @property
    def tail_len(self) -> Decimal:
        return min(self.open, self.close) - self.low

    @property
    def is_bullish(self) -> bool:
        return self.open < self.close

    @property
    def is_bearish(self) -> bool:
        return self.open > self.close

    @property
    def is_valid_candle(self):
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

    @staticmethod
    def quantize(value: Decimal, places=TWOPLACES):
        return value.quantize(places)

    @property
    def body_proportion(self):
        if self.full_len == ZERO:
            return ZERO
        return self.quantize(Decimal(self.body_len / self.full_len))

    @property
    def wick_proportion(self):
        if self.full_len == ZERO:
            return ZERO
        return self.quantize(Decimal(self.wick_len / self.full_len))

    @property
    def tail_proportion(self):
        if self.full_len == ZERO:
            return ZERO
        return self.quantize(Decimal(self.tail_len / self.full_len))
