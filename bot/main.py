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

BOT_NAME = "SB24GZ Word Bot"
BOT_SHORT_DESCRIPTION = "Word and text tools for cleaning, counting, and formatting text in Telegram."
BOT_DESCRIPTION = (
    "SB24GZ Word Bot provides simple word and text tools directly inside Telegram. "
    "Use Clean Text to remove extra spaces and blank lines, Count Text to count "
    "characters, words, and lines, and Format Text to change text case."
)


async def main() -> None:
    bot = Bot(
        BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(router)

    await bot.set_my_name(name=BOT_NAME)
    await bot.set_my_short_description(short_description=BOT_SHORT_DESCRIPTION)
    await bot.set_my_description(description=BOT_DESCRIPTION)

    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Open SB24GZ Word Bot"),
            BotCommand(command="help", description="See the three text tools"),
            BotCommand(command="cancel", description="Cancel the current tool"),
        ]
    )

    await bot.delete_webhook(drop_pending_updates=True)
    logging.info("%s is starting", BOT_NAME)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
