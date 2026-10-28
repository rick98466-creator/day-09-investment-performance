"""Calculate daily returns and cumulative performance."""

import pandas as pd

from investment_performance.config import PROCESSED_DIR
from investment_performance.data_loader import load_investment_prices
from investment_performance.validation import validate_investment_prices


def calculate_returns(prices: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calculate daily percentage returns and cumulative returns."""
    prices = validate_investment_prices(prices)

    price_columns = [column for column in prices.columns if column != "date"]
    daily_returns = prices[["date"]].copy()
    cumulative_returns = prices[["date"]].copy()

    for column in price_columns:
        daily_returns[column] = prices[column].pct_change()
        cumulative_returns[column] = prices[column] / prices[column].iloc[0] - 1

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    daily_returns.to_csv(PROCESSED_DIR / "daily_returns.csv", index=False)
    cumulative_returns.to_csv(PROCESSED_DIR / "cumulative_returns.csv", index=False)

    return daily_returns, cumulative_returns


if __name__ == "__main__":
    prices = load_investment_prices()
    daily, cumulative = calculate_returns(prices)

    print("Daily returns (first 5 rows):")
    print(daily.head().to_string(index=False, float_format=lambda x: f"{x:.4%}"))
    print("\nFinal cumulative returns:")
    print(cumulative.tail(1).to_string(index=False, float_format=lambda x: f"{x:.4%}"))