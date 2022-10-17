import datetime
from dataclasses import dataclass
from typing import List, Union

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


def calc_pct_chg_vs_latest_obv(
    wide_df: pd.DataFrame,
    lags: List[int],
    max_date: datetime.date,
    grp_var: str,
    lag_var: str,
) -> pd.DataFrame:
    """Calculate percent change on a wide pandas dataframe.

    Calculates the percent change of the latest observation in the dataframe with the given lags.

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

    Designed to used with the `pivot_pct_chg_tbl` function.

    Parameters
    ----------
    df : pd.DataFrame
        Pandas dataframe.
    title : str
        Table title.

    Returns
    -------
    None
    """
    display(
        df.style.format("{:.1%}")
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


def calc_groupby_pct_chg(
    df: pd.DataFrame,
    grp_column: Union[str, List[str]],
    periods: int = 1,
    column: str = "value",
) -> pd.DataFrame:
    """Calculate a group by percent change.

    Parameters
    ----------
    df : pd.DataFrame
        A long pandas dataframe.
    grp_column :
        Columns to group by.
    periods : int
        Periods to shift for forming percent change.
    column : str
        Column to calculate percent change on.

    Return
    -------
    pd.DataFrame
    """
    pct_chg_df = df.copy()
    pct_chg_df[f"pct_chg_{column}"] = (
        pct_chg_df.groupby(grp_column, sort=False, group_keys=True)[column]
        .apply(lambda x: x.pct_change(periods))
        .to_numpy()
    )

    return pct_chg_df.dropna()


def pivot_pct_chg_tbl(
    df: pd.DataFrame,
    index_column: str,
    pct_chg_column: str = "pct_chg_value",
) -> pd.DataFrame:
    """Pivot a percent change dataframe. Designed to work with the `calc_groupby_pct_chg` and
    `calc_pct_chg_vs_latest_obv` functions.

    Parameters
    ----------
    df : pd.DataFrame
        Pandas dataframe.
    index_column : str
        Column to make the index.
    pct_chg_column : str
        Name of the percent change column.

    Returns
    -------
    Pandas pivot table.
    """
    pv_df = df.copy()
    pv_df["Date"] = pv_df.date.dt.strftime("%b %Y")
    pv_dates = pv_df["Date"].tail(6).tolist()
    pv_df = pv_df.loc[pv_df["Date"].isin(pv_dates)]

    pivot_table = pd.pivot_table(
        pv_df,
        index=index_column,
        values=pct_chg_column,
        columns=["Date"],
        sort=False,
    )
    pivot_table.index.name = index_column.replace("_", " ").title()

    return pivot_table


def walkback_to_nearest_date(df, date) -> str:
    """Take a pandas dataframe and returns the date on of before the given date."""
    date_list = [date.to_pydatetime() for date in df.date.tolist()]
    wb_dict = {(date - df_date).days: df_date for df_date in date_list}
    nearest_date = wb_dict[min([days for days in wb_dict.keys() if int(days) > 0])]
    return str(nearest_date.date())
