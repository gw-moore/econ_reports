# Economics Reports with pyfredapi and jupyter

This repo contains a set of economics reports stored as jupyter notebooks. The notebooks use [pyfredapi](https://github.com/gw-moore/pyfredapi) and pull economic data from the FRED API web service. The reports include interactive graphs make with [plotly](https://plotly.com/python/) and tabular views of [pandas](https://pandas.pydata.org/) dataframes.

## Available reports

- Inflation - reports the change in prices overtime

## Setup

1. Install a version of python with [pyenv](https://github.com/pyenv/pyenv)
2. Install [poetry](https://python-poetry.org/)
3. Clone the repo
3. Run `poetry install`
4. Run `poetry shell`

## How-to

The reports can be generated with a `make report` command. The make command will execute the notebook with [papermill](https://papermill.readthedocs.io/en/latest/) and then use [nbconvert](https://nbconvert.readthedocs.io/en/latest/) to convert the notebook into an html file.

Use the example command below to generate a report. You can view the html report by opening the html file at `/output/html/{report}_{run_date}.html`, or the jupyter notebook at `/output/notebooks/{report}_{run_date}.ipynb`

```bash
make report report={name_of_report}
```


## Setup for development

1. Make a fork of the repo
2. Clone your repo to your machine
3. Install the development dependencies with `poetry install --with dev`
4. Setup pre-commit hooks by running `pre-commit install`
