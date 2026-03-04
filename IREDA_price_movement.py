"""
IREDA Price Movement Since Listing
====================================
Plots the daily closing price of IREDA.NS from its listing date
(29-Nov-2023) to today, with key annotations (listing price,
all-time high, all-time low, current price).
"""

import yfinance as yf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

# ── Configuration ─────────────────────────────
TICKER = "IREDA.NS"
LISTING_DATE = "2023-11-29"

# ── Fetch Data ────────────────────────────────
print(f"Fetching daily data for {TICKER} since {LISTING_DATE} …")
stock = yf.Ticker(TICKER)
df = stock.history(start=LISTING_DATE)

if df.empty:
    raise SystemExit("No data returned – check your ticker or internet connection.")

# ── Key Metrics ───────────────────────────────
listing_price = df.iloc[0]["Open"]
current_price = df["Close"].iloc[-1]
current_date = df.index[-1]

high_price = df["High"].max()
high_date = df["High"].idxmax()

low_price = df["Low"].min()
low_date = df["Low"].idxmin()

pct_change = ((current_price - listing_price) / listing_price) * 100

print(f"  Listing Price : ₹{listing_price:.2f}")
print(f"  Current Price : ₹{current_price:.2f}  ({pct_change:+.1f}% since listing)")
print(f"  All-Time High : ₹{high_price:.2f}  on {high_date.strftime('%d-%b-%Y')}")
print(f"  All-Time Low  : ₹{low_price:.2f}  on {low_date.strftime('%d-%b-%Y')}")

# ── Plot ──────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 7))

# Price line
ax.plot(df.index, df["Close"], color="#1f77b4", linewidth=1.4, label="Close Price")

ax.fill_between(df.index, df["Close"], alpha=0.10, color="#1f77b4")

# Moving averages
if len(df) >= 50:
    ax.plot(df.index, df["Close"].rolling(50).mean(),
            color="orange", linewidth=1, linestyle="--", label="50-Day MA")
if len(df) >= 200:
    ax.plot(df.index, df["Close"].rolling(200).mean(),
            color="red", linewidth=1, linestyle="--", label="200-Day MA")

offset = high_price * 0.04  # arrow offset

# All-time high
ax.annotate(f"ATH ₹{high_price:.2f}\n({high_date.strftime('%d-%b-%Y')})",
            xy=(high_date, high_price), xytext=(high_date, high_price + offset),
            fontsize=8, fontweight="bold", color="green",
            arrowprops=dict(arrowstyle="->", color="green", lw=1.2),
            ha="center")

# All-time low
ax.annotate(f"ATL ₹{low_price:.2f}\n({low_date.strftime('%d-%b-%Y')})",
            xy=(low_date, low_price), xytext=(low_date, low_price - offset * 1.5),
            fontsize=8, fontweight="bold", color="red",
            arrowprops=dict(arrowstyle="->", color="red", lw=1.2),
            ha="center")

# Listing price horizontal line
ax.axhline(y=listing_price, color="grey", linewidth=0.8, linestyle=":",
           label=f"Listing Price ₹{listing_price:.2f}")

# Current price marker
ax.plot(current_date, current_price, marker="D", color="black", markersize=7, zorder=5)
ax.annotate(f"CMP ₹{current_price:.2f}",
            xy=(current_date, current_price),
            xytext=(current_date, current_price + offset),
            fontsize=8, fontweight="bold", color="black",
            arrowprops=dict(arrowstyle="->", color="black", lw=1.2),
            ha="center")

# ── Volume subplot (secondary axis) ──────────
ax2 = ax.twinx()
ax2.bar(df.index, df["Volume"], color="grey", alpha=0.18, width=1)
ax2.set_ylabel("Volume", fontsize=10, color="grey")
ax2.tick_params(axis="y", labelcolor="grey", labelsize=8)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1e6:.0f}M"))


ax.set_title(f"IREDA (IREDA.NS) — Price Movement Since Listing ({LISTING_DATE})",
             fontsize=14, fontweight="bold", pad=15)
ax.set_xlabel("Date", fontsize=11)
ax.set_ylabel("Price (₹)", fontsize=11)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
ax.tick_params(axis="x", rotation=45)
ax.legend(loc="upper left", fontsize=9)
ax.grid(True, linestyle="--", alpha=0.4)

# Info box
textstr = (f"Listing: ₹{listing_price:.2f}\n"
           f"CMP: ₹{current_price:.2f} ({pct_change:+.1f}%)\n"
           f"High: ₹{high_price:.2f}\n"
           f"Low: ₹{low_price:.2f}")
props = dict(boxstyle="round,pad=0.5", facecolor="lightyellow", alpha=0.85, edgecolor="grey")
ax.text(0.01, 0.97, textstr, transform=ax.transAxes, fontsize=9,
        verticalalignment="top", bbox=props)

fig.tight_layout()
plt.savefig("IREDA_price_movement.png", dpi=150, bbox_inches="tight")
print("\nChart saved as IREDA_price_movement.png")
plt.show()

