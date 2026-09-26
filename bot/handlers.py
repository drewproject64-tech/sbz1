from __future__ import annotations

from html import escape

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

from .keyboards import back_menu, format_menu, main_menu

router = Router()


class ToolState(StatesGroup):
    waiting_clean = State()
    waiting_count = State()
    waiting_format = State()


def home_text() -> str:
    return (
        "<b>SB24GZ Word Bot</b>\n\n"
        "Simple word and text tools that work directly inside Telegram.\n\n"
        "Choose a tool:"
    )


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(home_text(), reply_markup=main_menu())


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(
        "<b>SB24GZ Word Bot</b>\n\n"
        "Clean Text removes extra spaces and blank lines.\n"
        "Count Text counts characters, words, and lines.\n"
        "Format Text changes text case.\n\n"
        "Send /start to open the tools.",
        reply_markup=main_menu(),
    )


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Cancelled. Choose a tool:", reply_markup=main_menu())


@router.callback_query(F.data == "main")
async def main_menu_callback(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.edit_text(home_text(), reply_markup=main_menu())
    await call.answer()


@router.callback_query(F.data == "clean")
async def clean_start(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(ToolState.waiting_clean)
    await call.message.edit_text(
        "<b>Clean Text</b>\n\n"
        "Send the text you want to clean. Extra spaces and blank lines will be removed.\n\n"
        "Use /cancel to stop.",
        reply_markup=back_menu(),
    )
    await call.answer()


@router.message(ToolState.waiting_clean)
async def clean_text(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not text:
        await message.answer("Please send some text.", reply_markup=back_menu())
        return
    if len(text) > 4000:
        await message.answer("Please keep the text under 4,000 characters.", reply_markup=back_menu())
        return

    cleaned = "\n".join(" ".join(line.split()) for line in text.splitlines() if line.strip())
    await state.clear()
    await message.answer(
        f"<b>Cleaned Text</b>\n\n<code>{escape(cleaned)}</code>",
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "count")
async def count_start(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(ToolState.waiting_count)
    await call.message.edit_text(
        "<b>Count Text</b>\n\n"
        "Send text to count characters, words, and lines.\n\n"
        "Use /cancel to stop.",
        reply_markup=back_menu(),
    )
    await call.answer()


@router.message(ToolState.waiting_count)
async def count_text(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not text:
        await message.answer("Please send some text.", reply_markup=back_menu())
        return

    characters = len(text)
    words = len(text.split())
    lines = len(text.splitlines())

    await state.clear()
    await message.answer(
        "<b>Text Count</b>\n\n"
        f"Characters: <b>{characters}</b>\n"
        f"Words: <b>{words}</b>\n"
        f"Lines: <b>{lines}</b>",
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "format")
async def format_start(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(ToolState.waiting_format)
    await call.message.edit_text(
        "<b>Format Text</b>\n\n"
        "Send the text you want to format, then choose a style.",
        reply_markup=back_menu(),
    )
    await call.answer()


@router.message(ToolState.waiting_format)
async def format_input(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not text:
        await message.answer("Please send some text.", reply_markup=back_menu())
        return
    if len(text) > 4000:
        await message.answer("Please keep the text under 4,000 characters.", reply_markup=back_menu())
        return

    await state.update_data(format_text=text)
    await message.answer("Choose a format:", reply_markup=format_menu())


@router.callback_query(F.data.startswith("fmt:"))
async def format_apply(call: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    text = data.get("format_text", "")

    if not text:
        await state.clear()
        await call.message.edit_text(home_text(), reply_markup=main_menu())
        await call.answer("Please start again.")
        return

    mode = call.data.split(":", 1)[1]
    if mode == "upper":
        result = text.upper()
    elif mode == "lower":
        result = text.lower()
    else:
        result = text.title()

    await state.clear()
    await call.message.edit_text(
        f"<b>Formatted Text</b>\n\n<code>{escape(result)}</code>",
        reply_markup=main_menu(),
    )
    await call.answer()
