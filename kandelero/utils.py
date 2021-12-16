import os
from datetime import datetime
from typing import Union

import pandas as pd


def parse_date(value: Union[str, datetime, None]) -> Union[datetime, None]:
    if isinstance(value, datetime):
        return value
    elif isinstance(value, str):
        return datetime.fromisoformat(value)
    elif value is None:
        return None
    else:
        raise ValueError(f"Impossible to parse date from value: {value}")


def get_filename(symbol: str, timeframe: str):
    BASE_DIR = os.getenv("DATADIR")
    filename = f"{symbol}-{timeframe}.csv"
    return os.path.join(BASE_DIR, filename)


def get_df(
    symbol: str, timeframe: str, date_filter: Union[datetime, str, None] = None
) -> pd.DataFrame:
    df = pd.read_csv(get_filename(symbol=symbol, timeframe=timeframe))

    if date_filter:
        date = parse_date(date_filter)
        df.date = pd.to_datetime(df.date)
        df = df[df.date >= date]

    return df
