# Sales Data Analyzer (Python)

Reads a sales CSV and prints a text report with revenue by product, region and month.

## Features
- CSV parsing with malformed-row handling
- Revenue totals, grouped summaries, monthly trend
- Mean / median / max order value
- ASCII bar charts in the terminal
- Includes a sample dataset (`sales.csv`)

## Run
```
python analyzer.py            # uses sales.csv
python analyzer.py my_data.csv
```

## Tests
```
python -m unittest discover tests
```

## Tech
Python 3 standard library only (csv, statistics, collections).
