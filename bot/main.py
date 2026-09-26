import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from .config import BOT_TOKEN
from .handlers import router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

BOT_NAME = "Word Tools Bot"
BOT_SHORT_DESCRIPTION = "Simple word and text tools for Telegram."
BOT_DESCRIPTION = (
    "Word Tools Bot provides three simple text functions directly in Telegram: "
    "clean text, count words and characters, and change text case."
)


async def main() -> None:
    bot = Bot(
        BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    await bot.set_my_name(name=BOT_NAME)
    await bot.set_my_short_description(short_description=BOT_SHORT_DESCRIPTION)
    await bot.set_my_description(description=BOT_DESCRIPTION)
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Open the text tools"),
            BotCommand(command="help", description="View available tools"),
            BotCommand(command="cancel", description="Cancel the current tool"),
        ]
    )

    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("%s is starting", BOT_NAME)

    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
