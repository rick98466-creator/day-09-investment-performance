"""Load historical investment prices."""

import pandas as pd

from investment_performance.config import INPUT_FILE


def load_investment_prices() -> pd.DataFrame:
    """Read investment prices and parse trading dates."""
    df = pd.read_csv(INPUT_FILE, parse_dates=["date"])

    if df.empty:
        raise ValueError("Investment price data cannot be empty.")

    return df