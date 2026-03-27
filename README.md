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
- Performance tracking (planned)

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
The first version of the bot will be based on simple and reliable technical strategies:
- Moving Average crossover (SMA 20 / SMA 50)
- Trend-following logic
- Clear BUY / SELL / HOLD signals

This serves as a foundation before integrating more advanced AI models.

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