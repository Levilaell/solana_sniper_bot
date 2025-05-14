# 🔫 Solana Token Sniper Bot

This is an automated bot that monitors a Telegram channel for newly launched Solana token addresses and automatically attempts to purchase them using the Jupiter Aggregator API.

## 🚀 Features

- ✅ Monitors a specific Telegram channel for token mentions
- ✅ Extracts Solana token addresses from messages
- ✅ Validates token support via Jupiter
- ✅ Fetches real-time swap quotes
- ✅ Automatically executes token swaps with SOL
- ✅ Uses `solders`, `solana-py`, and `httpx` for high performance and reliability
- ✅ Logs all events to the console
- ✅ Keypair stored securely as JSON file

---

## 🧠 Requirements

- Python 3.10+
- A funded Solana wallet (stored in `keypair.json`)
- A Telegram account with access to the monitored channel

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/solana-sniper-bot.git
cd solana-sniper-bot
```

### 2. Install dependencies

It’s recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 3. Add your wallet

Place your Solana keypair as a JSON file at the project root:

```text
./keypair.json
```

This is the same format used by Phantom, Sollet, Solana CLI, etc.

### 4. Configure the bot

Edit `config.json`:

```json
{
  "telegram": {
    "api_id": "YOUR_TELEGRAM_API_ID",
    "api_hash": "YOUR_API_HASH",
    "channel_id": "YOUR_TARGET_CHANNEL_ID"
  },
  "jupiter": {
    "api_url": "https://quote-api.jup.ag/v6",
    "rpc_endpoint": "https://api.mainnet-beta.solana.com",
    "amount": 0.1,
    "slippageBps": 50
  }
}
```

You can get your `api_id` and `api_hash` from [my.telegram.org](https://my.telegram.org).

---

## ▶️ Running the Bot

```bash
python main.py
```

Once started, the bot will listen to the configured Telegram channel and initiate swaps for supported tokens as soon as they are detected.

---

## 📁 Project Structure

```
solana-sniper-bot/
├── config.json              # Main configuration file
├── keypair.json             # Your wallet keypair
├── main.py                  # Entry point
├── jupiter.py               # Jupiter quote + swap logic
├── tg_listener.py           # Telegram listener
├── parser.py                # Token address extractor
├── wallet.py                # Wallet/keypair loader
├── config_manager.py        # Configuration loader
├── logger_setup.py          # Logging configuration
├── get_chat_id.py           # Utility to find Telegram chat ID
└── README.md                # This file
```

---

## 🛡️ Disclaimer

This project is provided for educational purposes. Use it at your own risk. The crypto market is volatile and highly speculative. Always test with small amounts and monitor your transactions.

---

## 📄 License

MIT License
# solana_sniper_bot
