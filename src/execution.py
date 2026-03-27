import MetaTrader5 as mt5


MAGIC_NUMBER = 20260327
DEVIATION = 20


def get_open_positions(symbol: str):
    positions = mt5.positions_get(symbol=symbol)
    if positions is None:
        return []
    return list(positions)


def has_open_position(symbol: str) -> bool:
    return len(get_open_positions(symbol)) > 0


def evaluate_trade_action(symbol: str, entry_signal: str) -> str:
    if entry_signal not in ["BUY", "SELL"]:
        return "NO_ACTION"

    if has_open_position(symbol):
        return "POSITION_ALREADY_OPEN"

    if entry_signal == "BUY":
        return "OPEN_BUY"

    if entry_signal == "SELL":
        return "OPEN_SELL"

    return "NO_ACTION"


def get_filling_modes():
    return [
        ("FOK", mt5.ORDER_FILLING_FOK),
        ("RETURN", mt5.ORDER_FILLING_RETURN),
        ("IOC", mt5.ORDER_FILLING_IOC),
    ]


def place_market_order(symbol: str, order_type: str, volume: float):
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        raise ValueError(f"Symbol '{symbol}' not found.")

    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            raise RuntimeError(f"Failed to select symbol '{symbol}'.")

    tick = mt5.symbol_info_tick(symbol)
    if tick is None:
        raise RuntimeError(f"Failed to get tick data for '{symbol}'.")

    if order_type == "BUY":
        mt5_order_type = mt5.ORDER_TYPE_BUY
        price = tick.ask
    elif order_type == "SELL":
        mt5_order_type = mt5.ORDER_TYPE_SELL
        price = tick.bid
    else:
        raise ValueError("order_type must be 'BUY' or 'SELL'.")

    last_result = None

    for filling_name, filling_mode in get_filling_modes():
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": mt5_order_type,
            "price": price,
            "deviation": DEVIATION,
            "magic": MAGIC_NUMBER,
            "comment": f"python mt5 bot order ({filling_name})",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": filling_mode,
        }

        check_result = mt5.order_check(request)
        print(f"Order check [{filling_name}]:", check_result)

        result = mt5.order_send(request)
        print(f"Order send [{filling_name}]:", result)

        last_result = result

        if result is not None and result.retcode == mt5.TRADE_RETCODE_DONE:
            print(f"Order executed successfully with filling mode: {filling_name}")
            return result

    raise RuntimeError(f"All filling modes failed. Last result: {last_result}")