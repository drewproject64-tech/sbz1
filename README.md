# Word Tools Bot

Word Tools Bot is a simple Telegram utility with three text functions:

- Clean Text — removes repeated spaces and blank lines.
- Count Text — counts words, characters, and lines.
- Format Text — converts text to uppercase, lowercase, or title case.

The bot performs its functions directly in Telegram. It has no external website, landing page, redirects, channels, promotions, payments, gambling, betting, gaming, or financial features.

## Setup

1. Copy `.env.example` to `.env`.
2. Set `BOT_TOKEN`.
3. Install dependencies with `pip install -r requirements.txt`.
4. Start with `python -m bot.main`.

## Render

Deploy the repository as a Docker worker and set `BOT_TOKEN` as a secret environment variable.
