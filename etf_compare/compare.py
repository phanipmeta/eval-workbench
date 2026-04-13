"""Core comparison logic for ETFs."""

from .fetcher import fetch_etf_info, fetch_price_history


def compare_etfs(tickers: list[str]) -> dict:
    """Compare multiple ETFs side by side.

    Args:
        tickers: List of ETF ticker symbols.

    Returns:
        Dict with 'etfs' (list of info dicts) and 'comparison' summary.
    """
    etfs = []
    for ticker in tickers:
        info = fetch_etf_info(ticker)
        etfs.append(info)

    comparison = _build_comparison(etfs)

    return {"etfs": etfs, "comparison": comparison}


def compare_returns(tickers: list[str], period: str = "1y") -> dict:
    """Compare price returns over a given period.

    Args:
        tickers: List of ETF ticker symbols.
        period: Time period (1mo, 3mo, 6mo, 1y, 2y, 5y).

    Returns:
        Dict mapping each ticker to its return percentage.
    """
    results = {}
    for ticker in tickers:
        history = fetch_price_history(ticker, period=period)
        if len(history) >= 2:
            start_price = history[0]["close"]
            end_price = history[-1]["close"]
            pct_return = ((end_price - start_price) / start_price) * 100
            results[ticker.upper()] = round(pct_return, 2)
        else:
            results[ticker.upper()] = None

    return results


def _build_comparison(etfs: list[dict]) -> dict:
    """Build a comparison summary highlighting best/worst across metrics."""
    if not etfs:
        return {}

    comparison = {}

    # Lowest expense ratio
    with_er = [(e["ticker"], e["expense_ratio"]) for e in etfs if e["expense_ratio"] is not None]
    if with_er:
        best = min(with_er, key=lambda x: x[1])
        comparison["lowest_expense_ratio"] = {"ticker": best[0], "value": best[1]}

    # Highest YTD return
    with_ytd = [(e["ticker"], e["ytd_return"]) for e in etfs if e["ytd_return"] is not None]
    if with_ytd:
        best = max(with_ytd, key=lambda x: x[1])
        comparison["highest_ytd_return"] = {"ticker": best[0], "value": best[1]}

    # Highest 5-year return
    with_5y = [(e["ticker"], e["five_year_return"]) for e in etfs if e["five_year_return"] is not None]
    if with_5y:
        best = max(with_5y, key=lambda x: x[1])
        comparison["highest_5y_return"] = {"ticker": best[0], "value": best[1]}

    # Highest dividend yield
    with_div = [(e["ticker"], e["dividend_yield"]) for e in etfs if e["dividend_yield"] is not None]
    if with_div:
        best = max(with_div, key=lambda x: x[1])
        comparison["highest_dividend_yield"] = {"ticker": best[0], "value": best[1]}

    # Lowest beta (least volatile)
    with_beta = [(e["ticker"], e["beta"]) for e in etfs if e["beta"] is not None]
    if with_beta:
        best = min(with_beta, key=lambda x: x[1])
        comparison["lowest_beta"] = {"ticker": best[0], "value": best[1]}

    return comparison
