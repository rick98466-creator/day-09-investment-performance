"""Export investment performance analysis to Excel."""

import pandas as pd

from investment_performance.config import REPORTS_DIR
from investment_performance.comparison import compare_investments
from investment_performance.data_loader import load_investment_prices
from investment_performance.returns import calculate_returns
from investment_performance.risk import calculate_risk_metrics


def export_performance_report(prices: pd.DataFrame) -> None:
    """Create an Excel workbook containing performance analysis."""
    comparison = compare_investments(prices)
    daily_returns, cumulative_returns = calculate_returns(prices)
    risk_metrics = calculate_risk_metrics(prices)

    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORTS_DIR / "investment_performance_report.xlsx"

    with pd.ExcelWriter(report_path, engine="openpyxl") as writer:
        comparison.to_excel(
            writer, sheet_name="Executive Summary", index=False
        )
        daily_returns.to_excel(
            writer, sheet_name="Daily Returns", index=False
        )
        cumulative_returns.to_excel(
            writer, sheet_name="Cumulative Returns", index=False
        )
        risk_metrics.to_excel(
            writer, sheet_name="Risk Metrics", index=False
        )

    print(f"Excel report created: {report_path}")


if __name__ == "__main__":
    export_performance_report(load_investment_prices())