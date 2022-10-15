import datetime
from dataclasses import dataclass
from typing import List

import pandas as pd
from dateutil.relativedelta import relativedelta
from IPython.display import display


@dataclass
class Date:
    min: datetime.date
    max: datetime.date


def get_dates(df: pd.DataFrame, date_col: str = "date") -> Date:
    """Get minimum and date from pandas date column

    Parameters
    ----------
    df : pd.DataFrame
        Pandas dataframe.
    date_col : str, optional
        Date column. Defaults to "date"

    Returns
    -------
    Date class. The date class as the attributes min_date & max_date.
    Both are datetime.date.
    """
    min_date = df[[date_col]].min().date.date()
    max_date = df[[date_col]].max().date.date()

    return Date(min=min_date, max=max_date)


def calc_pct_chg(
    wide_df: pd.DataFrame,
    lags: List[int],
    max_date: datetime.date,
    grp_var: str,
    lag_var: str,
) -> pd.DataFrame:
    """Calculate percent change on a wide pandas dataframe.

    Parameters
    ----------
    wide_df : pd.DataFrame
        A wide pandas dataframe.
    lags : List[int]
        The lags on which to calculate percent change.
    max_date : datetime.date
        The max date on the wide_df.
    grp_var : str
        Name to give the group column when the wide dataframe is pivoted.
    lag_var : str
        Name to give the lag column.

    Returns
    -------
    Pandas dataframe pivot table.
    """
    pct_chg_dfs = []

    for lag in lags:
        pct_chg_df = round(wide_df.pct_change(lag).iloc[[-1]], 4)
        comparison_month = max_date - relativedelta(months=lag)
        pct_chg_df["Date"] = comparison_month.strftime("%b %Y")
        pct_chg_df[lag_var] = lag
        pct_chg_dfs.append(pct_chg_df)

    pct_chg_df = pd.concat(pct_chg_dfs)

    pct_chg_pivot = pd.pivot_table(
        pct_chg_df.melt(
            id_vars=["Date", lag_var], var_name=grp_var, value_name="pct_chg"
        ),
        index=grp_var,
        values="pct_chg",
        columns=["Date", lag_var],
        sort=False,
    )

    return pct_chg_pivot


def display_pct_chg_df(df: pd.DataFrame, title: str) -> None:
    """Applies formatting and title to table and displays.

    Designed to used along with the `calc_pct_chg` function.

    Parameters
    ----------
    df : pd.DataFrame
        Pandas dataframe.
    title : str
        Table title.
    max_date : datetime.date

    Returns
    -------
    None
    """
    display(
        df.style.format("{:.2%}")
        .set_caption(f"{title}")
        .set_table_styles(
            [
                {
                    "selector": "caption",
                    "props": [
                        ("font-size", "18px"),
                        ("font-weight", "bold"),
                        ("text-align", "center"),
                    ],
                }
            ]
        )
    )


def calc_month_to_month_pct_chg(wide_df, grp_var: str, max_date):
    """Calculates the month-to-month percent changes for the previous 12-months.

    Parameters
    ----------
    """
    rng = list(range(12))
    rng.reverse()
    dates = [max_date - relativedelta(months=i) for i in rng]

    pct_chg_dfs = []
    for dt in dates:
        df = wide_df.loc[: str(dt)]

        df = round(df.pct_change(1).iloc[[-1]], 4)
        df["Date"] = dt.strftime("%b %Y")
        pct_chg_dfs.append(df)

    pct_chg_df = pd.concat(pct_chg_dfs)

    pct_chg_pivot = pd.pivot_table(
        pct_chg_df.melt(id_vars=["Date"], var_name=grp_var, value_name="pct_chg"),
        index=grp_var,
        values="pct_chg",
        columns=["Date"],
        sort=False,
    )

    return pct_chg_pivot


def walkback_to_nearest_date(df, date) -> str:
    """Take a pandas dataframe and returns the date on of before the given date."""
    date_list = [date.to_pydatetime() for date in df.date.tolist()]
    wb_dict = {(date - df_date).days: df_date for df_date in date_list}
    nearest_date = wb_dict[min([days for days in wb_dict.keys() if int(days) > 0])]
    return str(nearest_date.date())
