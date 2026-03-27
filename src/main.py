import MetaTrader5 as mt5
from data_loader import get_data
from strategy import add_indicators, generate_signals


SYMBOL = "EURUSD"
TIMEFRAME = mt5.TIMEFRAME_M5
NB_BARS = 200


def connect_mt5():
    if not mt5.initialize():
        error = mt5.last_error()
        raise RuntimeError(f"MT5 initialization failed: {error}")

    print(f"Connected to MT5 - version: {mt5.version()}")


def main():
    try:
        connect_mt5()

        df = get_data(SYMBOL, TIMEFRAME, NB_BARS)
        df = add_indicators(df)
        df = generate_signals(df)

        print(df.tail(10))

    except Exception as e:
        print("Error:", e)

    finally:
        mt5.shutdown()


if __name__ == "__main__":
    main()