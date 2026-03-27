# MT5 data retrieval
import MetaTrader5 as mt5
import pandas as pd


def get_data(symbol: str, timeframe, nb_bars: int) -> pd.DataFrame:
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        raise ValueError(f"Symbol '{symbol}' not found in MT5.")

    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            raise RuntimeError(f"Failed to select symbol '{symbol}'.")

    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, nb_bars)
    if rates is None or len(rates) == 0:
        raise RuntimeError(f"No data retrieved for {symbol}. Error: {mt5.last_error()}")

    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df = df.rename(columns={"time": "datetime", "tick_volume": "volume"})

    return df[["datetime", "open", "high", "low", "close", "volume", "spread", "real_volume"]]