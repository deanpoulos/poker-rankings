import math

import numpy as np
import pandas as pd


def drop_non_tournament_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes the special rows for rankings from the original sheet.
    """
    # Create mask for first non-datetime, non-NaN value
    mask = df["GAMES"].apply(lambda x: not (pd.isna(x) or _is_datetime_string(x) or x == ""))

    # Find the first valid index
    first_invalid_index = mask.idxmax() if mask.any() else None

    # Slice DataFrame
    df = df.iloc[:first_invalid_index] if first_invalid_index is not None else df

    # Drop fully NaN rows for unheld tournaments
    df = df.dropna(how="all")

    return df


def drop_non_player_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes the special columns for other tournament details from the original sheet.
    """
    # Find the first column containing "Unnamed"
    col_idx = next((i for i, col in enumerate(df.columns) if "Unnamed" in col), None)

    # Drop all columns after the first "Unnamed" column
    if col_idx is not None:
        df = df.iloc[:, :col_idx]

    return df


def drop_profit_columns(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop(df.columns[1::2], axis=1)


def recast_table_values_from_strings(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recasts all string values from a .csv into datetimes and integers.
    """
    # Ensure 'GAMES' is a datetime column
    df.rename(columns={df.columns[0]: "Date"}, inplace=True)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Drop empty rows at the end
    df = df.dropna(subset=["Date"])

    df.iloc[:, 1:] = df.iloc[:, 1:].applymap(lambda x: int(x) if isinstance(x, str) or not pd.isna(x) else x)

    return df


def _is_datetime_string(x) -> bool:
    try:
        pd.to_datetime(x)  # Try converting to datetime
        return True
    except:
        return False
