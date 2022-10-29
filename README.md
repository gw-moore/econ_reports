# Economics Reports with pyfredapi and jupyter

This repo contains a set of economics reports stored as jupyter notebooks. The notebooks use [pyfredapi](https://github.com/gw-moore/pyfredapi) and pull economic data from the FRED API web service. The reports include interactive graphs make with [plotly](https://plotly.com/python/) and tabular views of [pandas](https://pandas.pydata.org/) dataframes.

## Available reports

- CPI - reports the change in prices overtime

## Setup for development / contributing

1. Install a version of python with [pyenv](https://github.com/pyenv/pyenv)
2. Install [poetry](https://python-poetry.org/)
3. Fork the repo
4. Clone the forked repo
5. Run `poetry install --with dev`
6. Run `poetry shell`
7. Setup pre-commit hooks by running `pre-commit install`

## How to generate reports

The reports can be generated with a `make report` command. The make command will execute the notebook with [papermill](https://papermill.readthedocs.io/en/latest/) and then use [nbconvert](https://nbconvert.readthedocs.io/en/latest/) to convert the notebook into an html file.

For example, you can generate the cpi report with the make command below.

```bash
make report report=cpi
```

This command run two steps

1. Papermill is used to run `cpi.ipynb` file in the `notebooks/` directory and stores the output notebook at `site/source/notebooks`
2. nbconvert converts the output notebook into an html file and stores the output at `site/source/html`

To view the report, simply open the html file at `site/source/html/cpi_{}.html`

## Guide for building notebooks

- If you want the cell excluded from the html output, add the tag `remove_cell`
- If you want to remove the cell code, but not the output, add the tag `remove_input`
