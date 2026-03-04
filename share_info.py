import yfinance as yf

TICKER = "IREDA.NS"

stock = yf.Ticker(TICKER)

# --- Listing Price ---
# IREDA listed on NSE on 29-Nov-2023. Fetch that day's Open price.
listing_date = "2023-11-29"
listing_data = stock.history(start=listing_date, end="2023-11-30")
if not listing_data.empty:
    listing_price = listing_data.iloc[0]["Open"]
else:
    listing_price = "N/A"

# --- Current Market Price ---
info = stock.info
current_price = info.get("currentPrice") or info.get("regularMarketPrice", "N/A")

# --- High / Low since Listing ---
all_data = stock.history(start=listing_date, period="max")
if not all_data.empty:
    high_since_listing = all_data["High"].max()
    high_date = all_data["High"].idxmax().strftime("%d-%b-%Y")
    low_since_listing = all_data["Low"].min()
    low_date = all_data["Low"].idxmin().strftime("%d-%b-%Y")
else:
    high_since_listing = "N/A"
    high_date = "N/A"
    low_since_listing = "N/A"
    low_date = "N/A"


print(f"{'='*50}")
print(f"  Stock Information for {TICKER}")
print(f"{'='*50}")
print(f"  7. Listing Price (Open on {listing_date}):  ₹{listing_price}")
print(f"  8. Current Market Price:                    ₹{current_price}")
print(f"  9. High since Listing:                      ₹{high_since_listing}  (on {high_date})")
print(f"     Low  since Listing:                      ₹{low_since_listing}  (on {low_date})")
print(f"{'='*50}")
