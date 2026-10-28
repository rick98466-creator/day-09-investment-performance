"""Combine investment return and risk metrics."""

import pandas as pd

from investment_performance.config import PROCESSED_DIR
from investment_performance.data_loader import load_investment_prices
from investment_performance.returns import calculate_returns
from investment_performance.risk import calculate_risk_metrics


def compare_investments(prices: pd.DataFrame) -> pd.DataFrame:
    """Rank investments by cumulative return and include risk metrics."""
    _, cumulative = calculate_returns(prices)
    risk = calculate_risk_metrics(prices)

    price_columns = [column for column in prices.columns if column != "date"]
    final_returns = cumulative.iloc[-1]

    comparison = pd.DataFrame({
        "investment": price_columns,
        "cumulative_return": [
            float(final_returns[column]) for column in price_columns
        ],
    })

    comparison = comparison.merge(risk, on="investment", how="inner")
    comparison = comparison.sort_values(
        "cumulative_return", ascending=False
    ).reset_index(drop=True)

    comparison.insert(0, "rank", range(1, len(comparison) + 1))

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(
        PROCESSED_DIR / "investment_comparison.csv", index=False
    )

    return comparison


if __name__ == "__main__":
    prices = load_investment_prices()
    results = compare_investments(prices)

    print(results.to_string(
        index=False,
        formatters={
            "cumulative_return": lambda x: f"{x:.2%}",
            "annualized_volatility": lambda x: f"{x:.2%}",
            "maximum_drawdown": lambda x: f"{x:.2%}",
        },
    ))