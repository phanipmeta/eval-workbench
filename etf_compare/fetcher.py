"""Fetch ETF data from Yahoo Finance using yfinance."""

from datetime import datetime, timedelta
import yfinance as yf


def fetch_etf_info(ticker: str) -> dict:
    """Fetch basic ETF info: name, expense ratio, category, holdings count."""
    etf = yf.Ticker(ticker)
    info = etf.info

    # Validate ticker exists - info dict will be empty or missing key fields for invalid tickers
    if not info or (
        not info.get("longName")
        and not info.get("shortName")
        and not info.get("symbol")
    ):
        raise ValueError(
            f"Ticker '{ticker.upper()}' not found. Please check the symbol and try again."
        )

    # Note: ytdReturn and netExpenseRatio from yfinance are already percentages
    # (e.g., -4.34 for -4.34%, 0.03 for 0.03%), but other returns are decimals
    # (e.g., 0.1228 for 12.28%). Normalize to decimals for consistency.
    ytd = info.get("ytdReturn")
    if ytd is not None:
        ytd = ytd / 100

    expense = info.get("netExpenseRatio")
    if expense is not None:
        expense = expense / 100

    return {
        "ticker": ticker.upper(),
        "name": info.get("longName") or info.get("shortName", "N/A"),
        "expense_ratio": expense,
        "category": info.get("category", "N/A"),
        "total_assets": info.get("totalAssets"),
        "ytd_return": ytd,
        "three_year_return": info.get("threeYearAverageReturn"),
        "five_year_return": info.get("fiveYearAverageReturn"),
        "dividend_yield": info.get("yield"),
        "beta": info.get("beta3Year"),
        "currency": info.get("currency", "USD"),
    }


def fetch_price_history(ticker: str, period: str = "1y") -> list[dict]:
    """Fetch historical closing prices for an ETF.

    Args:
        ticker: ETF ticker symbol.
        period: Time period — 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, max.

    Returns:
        List of dicts with 'date' and 'close' keys.
    """
    etf = yf.Ticker(ticker)
    hist = etf.history(period=period)

    if hist.empty:
        return []

    return [
        {"date": date.strftime("%Y-%m-%d"), "close": round(row["Close"], 2)}
        for date, row in hist.iterrows()
    ]


def fetch_top_holdings(ticker: str) -> list[dict]:
    """Fetch top holdings for an ETF (if available via yfinance)."""
    etf = yf.Ticker(ticker)

    try:
        holdings = etf.major_holders
        if holdings is not None and not holdings.empty:
            return [
                {"description": row[1], "value": row[0]}
                for _, row in holdings.iterrows()
            ]
    except Exception:
        pass

    return []
