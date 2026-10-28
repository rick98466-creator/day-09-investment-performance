"""Validation rules for investment prices."""

import numpy as np
import pandas as pd

DATE_COLUMN = "date"


def validate_investment_prices(df: pd.DataFrame) -> pd.DataFrame:
    """Validate dates and positive, finite investment prices."""
    if df.empty:
        raise ValueError("Investment price data cannot be empty.")

    if DATE_COLUMN not in df.columns:
        raise ValueError("Missing required date column.")

    if len(df.columns) < 2:
        raise ValueError("At least one investment column is required.")

    result = df.copy()
    result["date"] = pd.to_datetime(result["date"], errors="raise")

    if result["date"].isna().any():
        raise ValueError("Dates cannot contain missing values.")

    if result["date"].duplicated().any():
        raise ValueError("Dates must not be duplicated.")

    if not result["date"].is_monotonic_increasing:
        raise ValueError("Dates must be in ascending order.")

    price_columns = [column for column in result.columns if column != DATE_COLUMN]

    if result[price_columns].isna().any().any():
        raise ValueError("Investment prices cannot contain missing values.")

    for column in price_columns:
        result[column] = pd.to_numeric(result[column], errors="raise")

    prices = result[price_columns].to_numpy(dtype=float)

    if not np.isfinite(prices).all():
        raise ValueError("Investment prices must be finite.")

    if (prices <= 0).any():
        raise ValueError("Investment prices must be positive.")

    return result