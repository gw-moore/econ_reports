# Economics Reports with pyfredapi and jupyter

This repo contains a set of economics reports stored as jupyter notebooks. The notebooks use [pyfredapi](https://github.com/gw-moore/pyfredapi) and pull economic data from the FRED API web service. The reports include interactive graphs make with [plotly](https://plotly.com/python/) and tabular views of [pandas](https://pandas.pydata.org/) dataframes.

## Available reports

- Inflation - reports the change in prices overtime

## Setup

1. Install a version of python with [pyenv](https://github.com/pyenv/pyenv)
2. Install [poetry](https://python-poetry.org/)
3. Run `poetry install`
4. Run `poetry shell`

## How-to

The reports can be generated with a `make report` command. The make command will execute the notebook with [papermill](https://papermill.readthedocs.io/en/latest/) and then use `nbconvert` to convert the notebook into an html file for

 can run via [papermill](https://papermill.readthedocs.io/en/latest/) and converted into

1. Generate a report using the Makefile: `make report report={name_of_report}`
2. View the report by opening the html file at: `/output/html/{report}_{run_date}.html`
