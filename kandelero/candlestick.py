from dataclasses import dataclass
from decimal import Decimal, getcontext

getcontext().prec = 50


@dataclass()
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
