import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_IDS = {int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()}
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/sbz1.db").strip()

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is required.")
