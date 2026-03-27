import os
import sqlite3


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
            ticket INTEGER
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