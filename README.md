# SB24GZ - Clear Channels

A simple Telegram-native channel discovery bot with exactly three core user functions:

1. Search Channels
2. Browse Channels
3. Featured Channels

## Local setup

1. Copy `.env.example` to `.env`.
2. Set `BOT_TOKEN`.
3. Install dependencies: `pip install -r requirements.txt`
4. Start the bot: `python -m bot.main`

SQLite is created automatically.

## Render

Deploy as a worker using the included `render.yaml` and set `BOT_TOKEN` as a secret environment variable.

The core user experience works directly inside Telegram and does not require an external website.
