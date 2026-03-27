import MetaTrader5 as mt5
from data_loader import get_data
from strategy import add_indicators, generate_trend_signals, generate_entry_signals


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
        df = generate_trend_signals(df)
        df = generate_entry_signals(df)

        print(
            df[
                [
                    "datetime",
                    "close",
                    "SMA20",
                    "SMA50",
                    "RSI",
                    "BB_UPPER",
                    "BB_LOWER",
                    "trend_signal",
                    "bollinger_context",
                    "entry_signal",
                ]
            ].tail(15)
        )

        last_row = df.iloc[-1]
        print("\nLatest candle analysis:")
        print(f"Close: {last_row['close']}")
        print(f"SMA20: {last_row['SMA20']}")
        print(f"SMA50: {last_row['SMA50']}")
        print(f"RSI: {last_row['RSI']}")
        print(f"Bollinger context: {last_row['bollinger_context']}")
        print(f"Trend signal: {last_row['trend_signal']}")
        print(f"Entry signal: {last_row['entry_signal']}")

    except Exception as e:
        print("Error:", e)

    finally:
        mt5.shutdown()


if __name__ == "__main__":
    main()