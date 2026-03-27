import MetaTrader5 as mt5
from data_loader import get_data
from strategy import add_indicators, generate_trend_signals, generate_entry_signals, calculate_trade_levels
from execution import evaluate_trade_action, place_market_order

SYMBOL = "EURUSD"
TIMEFRAME = mt5.TIMEFRAME_M5
NB_BARS = 200
LOT_SIZE = 0.01


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
        df = calculate_trade_levels(df)

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
        print(f"Stop Loss: {closed_candle['stop_loss']}")
        print(f"Take Profit: {closed_candle['take_profit']}")

        action = evaluate_trade_action(SYMBOL, closed_candle["entry_signal"])
        print(f"\nExecution decision: {action}")

        if action == "OPEN_BUY":
            result = place_market_order(
                SYMBOL,
                "BUY",
                LOT_SIZE,
                closed_candle["stop_loss"],
                closed_candle["take_profit"],
            )
            print(f"BUY order sent successfully. Ticket: {result.order}")

        elif action == "OPEN_SELL":
            result = place_market_order(
                SYMBOL,
                "SELL",
                LOT_SIZE,
                closed_candle["stop_loss"],
                closed_candle["take_profit"],
            )
            print(f"SELL order sent successfully. Ticket: {result.order}")

        else:
             print("No order sent.")

    except Exception as e:
        print("Error:", e)

    finally:
        mt5.shutdown()


if __name__ == "__main__":
    main()