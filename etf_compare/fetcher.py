"""Fetch ETF data from Yahoo Finance using yfinance."""

from datetime import datetime, timedelta
import yfinance as yf


def fetch_etf_info(ticker: str) -> dict:
    """Fetch basic ETF info: name, expense ratio, category, holdings count."""
    etf = yf.Ticker(ticker)
    info = etf.info

    return {
        "ticker": ticker.upper(),
        "name": info.get("longName") or info.get("shortName", "N/A"),
        "expense_ratio": info.get("annualReportExpenseRatio"),
        "category": info.get("category", "N/A"),
        "total_assets": info.get("totalAssets"),
        "ytd_return": info.get("ytdReturn"),
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
