import MetaTrader5 as mt5

print("TEST SCRIPT STARTED")

SYMBOL = "EURUSD"
LOT_SIZE = 0.01
DEVIATION = 20
MAGIC_NUMBER = 20260327


def connect_mt5():
    if not mt5.initialize():
        raise RuntimeError(f"MT5 initialization failed: {mt5.last_error()}")

    print(f"Connected to MT5 - version: {mt5.version()}")


def get_supported_filling_modes():
    return [
        ("RETURN", mt5.ORDER_FILLING_RETURN),
        ("IOC", mt5.ORDER_FILLING_IOC),
        ("FOK", mt5.ORDER_FILLING_FOK),
    ]


def send_test_buy_order(symbol: str, volume: float):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        raise ValueError(f"Symbol '{symbol}' not found.")

    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            raise RuntimeError(f"Failed to select symbol '{symbol}'.")

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        raise RuntimeError(f"Failed to get tick data for '{symbol}'.")

    price = tick.ask
    print(f"Sending BUY at price: {price}")

    last_result = None

    for filling_name, filling_mode in get_supported_filling_modes():
        print(f"\nTrying filling mode: {filling_name}")

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "deviation": DEVIATION,
            "magic": MAGIC_NUMBER,
            "comment": f"test buy order ({filling_name})",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": filling_mode,
        }

        check = mt5.order_check(request)
        print("Order check result:", check)

        result = mt5.order_send(request)
        print("Order send result:", result)

        last_result = result

        if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"\n✅ ORDER EXECUTED SUCCESSFULLY with filling mode: {filling_name}")
            return result

        if result is not None:
            print(f"❌ Failed with retcode: {result.retcode}")

    raise RuntimeError(f"All filling modes failed. Last result: {last_result}")


def main():
    try:
        connect_mt5()
        send_test_buy_order(SYMBOL, LOT_SIZE)
    except Exception as e:
        print("Error:", e)
    finally:
        mt5.shutdown()


if __name__ == "__main__":
    main()