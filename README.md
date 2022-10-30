# Economics Reports

This repo contains explority demos of creating economic reports and analysis with different tools such as Jupyter notebooks and Dash apps. The demos rely on [pyfredapi](https://github.com/gw-moore/pyfredapi) to pull economic data from the FRED API web service.

## Demos

### CPI dashboard with Dash

The `cpi_dash_app/` folder is a MVP Dash app for Consumer Price Index data.

Launch app:

```bash
python cpi_dash_app/app.py
```

### Jupyter notebook report

The reports can be generated with a `make report` command. The make command will execute the notebook with [papermill](https://papermill.readthedocs.io/en/latest/) and then use [nbconvert](https://nbconvert.readthedocs.io/en/latest/) to convert the notebook into an html file.

For example, you can generate the cpi report with the make command below.

```bash
make report report=cpi
```

This command run two steps

1. Papermill is used to run `cpi.ipynb` file in the `notebooks/` directory and stores the output notebook at `site/source/notebooks`
2. nbconvert converts the output notebook into an html file and stores the output at `site/source/html`

To view the report, simply open the html file at `site/source/html/cpi_{}.html`

#### Guide for building notebooks for this demo

- If you want the cell excluded from the html output, add the tag `remove_cell`
- If you want to remove the cell code, but not the output, add the tag `remove_input`

## Setup for development / contributing

1. Install a version of python with [pyenv](https://github.com/pyenv/pyenv)
2. Install [poetry](https://python-poetry.org/)
3. Fork the repo
4. Clone the forked repo
5. Run `poetry install --with dev`
6. Run `poetry shell`
7. Setup pre-commit hooks by running `pre-commit install`
