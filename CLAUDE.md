# Taxes Project

Scripts for calculating taxes from stock dividends and market orders, tailored for Bulgarian tax reporting.

## Project Structure

```
taxes/
├── CLAUDE.md              # This file
├── stocks.py              # Process market orders (buy/sell transactions)
├── dividends.py           # Process dividend income
├── exchange_rates.py      # Currency conversion (BNB API)
├── dividends_data/        # Dividends data
│   ├── dividends.csv      # Input: dividend records
│   ├── calculated_dividends.csv  # Output: total dividends per stock
│   └── previous/          # Backup of previous runs
├── stocks_data/           # Stocks data
│   ├── market_orders/     # Input: CSV files per year
│   │   ├── market_orders_2020.csv
│   │   ├── market_orders_2021.csv
│   │   ├── market_orders_2022.csv
│   │   ├── market_orders_2023.csv
│   │   └── market_orders_2024.csv
│   ├── market_orders_aggregated.csv  # Output: aggregated stock positions
│   └── previous/          # Backup of previous runs
└── requirements.txt      # Python dependencies
```

## Scripts

### stocks.py

Processes market orders from CSV files in the `stocks_data/market_orders/` directory. Aggregates buy/sell transactions per stock and calculates:
- Total quantity held
- Total cost in original currency
- Total cost in BGN (converted using exchange rate)
- Average purchase price
- Average currency exchange rate

Before writing output, backs up existing output to `stocks_data/previous/` with timestamp.

**Input format** (`stocks_data/market_orders/*.csv`):
- `Time`: Transaction date (YYYY-MM-DD)
- `Ticker`: Stock symbol
- `Name`: Company name
- `Action`: "Market buy" or "Market sell"
- `No. of shares`: Quantity
- `Price / share`: Price per share
- `Currency (Price / share)`: Currency code (GBP, EUR, USD, etc.)

**Output** (`stocks_data/market_orders_aggregated.csv`):
- `Name`, `Total Quantity`, `Total Cost`, `Total Cost BGN`, `Average Price`, `Currency`, `Date`, `Average currency rate`

### dividends.py

Sums dividend payments per stock from a CSV file.

Before writing output, backs up existing output to `dividends_data/previous/` with timestamp.

**Input format** (`dividends_data/dividends.csv`):
- `Name`: Company name
- `Total`: Dividend amount in EUR

**Output** (`dividends_data/calculated_dividends.csv`):
- `Name`, `Total Dividend`

### exchange_rates.py

Fetches daily exchange rates from the Bulgarian National Bank (BNB) API. Caches rates by date to minimize API calls.

**Supported currencies**: All currencies tracked by BNB (GBP, USD, CHF, etc.)
**EUR is hardcoded**: 1 EUR = 1.95583 BGN (Bulgarian lev)

## Run

```bash
# Activate virtual environment (required before running scripts)
source .venv/bin/activate

# Process market orders
python stocks.py

# Process dividends
python dividends.py
```

## Dependencies

- beautifulsoup4
- requests
- python-dateutil