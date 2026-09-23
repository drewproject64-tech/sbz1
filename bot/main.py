import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from .config import BOT_TOKEN
from .db import init_db, seed_demo_data
from .handlers import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


async def main() -> None:
    await init_db()
    await seed_demo_data()

    bot = Bot(
        BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Open the main menu"),
            BotCommand(command="help", description="Learn how the bot works"),
            BotCommand(command="cancel", description="Cancel the current action"),
        ]
    )

    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("SB24GZ bot is starting")

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
