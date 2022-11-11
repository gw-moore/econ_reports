import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
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

long_df, wide_df = _get_data()
dates = get_dates(long_df, "date")
series_column_name = "cpi_series"

mtm_pct_chg_df = calc_groupby_pct_chg(df=long_df, by=series_column_name, periods=1).dropna()
yty_pct_chg_df = calc_groupby_pct_chg(df=long_df, by=series_column_name, periods=12).dropna()

mtm_bp_df = mtm_pct_chg_df.groupby(series_column_name).tail(1).copy()
mtm_bp_df["group"] = "1 Month Percent Change"

yty_bp_df = yty_pct_chg_df.groupby(series_column_name).tail(1).copy()
yty_bp_df["group"] = "12 Month Percent Change"

bar_plot_df = pd.concat([mtm_bp_df, yty_bp_df])

bar_plot = px.bar(
    data_frame=bar_plot_df,
    x=series_column_name,
    color="group",
    y="pct_chg_value",
    hover_data={"pct_chg_value": ":.2%"},
    barmode="group",
    color_discrete_sequence=px.colors.qualitative.Safe,
    labels=dict(
        cpi_category="CPI Category",
        group="Months Ago",
        pct_chg_value="Percent Change",
        date="Date",
    ),
)
bar_plot.layout.yaxis.tickformat = ",.0%"
bar_plot.update_layout(
    title_text=f"1 & 12 Month Percent Change, Consumer Price Index for All Urban Consumers, {dates.max}",
)

line_plot = px.line(
    data_frame=long_df,
    x="date",
    y="value",
    color=series_column_name,
    title=f"Consumer Price Index for All Urban Consumers, {dates.min} - {dates.max}",
    labels=dict(cpi_category="CPI Category", value="CPI", date="Date"),
    color_discrete_sequence=px.colors.qualitative.Safe,
)

overview_content = dbc.Container(
    [
        html.H1("CPI Summary"),
        html.Hr(),
        html.H3(f"Latest CPI Data: {dates.max}"),
        html.H2(f"Headline Inflation: {12}%"),
        html.H2(f"Core Inflation: {12}%"),
        html.Br(),
        dcc.Markdown(
            """
            # Percent Change - 1 & 12 Month
            """
        ),
        dcc.Graph(id="barplot", figure=bar_plot),
        dcc.Graph(id="lineplot", figure=line_plot),
    ]
)
