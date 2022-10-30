"""Dash object for the home page."""

import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dash_table, dcc, html

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
series = ["All items", "All items less food and energy"]

long_df, wide_df = _get_data(series)

mtm_pct_chg_df = calc_groupby_pct_chg(df=long_df, by=series_column_name, periods=1).dropna()
yty_pct_chg_df = calc_groupby_pct_chg(df=long_df, by=series_column_name, periods=12).dropna()

mtm_pct_chg_pivot_tbl = pivot_pct_chg_tbl(
    df=mtm_pct_chg_df,
    index_col=series_column_name,
    pct_chg_col="pct_chg_value",
)

mtm_line_plot, yty_line_plot = _mk_line_plot(mtm_pct_chg_df, yty_pct_chg_df, category="Core & Headline")


month_over_month_tab_content = dbc.Card(
    dbc.CardBody([dcc.Graph(figure=mtm_line_plot)]),
    class_name="mtm",
)

year_over_year_tab_content = dbc.Card(
    dbc.CardBody([dcc.Graph(figure=yty_line_plot)]),
    class_name="yty",
)

headline_and_core_content = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Core & Headline CPI"),
        html.Hr(),
        dcc.Markdown(
            """
            # Percent Change in Core and Headline Inflation
            """
        ),
        dbc.Tabs(
            [
                dbc.Tab(year_over_year_tab_content, label="Year-over-Year", id="yty"),
                dbc.Tab(month_over_month_tab_content, label="Month-over-Month", id="mtm"),
            ],
            id="headline_and_core_tabs",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)
