import os
import sqlite3
import MetaTrader5 as mt5
from datetime import datetime


DB_PATH = "data/trading_bot.db"


def get_connection():
    os.makedirs("data", exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trade_time TEXT NOT NULL,
        symbol TEXT NOT NULL,
        order_type TEXT NOT NULL,
        volume REAL NOT NULL,
        entry_price REAL NOT NULL,
        stop_loss REAL,
        take_profit REAL,
        trend_signal TEXT,
        entry_signal TEXT,
        rsi REAL,
        sma20 REAL,
        sma50 REAL,
        bollinger_context TEXT,
        status TEXT NOT NULL,
        ticket INTEGER,
        exit_time TEXT,
        exit_price REAL,
        profit REAL,
        outcome TEXT
    )
""")

    conn.commit()
    conn.close()


def log_trade(
    trade_time,
    symbol,
    order_type,
    volume,
    entry_price,
    stop_loss,
    take_profit,
    trend_signal,
    entry_signal,
    rsi,
    sma20,
    sma50,
    bollinger_context,
    status,
    ticket,
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO trades (
            trade_time,
            symbol,
            order_type,
            volume,
            entry_price,
            stop_loss,
            take_profit,
            trend_signal,
            entry_signal,
            rsi,
            sma20,
            sma50,
            bollinger_context,
            status,
            ticket
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        str(trade_time),
        symbol,
        order_type,
        volume,
        entry_price,
        stop_loss,
        take_profit,
        trend_signal,
        entry_signal,
        rsi,
        sma20,
        sma50,
        bollinger_context,
        status,
        ticket,
    ))

    conn.commit()
    conn.close()

def update_trade_closure(ticket, exit_time, exit_price, profit):
    conn = get_connection()
    cursor = conn.cursor()

    outcome = "BREAKEVEN"
    if profit > 0:
        outcome = "WIN"
    elif profit < 0:
        outcome = "LOSS"

    cursor.execute("""
        UPDATE trades
        SET
            status = ?,
            exit_time = ?,
            exit_price = ?,
            profit = ?,
            outcome = ?
        WHERE ticket = ? AND status = 'OPEN'
    """, (
        "CLOSED",
        str(exit_time),
        exit_price,
        profit,
        outcome,
        ticket,
    ))

    conn.commit()
    conn.close()

def sync_closed_trades():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT ticket FROM trades WHERE status = 'OPEN'")
    open_db_trades = cursor.fetchall()

    current_positions = mt5.positions_get()
    current_position_tickets = set()

    if current_positions is not None:
        current_position_tickets = {position.ticket for position in current_positions}

    for row in open_db_trades:
        ticket = row[0]

        if ticket not in current_position_tickets:
            deals = mt5.history_deals_get(position=ticket)

            if deals is not None and len(deals) > 0:
                last_deal = deals[-1]

                update_trade_closure(
                    ticket=ticket,
                    exit_time=datetime.fromtimestamp(last_deal.time),
                    exit_price=last_deal.price,
                    profit=last_deal.profit,
                )

    conn.close()