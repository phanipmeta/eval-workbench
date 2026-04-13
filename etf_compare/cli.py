"""CLI entry point for ETF comparison tool."""

import argparse
import sys

from .fetcher import fetch_etf_info
from .compare import compare_etfs, compare_returns
from .formatter import (
    format_comparison_table,
    format_returns_table,
    format_etf_info,
)


def main():
    parser = argparse.ArgumentParser(
        prog="etf-compare",
        description="Compare ETFs side by side — expense ratios, returns, risk metrics, and more.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # compare command
    compare_parser = subparsers.add_parser("compare", help="Compare multiple ETFs side by side")
    compare_parser.add_argument("tickers", nargs="+", help="ETF ticker symbols (e.g., VOO SPY IVV)")

    # returns command
    returns_parser = subparsers.add_parser("returns", help="Compare price returns over a period")
    returns_parser.add_argument("tickers", nargs="+", help="ETF ticker symbols")
    returns_parser.add_argument(
        "-p", "--period",
        default="1y",
        choices=["1mo", "3mo", "6mo", "1y", "2y", "5y"],
        help="Time period (default: 1y)",
    )

    # info command
    info_parser = subparsers.add_parser("info", help="Show detailed info for a single ETF")
    info_parser.add_argument("ticker", help="ETF ticker symbol")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(1)

    try:
        if args.command == "compare":
            if len(args.tickers) < 2:
                print("Error: Need at least 2 tickers to compare.")
                sys.exit(1)
            print(f"Fetching data for {', '.join(t.upper() for t in args.tickers)}...")
            result = compare_etfs(args.tickers)
            print(format_comparison_table(result))

        elif args.command == "returns":
            if len(args.tickers) < 2:
                print("Error: Need at least 2 tickers to compare.")
                sys.exit(1)
            print(f"Fetching {args.period} returns for {', '.join(t.upper() for t in args.tickers)}...")
            returns = compare_returns(args.tickers, period=args.period)
            print(format_returns_table(returns, args.period))

        elif args.command == "info":
            print(f"Fetching info for {args.ticker.upper()}...")
            info = fetch_etf_info(args.ticker)
            print(format_etf_info(info))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
