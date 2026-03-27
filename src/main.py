import MetaTrader5 as mt5
from data_loader import get_data
from strategy import add_indicators, generate_trend_signals, generate_entry_signals
from execution import evaluate_trade_action


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

        closed_candle = df.iloc[-2]

        print("\nLast closed candle analysis:")
        print(f"Datetime: {closed_candle['datetime']}")
        print(f"Close: {closed_candle['close']}")
        print(f"SMA20: {closed_candle['SMA20']}")
        print(f"SMA50: {closed_candle['SMA50']}")
        print(f"RSI: {closed_candle['RSI']}")
        print(f"Bollinger context: {closed_candle['bollinger_context']}")
        print(f"Trend signal: {closed_candle['trend_signal']}")
        print(f"Entry signal: {closed_candle['entry_signal']}")

        action = evaluate_trade_action(SYMBOL, closed_candle["entry_signal"])

        print(f"\nExecution decision: {action}")

    except Exception as e:
        print("Error:", e)

    finally:
        mt5.shutdown()


if __name__ == "__main__":
    main()