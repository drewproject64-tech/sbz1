from __future__ import annotations

import logging

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from .db import SessionLocal, Channel, get_channels, list_categories, search_channels
from .keyboards import back_menu, categories_menu, main_menu, search_result_menu

router = Router()
logger = logging.getLogger(__name__)


class SearchState(StatesGroup):
    waiting_query = State()


def channel_text(channel: Channel, index: int | None = None) -> str:
    prefix = f"{index}. " if index is not None else ""
    return (
        f"{prefix}📺 <b>{channel.name}</b>\n"
        f"{channel.description}\n"
        f"<b>Category:</b> {channel.category}"
    )


async def show_home(message: Message) -> None:
    await message.answer(
        "👋 <b>Welcome to SB24GZ - Clear Channels</b>\n\n"
        "Discover and explore useful Telegram channels from one simple directory.\n\n"
        "Choose an option below:",
        reply_markup=main_menu(),
    )


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await show_home(message)


@router.message(Command("help"))
async def help_cmd(message: Message) -> None:
    await message.answer(
        "ℹ️ <b>How SB24GZ works</b>\n\n"
        "• Search Channels — find channels by name, topic, or category.\n"
        "• Browse Channels — explore channels by category.\n"
        "• Featured Channels — view selected channels.\n\n"
        "The core features work directly inside Telegram.",
        reply_markup=main_menu(),
    )


@router.message(Command("cancel"))
async def cancel_cmd(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("✅ Cancelled.", reply_markup=main_menu())


@router.callback_query(F.data == "main")
async def cb_main(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    try:
        await call.message.edit_text(
            "👋 <b>Welcome to SB24GZ - Clear Channels</b>\n\n"
            "Discover and explore useful Telegram channels from one simple directory.\n\n"
            "Choose an option below:",
            reply_markup=main_menu(),
        )
    except TelegramBadRequest:
        await call.message.answer(
            "👋 <b>Welcome to SB24GZ - Clear Channels</b>\n\n"
            "Discover and explore useful Telegram channels from one simple directory.",
            reply_markup=main_menu(),
        )
    await call.answer()


@router.callback_query(F.data == "search")
async def cb_search(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(SearchState.waiting_query)
    await call.message.edit_text(
        "🔎 <b>Search Channels</b>\n\n"
        "Enter a keyword such as <code>technology</code>, <code>sports</code>, "
        "or <code>education</code>.\n\n"
        "Use /cancel to stop searching.",
        reply_markup=back_menu(),
    )
    await call.answer()


@router.message(SearchState.waiting_query)
async def process_search(message: Message, state: FSMContext) -> None:
    query = (message.text or "").strip()
    if not query:
        await message.answer(
            "Please enter a search keyword.",
            reply_markup=back_menu(),
        )
        return

    if len(query) > 80:
        await message.answer(
            "Please keep your search to 80 characters or fewer.",
            reply_markup=back_menu(),
        )
        return

    async with SessionLocal() as session:
        results = await search_channels(session, query)

    await state.clear()

    if not results:
        await message.answer(
            f'No channels found for "<b>{query}</b>". Try another keyword.',
            reply_markup=search_result_menu(),
        )
        return

    body = [f"🔎 <b>Search results for:</b> {query}", ""]
    for index, channel in enumerate(results, 1):
        body.append(channel_text(channel, index))
        body.append("")

    await message.answer(
        "\n".join(body),
        reply_markup=search_result_menu(),
    )


@router.callback_query(F.data == "browse")
async def cb_browse(call: CallbackQuery) -> None:
    async with SessionLocal() as session:
        categories = await list_categories(session)

    if not categories:
        text = "📂 <b>Browse Channels</b>\n\nNo categories are available yet."
        markup = back_menu()
    else:
        text = "📂 <b>Browse Channels</b>\n\nChoose a category:"
        markup = categories_menu(categories)

    await call.message.edit_text(text, reply_markup=markup)
    await call.answer()


@router.callback_query(F.data.startswith("cat:"))
async def cb_category(call: CallbackQuery) -> None:
    category = call.data.split(":", 1)[1]

    async with SessionLocal() as session:
        results = await get_channels(session, category=category)

    if not results:
        text = (
            f"📂 <b>{category}</b>\n\n"
            "No channels are available in this category yet."
        )
    else:
        body = [f"📂 <b>{category}</b>", ""]
        for index, channel in enumerate(results, 1):
            body.append(channel_text(channel, index))
            body.append("")
        text = "\n".join(body)

    await call.message.edit_text(text, reply_markup=back_menu())
    await call.answer()


@router.callback_query(F.data == "featured")
async def cb_featured(call: CallbackQuery) -> None:
    async with SessionLocal() as session:
        results = await get_channels(session, featured=True)

    if not results:
        text = "⭐ <b>Featured Channels</b>\n\nNo featured channels are available yet."
    else:
        body = ["⭐ <b>Featured Channels</b>", ""]
        for index, channel in enumerate(results, 1):
            body.append(channel_text(channel, index))
            body.append("")
        text = "\n".join(body)

    await call.message.edit_text(text, reply_markup=back_menu())
    await call.answer()


@router.callback_query()
async def unknown_callback(call: CallbackQuery) -> None:
    await call.answer(
        "This menu is no longer active. Please open the main menu.",
        show_alert=True,
    )
