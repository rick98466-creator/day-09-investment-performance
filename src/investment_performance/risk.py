"""Calculate investment volatility and maximum drawdown."""

import pandas as pd

from investment_performance.config import PROCESSED_DIR
from investment_performance.data_loader import load_investment_prices
from investment_performance.returns import calculate_returns


TRADING_DAYS_PER_YEAR = 252


def calculate_risk_metrics(prices: pd.DataFrame) -> pd.DataFrame:
    """Calculate annualized volatility and maximum drawdown."""
    daily_returns, _ = calculate_returns(prices)
    price_columns = [column for column in prices.columns if column != "date"]
    rows = []

    for column in price_columns:
        returns = daily_returns[column].dropna()
        price_series = prices[column].astype(float)

        annualized_volatility = (
            returns.std(ddof=1) * TRADING_DAYS_PER_YEAR ** 0.5
        )

        running_peak = price_series.cummax()
        drawdowns = price_series / running_peak - 1
        maximum_drawdown = drawdowns.min()

        rows.append({
            "investment": column,
            "annualized_volatility": annualized_volatility,
            "maximum_drawdown": maximum_drawdown,
        })

    results = pd.DataFrame(rows)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    results.to_csv(PROCESSED_DIR / "risk_metrics.csv", index=False)

    return results


if __name__ == "__main__":
    prices = load_investment_prices()
    results = calculate_risk_metrics(prices)

    print(results.to_string(
        index=False,
        formatters={
            "annualized_volatility": lambda x: f"{x:.2%}",
            "maximum_drawdown": lambda x: f"{x:.2%}",
        },
    ))