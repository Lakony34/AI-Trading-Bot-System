# Risk management
import MetaTrader5 as mt5


def get_account_balance():
    account_info = mt5.account_info()
    if account_info is None:
        raise RuntimeError("Failed to get account info")
    return account_info.balance


def calculate_lot_size(symbol: str, risk_percent: float, sl_pips: float):
    balance = get_account_balance()

    risk_amount = balance * (risk_percent / 100)

    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        raise ValueError(f"Symbol '{symbol}' not found.")

    # Valeur approximative du pip (Forex standard)
    pip_value_per_lot = 10  # EURUSD ≈ 10$ par pip pour 1 lot

    lot_size = risk_amount / (sl_pips * pip_value_per_lot)

    # Arrondi au minimum autorisé
    lot_size = max(symbol_info.volume_min, round(lot_size, 2))

    return lot_size