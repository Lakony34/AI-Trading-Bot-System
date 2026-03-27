import MetaTrader5 as mt5
import pandas as pd


SYMBOL = "EURUSD"
TIMEFRAME = mt5.TIMEFRAME_M5
NB_BARS = 200


def connect_mt5():
    if not mt5.initialize():
        error = mt5.last_error()
        raise RuntimeError(f"MT5 initialization failed: {error}")

    print(f"Connected to MT5 - version: {mt5.version()}")


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


def main():
    try:
        connect_mt5()
        df = get_data(SYMBOL, TIMEFRAME, NB_BARS)
        print(df.tail())
    except Exception as e:
        print("Error:", e)
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    main()