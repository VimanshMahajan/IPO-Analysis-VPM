# IREDA Stock — Beta Calculation & Price Analysis

A Python-based toolkit for calculating the **Beta (β)** of **IREDA** (Indian Renewable Energy Development Agency) against the **NIFTY 50** benchmark index, along with price-movement visualisation and key stock metrics.

## Project Overview

| Script | Purpose |
|---|---|
| `beta_value_IREDA.py` | Calculates Beta using weekly returns over the past year and exports a formatted Excel report |
| `IREDA_price_movement.py` | Plots IREDA's daily closing price since listing with annotated ATH, ATL, and moving averages |
| `share_info.py` | Fetches and prints key stock information (listing price, CMP, high/low since listing) |

## Key Concepts

**Beta (β)** measures a stock's volatility relative to the market:

```
β = Cov(Rᵢ, Rₘ) / Var(Rₘ)
```

| Beta Range | Interpretation |
|---|---|
| β > 1 | More volatile than the market (aggressive) |
| β = 1 | Moves in line with the market |
| β < 1 | Less volatile than the market (defensive) |

## Output

### Excel Report (`Beta_Calculation_IREDA.xlsx`)

The report contains three sheets:

1. **Weekly Data** — Weekly closing prices and percentage returns for both IREDA and NIFTY 50.
2. **Beta Summary** — Covariance, variance, beta, correlation, alpha, and interpretation.
3. **Regression Chart** — Scatter plot of stock vs. index returns with a fitted regression line.

### Price Movement Chart (`IREDA_price_movement.png`)

An annotated chart showing daily price movement since IREDA's listing (29-Nov-2023), including:
- 50-day and 200-day moving averages
- All-time high / low annotations
- Volume overlay
- Listing price reference line

## Requirements

- Python 3.8+
- Dependencies:

```
yfinance
pandas
numpy
matplotlib
xlsxwriter
```

Install all dependencies:

```bash
pip install yfinance pandas numpy matplotlib xlsxwriter
```

## Usage

```bash
# Generate Beta calculation report (Excel)
python beta_value_IREDA.py

# Generate price movement chart (PNG)
python IREDA_price_movement.py

# Print stock info to console
python share_info.py
```

## Configuration

All scripts default to:

| Parameter | Value |
|---|---|
| Stock Ticker | `IREDA.NS` |
| Benchmark Index | `^NSEI` (NIFTY 50) |
| Data Period | Last 1 year (weekly) for beta; since listing for price chart |


