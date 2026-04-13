"""Format comparison results for terminal output."""

from tabulate import tabulate


def format_pct(value) -> str:
    """Format a decimal as a percentage string."""
    if value is None:
        return "N/A"
    return f"{value * 100:.2f}%"


def format_currency(value) -> str:
    """Format a number as a dollar amount."""
    if value is None:
        return "N/A"
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.1f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    return f"${value:,.0f}"


def format_comparison_table(result: dict) -> str:
    """Format the comparison result as a table.

    Args:
        result: Output from compare_etfs().

    Returns:
        Formatted string with the comparison table.
    """
    etfs = result["etfs"]
    comparison = result["comparison"]

    headers = ["Metric"] + [e["ticker"] for e in etfs]
    rows = [
        ["Name"] + [e["name"] for e in etfs],
        ["Category"] + [e["category"] for e in etfs],
        ["Total Assets"] + [format_currency(e["total_assets"]) for e in etfs],
        ["Expense Ratio"] + [format_pct(e["expense_ratio"]) for e in etfs],
        ["YTD Return"] + [format_pct(e["ytd_return"]) for e in etfs],
        ["3-Year Return"] + [format_pct(e["three_year_return"]) for e in etfs],
        ["5-Year Return"] + [format_pct(e["five_year_return"]) for e in etfs],
        ["Dividend Yield"] + [format_pct(e["dividend_yield"]) for e in etfs],
        ["Beta (3Y)"] + [f"{e['beta']:.2f}" if e["beta"] else "N/A" for e in etfs],
    ]

    table = tabulate(rows, headers=headers, tablefmt="simple")

    # Add comparison highlights
    highlights = []
    labels = {
        "lowest_expense_ratio": "Lowest Expense Ratio",
        "highest_ytd_return": "Highest YTD Return",
        "highest_5y_return": "Highest 5Y Return",
        "highest_dividend_yield": "Highest Dividend Yield",
        "lowest_beta": "Lowest Beta (least volatile)",
    }
    for key, label in labels.items():
        if key in comparison:
            entry = comparison[key]
            value = format_pct(entry["value"]) if "return" in key or "yield" in key or "ratio" in key else f"{entry['value']:.2f}"
            highlights.append(f"  {label}: {entry['ticker']} ({value})")

    output = f"\n{table}\n"
    if highlights:
        output += "\nHighlights:\n" + "\n".join(highlights) + "\n"

    return output


def format_returns_table(returns: dict, period: str) -> str:
    """Format return comparison as a table.

    Args:
        returns: Dict mapping ticker to return percentage.
        period: The time period string.

    Returns:
        Formatted string.
    """
    headers = ["Ticker", f"Return ({period})"]
    rows = []
    for ticker, ret in returns.items():
        if ret is not None:
            rows.append([ticker, f"{ret:+.2f}%"])
        else:
            rows.append([ticker, "N/A"])

    return "\n" + tabulate(rows, headers=headers, tablefmt="simple") + "\n"


def format_etf_info(info: dict) -> str:
    """Format a single ETF's info for display.

    Args:
        info: Output from fetch_etf_info().

    Returns:
        Formatted string.
    """
    lines = [
        f"\n  {info['ticker']} — {info['name']}",
        f"  Category:       {info['category']}",
        f"  Total Assets:   {format_currency(info['total_assets'])}",
        f"  Expense Ratio:  {format_pct(info['expense_ratio'])}",
        f"  YTD Return:     {format_pct(info['ytd_return'])}",
        f"  3-Year Return:  {format_pct(info['three_year_return'])}",
        f"  5-Year Return:  {format_pct(info['five_year_return'])}",
        f"  Dividend Yield: {format_pct(info['dividend_yield'])}",
        f"  Beta (3Y):      {info['beta']:.2f}" if info["beta"] else "  Beta (3Y):      N/A",
        "",
    ]
    return "\n".join(lines)
