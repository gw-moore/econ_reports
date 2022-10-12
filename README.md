# Economics Reports with pyfredapi and jupyter

This repo contains a set of economics reports stored as jupyter notebooks. The notebooks use [pyfredapi](https://github.com/gw-moore/pyfredapi) and pull economic data from the FRED API web service. The notebook can run via [papermill](https://papermill.readthedocs.io/en/latest/).

## Available reports

- Inflation - reports the change in prices overtime

## How-to

The reports can be generate via command-line with the command `generate_report`.

```bash
papermill econ_report/report/inflation_report.ipynb inflation_report.ipynb
```
