"""Top-level package for kandelero."""

__author__ = """Jonas Borges Alves"""
__email__ = "jonasborgesalves@gmail.com"
__version__ = "0.1.0"


from decimal import getcontext

from .candlestick import Candlestick

getcontext().prec = 15
