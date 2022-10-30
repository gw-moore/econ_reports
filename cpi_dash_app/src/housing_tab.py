"""Dash object for the home page."""

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, dash_table, dcc, html

from econ_reports_utils.pandas import (
    calc_groupby_pct_chg,
    calc_pct_chg_for_latest_obv,
    display_pct_chg_df,
    get_dates,
    pivot_pct_chg_tbl,
)

from .utils.line_plots import _mk_line_plot
from .utils.prep_data import _get_data

series_column_name = "cpi_series"
series = [
    "Owners' equivalent rent of residences",
    "Rent of primary residence",
]

long_df, wide_df = _get_data(series)

mtm_pct_chg_df = calc_groupby_pct_chg(df=long_df, by=series_column_name, periods=1).dropna()
yty_pct_chg_df = calc_groupby_pct_chg(df=long_df, by=series_column_name, periods=12).dropna()

mtm_pct_chg_pivot_tbl = pivot_pct_chg_tbl(
    df=mtm_pct_chg_df,
    index_col=series_column_name,
    pct_chg_col="pct_chg_value",
)

mtm_line_plot, yty_line_plot = _mk_line_plot(mtm_pct_chg_df, yty_pct_chg_df, category="Housing")

month_over_month_tab_content = dbc.Card(
    dbc.CardBody([dcc.Graph(figure=mtm_line_plot)]),
    class_name="mtm",
)

year_over_year_tab_content = dbc.Card(
    dbc.CardBody([dcc.Graph(figure=yty_line_plot)]),
    class_name="yty",
)

housing_content = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Housing CPI"),
        html.Hr(),
        dcc.Markdown(
            """
            # Percent Change in Housing Prices
            """
        ),
        dbc.Tabs(
            [
                dbc.Tab(year_over_year_tab_content, label="Year-over-Year", id="yty"),
                dbc.Tab(month_over_month_tab_content, label="Month-over-Month", id="mtm"),
            ],
            id="housing_tabs",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)
