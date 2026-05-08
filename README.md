# Binance Futures Testnet Trading Bot

A simplified Python Command-Line Interface (CLI) application that places orders on the Binance Futures Testnet (USDT-M). This project features a clean, reusable structure, input validation, robust error handling, and structured logging.

## Features

- **Order Types**: Place `MARKET`, `LIMIT`, and `STOP_MARKET` (Bonus) orders.
- **Enhanced CLI**: Uses `Typer` and `Rich` for a colorful, structured, and user-friendly CLI experience.
- **Validation**: Strict input validation before any API requests are made.
- **Logging**: All API responses and errors are logged to `logs/trading_bot.log`.
- **Reusable Structure**: Clear separation of concerns between CLI, validation, API interaction, and logic.

## Prerequisites

- Python 3.9+
- A Binance Futures Testnet account.
- Testnet API Keys (API Key & Secret).

## Setup Instructions

1. **Clone or Extract the Repository:**
   Navigate to the project directory.

2. **Create a Virtual Environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Copy the example environment file and add your credentials:
   ```bash
   cp .env.example .env
   ```
   Open the `.env` file and replace the placeholders with your actual testnet `BINANCE_API_KEY` and `BINANCE_API_SECRET`.

## How to Run Examples

Use the `cli.py` script to interact with the bot.

### View Help
```bash
python cli.py --help
```

### Place a MARKET Order
Buy 0.001 BTCUSDT at the current market price:
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Place a LIMIT Order
Sell 0.001 BTCUSDT at a specific price (e.g., 90000.0):
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 90000.0
```

### Place a STOP_MARKET Order (Bonus Feature)
Place a stop-market order to sell 0.001 BTCUSDT if the price drops to 50000.0:
```bash
python cli.py --symbol BTCUSDT --side SELL --type STOP_MARKET --quantity 0.001 --stop-price 50000.0
```

## Assumptions Made

1. **Testnet Only**: The bot is hardcoded to connect to the Binance Futures Testnet (`https://testnet.binancefuture.com`). It will not place real orders.
2. **USDT-M Futures**: The validation assumes trading pairs ending in `USDT` (e.g., `BTCUSDT`). It does not support Coin-M futures.
3. **Good Till Cancelled (GTC)**: All LIMIT orders are placed with a `timeInForce` of `GTC`.
4. **Log Directory**: The application expects to be able to create a `logs` directory in the current working directory to store `trading_bot.log`.
