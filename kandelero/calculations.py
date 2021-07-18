import math
from decimal import Decimal, DivisionByZero, DivisionUndefined, InvalidOperation
from functools import wraps

DECIMAL_PLACES = 4
ZERO = Decimal(0)
MIN_VALUE = Decimal("0.0001")
MAX_VALUE = Decimal("9999999999")


def round_up(number: Decimal, decimal_places: int = DECIMAL_PLACES) -> Decimal:
    factor = 10 ** decimal_places
    result = safe_div(dividend=math.ceil(number * factor), divisor=factor)
    return Decimal(result).quantize(Decimal(10) ** -DECIMAL_PLACES)


def round_down(number: Decimal, decimal_places: int = DECIMAL_PLACES) -> Decimal:
    factor = 10 ** decimal_places
    result = safe_div(dividend=math.floor(number * factor), divisor=factor)
    return Decimal(result).quantize(Decimal(10) ** -DECIMAL_PLACES)


def handle_division_by_zero(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (DivisionByZero, DivisionUndefined, InvalidOperation):
            return ZERO

    return wrapper


@handle_division_by_zero
def safe_div(dividend, divisor):
    return dividend / divisor
