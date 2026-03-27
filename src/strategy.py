# Signal logic
import pandas as pd


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["SMA20"] = df["close"].rolling(window=20).mean()
    df["SMA50"] = df["close"].rolling(window=50).mean()
    return df


def generate_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["signal"] = "HOLD"

    df.loc[df["SMA20"] > df["SMA50"], "signal"] = "BUY"
    df.loc[df["SMA20"] < df["SMA50"], "signal"] = "SELL"

    return df