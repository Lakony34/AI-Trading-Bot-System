# AI Trading Bot (MT5)

This project aims to build a fully automated trading bot powered by AI, focused on intraday trading with future scalping expansion.

## Trading Scope
- Market: Forex
- Instrument: EURUSD
- Timeframe: Intraday (scalping extension planned)
- Broker: MetaTrader 5 (MT5)
- Type: Signal generation + automated execution

---

## Objectives
- Retrieve real-time and historical market data from MT5
- Analyze price action and technical indicators
- Generate high-probability trading signals (BUY / SELL / HOLD)
- Execute trades automatically via MT5 API
- Implement strict risk management rules
- Continuously improve performance using AI models

---

## Technologies
- Python
- MetaTrader5 (MT5 API)
- Pandas / NumPy
- Machine Learning (future integration)
- Data analysis & visualization

---

## Core Features
- Market data collection (OHLCV)
- Technical indicators (SMA, RSI, etc.)
- Signal generation engine
- Trade execution via MT5
- Risk management system (SL, TP, position sizing)
- Backtesting module (planned)
- Performance tracking (planned)7- Trend detection using SMA 20 / SMA 50
- Entry signal generation based on moving average crossovers
- RSI confirmation
- Bollinger Bands market context detection
- Filtered entry signals to reduce false trades
- Basic execution decision layer to prevent duplicate trades
- Open position check before any order action

---

## Project Structure
src/
│── main.py              # Entry point
│── data_loader.py       # MT5 data retrieval
│── indicators.py        # Technical indicators
│── strategy.py          # Signal logic
│── execution.py         # Trade execution (MT5)
│── risk_manager.py      # Risk management
│── utils.py             # Helper functions

---

## Strategy (Initial Version)
The first version of the bot combines:
- SMA 20 / SMA 50 crossover
- RSI confirmation
- Bollinger Bands context analysis

Signal logic:
- Bullish SMA crossover → potential BUY
- Bearish SMA crossover → potential SELL
- RSI helps validate momentum
- Bollinger Bands help detect overbought / oversold price extension
- Signals are validated only on closed candles to avoid unstable entries

The system distinguishes between:
- trend signals
- entry signals
- market context

This provides a stronger and more realistic foundation before adding advanced execution logic or AI-based improvements.
The bot evaluates signals only on closed candles in order to reduce noise and avoid taking trades based on unfinished market data.
The bot includes a basic execution control layer that checks for existing open positions before validating a new trade action.

---

## Risk Management
- Fixed risk per trade
- Stop Loss & Take Profit mandatory
- Drawdown control
- Capital preservation priority

---

## Roadmap
- [ ] MT5 connection
- [ ] EURUSD data retrieval module
- [ ] Basic strategy implementation
- [ ] Backtesting system
- [ ] Trade execution automation
- [ ] AI integration
- [ ] Dashboard & monitoring

---

## Status
Project in development – building core trading infrastructure.

---

## Vision
Build a scalable, automated, and profitable EURUSD trading system combining algorithmic trading and artificial intelligence.