"""
Beta Value Calculation for IREDA.NS
====================================
- Benchmark Index : NIFTY 50 (^NSEI)
- Period          : Last 1 Year (weekly data)
- Formula         : Beta = Cov(Ri, Rm) / Var(Rm)
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ──────────────────────────────────────────────
# 1. Configuration
# ──────────────────────────────────────────────
STOCK_TICKER = "IREDA.NS"
INDEX_TICKER = "^NSEI"          # NIFTY 50
STOCK_NAME   = "IREDA"
INDEX_NAME   = "NIFTY 50"

end_date   = datetime.today()
start_date = end_date - timedelta(days=365)

print(f"Fetching weekly data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} ...")

# ──────────────────────────────────────────────
# 2. Download Weekly Closing Prices
# ──────────────────────────────────────────────
stock_data = yf.download(STOCK_TICKER, start=start_date, end=end_date, interval="1wk", auto_adjust=True)
index_data = yf.download(INDEX_TICKER, start=start_date, end=end_date, interval="1wk", auto_adjust=True)

# Keep only the Close column & flatten MultiIndex if present
stock_close = stock_data["Close"].squeeze()
index_close = index_data["Close"].squeeze()

# ──────────────────────────────────────────────
# 3. Build a combined DataFrame
# ──────────────────────────────────────────────
df = pd.DataFrame({
    f"{STOCK_NAME}_Close": stock_close,
    f"{INDEX_NAME}_Close": index_close,
}).dropna()

# ──────────────────────────────────────────────
# 4. Calculate Weekly Returns  (% change)
# ──────────────────────────────────────────────
df[f"{STOCK_NAME}_Return(%)"] = df[f"{STOCK_NAME}_Close"].pct_change() * 100
df[f"{INDEX_NAME}_Return(%)"]  = df[f"{INDEX_NAME}_Close"].pct_change() * 100

# Drop the first row (NaN from pct_change)
df = df.dropna()

# ──────────────────────────────────────────────
# 5. Compute Beta
# ──────────────────────────────────────────────
stock_returns = df[f"{STOCK_NAME}_Return(%)"]
index_returns = df[f"{INDEX_NAME}_Return(%)"]

covariance  = np.cov(stock_returns, index_returns)[0][1]
variance_m  = np.var(index_returns, ddof=1)          # sample variance
beta        = covariance / variance_m

slope, intercept = np.polyfit(index_returns, stock_returns, 1)
# slope == beta (OLS regression)

# Correlation
correlation = np.corrcoef(stock_returns, index_returns)[0][1]

# ──────────────────────────────────────────────
# 6. Summary
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print(f"   BETA VALUE CALCULATION — {STOCK_NAME} vs {INDEX_NAME}")
print("=" * 60)
print(f"   Period               : {df.index[0].strftime('%Y-%m-%d')} to {df.index[-1].strftime('%Y-%m-%d')}")
print(f"   Data Frequency       : Weekly")
print(f"   Number of Weeks      : {len(df)}")
print(f"   Covariance(Ri,Rm)    : {covariance:.6f}")
print(f"   Variance(Rm)         : {variance_m:.6f}")
print("-" * 60)
print(f"   *** BETA VALUE       : {beta:.4f} ***")
print(f"   (Regression slope)   : {slope:.4f}  (cross-check)")
print(f"   Correlation (r)      : {correlation:.4f}")
print(f"   Alpha (intercept)    : {intercept:.4f}")
print("-" * 60)
if beta > 1:
    interpretation = "IREDA is MORE volatile than the market (Aggressive stock)"
elif beta == 1:
    interpretation = "IREDA moves in line with the market"
else:
    interpretation = "IREDA is LESS volatile than the market (Defensive stock)"
print(f"   Interpretation       : {interpretation}")
print("=" * 60)

# ──────────────────────────────────────────────
# 7. Excel file
# ──────────────────────────────────────────────
EXCEL_FILE = "Beta_Calculation_IREDA.xlsx"

with pd.ExcelWriter(EXCEL_FILE, engine="xlsxwriter") as writer:
    workbook = writer.book


    title_fmt = workbook.add_format({
        "bold": True, "font_size": 14, "align": "center",
        "valign": "vcenter", "font_color": "#FFFFFF",
        "bg_color": "#2F5496", "border": 1,
    })
    header_fmt = workbook.add_format({
        "bold": True, "font_size": 11, "align": "center",
        "bg_color": "#D6E4F0", "border": 1, "text_wrap": True,
    })
    num_fmt = workbook.add_format({"num_format": "#,##0.00", "border": 1, "align": "center"})
    pct_fmt = workbook.add_format({"num_format": "0.00", "border": 1, "align": "center"})
    date_fmt = workbook.add_format({"num_format": "dd-mmm-yyyy", "border": 1, "align": "center"})
    label_fmt = workbook.add_format({
        "bold": True, "font_size": 11, "bg_color": "#D6E4F0",
        "border": 1, "align": "left",
    })
    value_fmt = workbook.add_format({
        "font_size": 11, "border": 1, "align": "center", "num_format": "0.0000",
    })
    beta_fmt = workbook.add_format({
        "bold": True, "font_size": 13, "border": 2, "align": "center",
        "bg_color": "#FFC000", "num_format": "0.0000",
    })

    # ════════════════════════════════════════
    # SHEET 1: Weekly Data
    # ════════════════════════════════════════
    sheet1_name = "Weekly Data"
    df_export = df.copy()
    df_export.index.name = "Week Ending"
    df_export = df_export.reset_index()
    df_export.to_excel(writer, sheet_name=sheet1_name, startrow=2, index=False)

    ws1 = writer.sheets[sheet1_name]
    ws1.merge_range("A1:E1", f"APPENDIX — Weekly Stock Data: {STOCK_NAME} vs {INDEX_NAME} (Beta Calculation)",
                    title_fmt)
    ws1.set_row(0, 30)

    # Apply header format
    for col_num, col_name in enumerate(df_export.columns):
        ws1.write(2, col_num, col_name, header_fmt)

    # Apply data formats
    for row_idx in range(len(df_export)):
        ws1.write(row_idx + 3, 0, df_export.iloc[row_idx, 0], date_fmt)  # Date
        ws1.write(row_idx + 3, 1, df_export.iloc[row_idx, 1], num_fmt)   # Stock Close
        ws1.write(row_idx + 3, 2, df_export.iloc[row_idx, 2], num_fmt)   # Index Close
        ws1.write(row_idx + 3, 3, df_export.iloc[row_idx, 3], pct_fmt)   # Stock Return
        ws1.write(row_idx + 3, 4, df_export.iloc[row_idx, 4], pct_fmt)   # Index Return

    # Column widths
    ws1.set_column("A:A", 16)
    ws1.set_column("B:C", 18)
    ws1.set_column("D:E", 20)

    # ════════════════════════════════════════
    # SHEET 2: Beta Summary
    # ════════════════════════════════════════
    sheet2_name = "Beta Summary"
    ws2 = workbook.add_worksheet(sheet2_name)

    ws2.merge_range("A1:D1", f"BETA VALUE CALCULATION — {STOCK_NAME} vs {INDEX_NAME}", title_fmt)
    ws2.set_row(0, 30)

    summary_rows = [
        ("Stock",                    STOCK_NAME),
        ("Benchmark Index",          INDEX_NAME),
        ("Period",                   f"{df.index[0].strftime('%d-%b-%Y')} to {df.index[-1].strftime('%d-%b-%Y')}"),
        ("Data Frequency",           "Weekly"),
        ("Number of Observations",   len(df)),
        ("Covariance (Ri, Rm)",      covariance),
        ("Variance (Rm)",            variance_m),
        ("Beta (β) = Cov/Var",       beta),
        ("Regression Slope (cross-check)", slope),
        ("Correlation (r)",          correlation),
        ("Alpha (Intercept)",        intercept),
    ]

    for i, (label, value) in enumerate(summary_rows):
        ws2.write(i + 2, 0, label, label_fmt)
        if isinstance(value, (int, float)):
            ws2.write(i + 2, 1, value, value_fmt)
        else:
            ws2.write(i + 2, 1, str(value), workbook.add_format({"border": 1, "align": "center", "font_size": 11}))

    # BETA VALUE (highlighted)
    beta_row = len(summary_rows) + 3
    ws2.write(beta_row, 0, "BETA VALUE (β)", workbook.add_format({
        "bold": True, "font_size": 13, "bg_color": "#FFC000", "border": 2, "align": "right",
    }))
    ws2.write(beta_row, 1, beta, beta_fmt)
    ws2.set_row(beta_row, 28)

    # Interpretation
    ws2.merge_range(beta_row + 2, 0, beta_row + 2, 3, f"Interpretation: {interpretation}",
                    workbook.add_format({
                        "bold": True, "font_size": 11, "italic": True,
                        "align": "left", "valign": "vcenter",
                    }))

    # Formula
    ws2.merge_range(beta_row + 4, 0, beta_row + 4, 3, "Formula: β = Cov(Ri, Rm) / Var(Rm)",
                    workbook.add_format({
                        "font_size": 11, "italic": True, "align": "left",
                    }))
    ws2.merge_range(beta_row + 5, 0, beta_row + 5, 3,
                    "Where Ri = Weekly return of IREDA, Rm = Weekly return of NIFTY 50",
                    workbook.add_format({
                        "font_size": 10, "italic": True, "align": "left", "font_color": "#808080",
                    }))

    ws2.set_column("A:A", 28)
    ws2.set_column("B:B", 22)
    ws2.set_column("C:D", 15)
