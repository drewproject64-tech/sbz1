# SB24GZ Word Bot

SB24GZ Word Bot is a Telegram-native word and text utility bot with three practical tools:

1. Clean Text — removes extra spaces and blank lines.
2. Count Text — counts characters, words, and lines.
3. Format Text — converts text to uppercase, lowercase, or title case.

All processing happens directly inside Telegram. The bot does not redirect users to an external website.

## Local setup

1. Copy `.env.example` to `.env`.
2. Set `BOT_TOKEN`.
3. Install dependencies:
   `pip install -r requirements.txt`
4. Start:
   `python -m bot.main`

## Render

Deploy as a worker using `render.yaml` and set `BOT_TOKEN` as a secret environment variable.

## Telegram Ads destination checklist

The advertised destination is the SB24GZ Word Bot itself. Its advertised functions are implemented directly inside the bot, with no external landing page or redirect flow.
