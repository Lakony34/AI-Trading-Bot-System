# Trade execution (MT5)
import MetaTrader5 as mt5


def get_open_positions(symbol: str):
    positions = mt5.positions_get(symbol=symbol)
    if positions is None:
        return []
    return list(positions)


def has_open_position(symbol: str) -> bool:
    positions = get_open_positions(symbol)
    return len(positions) > 0


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