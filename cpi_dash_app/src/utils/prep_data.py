"""Routinue data prep used in each tab of the report
"""

from pathlib import Path
from typing import List, Union

import pandas as pd

path = Path(".") / "cpi_dash_app" / "src" / "data" / "cpi"
path = str(path.resolve())
series_column_name = "cpi_series"


def _get_data(series: Union[List[str], None] = None):
    """Read data from the .csv files."""
    long_df = pd.read_csv(f"{path}/long_df.csv", parse_dates=["date"])
    wide_df = pd.read_csv(f"{path}/wide_df.csv", parse_dates=["date"])

    if series:
        long_df = long_df[long_df["cpi_series"].isin(series)]

    return long_df, wide_df
