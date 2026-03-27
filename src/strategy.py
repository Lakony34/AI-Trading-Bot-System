import pandas as pd


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # SMA
    df["SMA20"] = df["close"].rolling(window=20).mean()
    df["SMA50"] = df["close"].rolling(window=50).mean()

    # RSI 14
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    df["RSI"] = 100 - (100 / (1 + rs))

    # Bollinger Bands 20 / 2
    df["BB_MIDDLE"] = df["close"].rolling(window=20).mean()
    rolling_std = df["close"].rolling(window=20).std()

    df["BB_UPPER"] = df["BB_MIDDLE"] + (2 * rolling_std)
    df["BB_LOWER"] = df["BB_MIDDLE"] - (2 * rolling_std)

    return df


def generate_trend_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["trend_signal"] = "HOLD"

    df.loc[df["SMA20"] > df["SMA50"], "trend_signal"] = "BUY"
    df.loc[df["SMA20"] < df["SMA50"], "trend_signal"] = "SELL"

    return df


def generate_entry_signals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["entry_signal"] = "NONE"
    df["bollinger_context"] = "NEUTRAL"

    df.loc[df["close"] > df["BB_UPPER"], "bollinger_context"] = "OVERBOUGHT"
    df.loc[df["close"] < df["BB_LOWER"], "bollinger_context"] = "OVERSOLD"

    valid_data = (
        df["SMA20"].notna() &
        df["SMA50"].notna() &
        df["RSI"].notna() &
        df["BB_UPPER"].notna() &
        df["BB_LOWER"].notna()
    )

    bullish_cross = (
        (df["SMA20"] > df["SMA50"]) &
        (df["SMA20"].shift(1) <= df["SMA50"].shift(1))
    )

    bearish_cross = (
        (df["SMA20"] < df["SMA50"]) &
        (df["SMA20"].shift(1) >= df["SMA50"].shift(1))
    )

    buy_condition = (
        valid_data &
        bullish_cross &
        (df["RSI"] < 70) &
        (df["close"] < df["BB_UPPER"])
    )

    sell_condition = (
        valid_data &
        bearish_cross &
        (df["RSI"] > 30) &
        (df["close"] > df["BB_LOWER"])
    )

    df.loc[buy_condition, "entry_signal"] = "BUY"
    df.loc[sell_condition, "entry_signal"] = "SELL"

    return df