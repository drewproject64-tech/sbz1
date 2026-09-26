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
    clean = State()
    count = State()
    format_text = State()


def home_text() -> str:
    return (
        "<b>Word Tools Bot</b>\n\n"
        "Simple tools for working with text directly in Telegram.\n\n"
        "Choose a tool:"
    )


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(home_text(), reply_markup=main_menu())


@router.message(Command("help"))
async def help_command(message: Message) -> None:
    await message.answer(
        "<b>Word Tools Bot</b>\n\n"
        "Clean Text removes repeated spaces and blank lines.\n"
        "Count Text counts words, characters, and lines.\n"
        "Format Text changes text case.\n\n"
        "Choose a tool from the menu.",
        reply_markup=main_menu(),
    )


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Cancelled.", reply_markup=main_menu())


@router.callback_query(F.data == "main")
async def main_menu_callback(call: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await call.message.edit_text(home_text(), reply_markup=main_menu())
    await call.answer()


@router.callback_query(F.data == "clean")
async def clean_start(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(ToolState.clean)
    await call.message.edit_text(
        "<b>Clean Text</b>\n\n"
        "Send text to remove repeated spaces and blank lines.",
        reply_markup=back_menu(),
    )
    await call.answer()


@router.message(ToolState.clean)
async def clean_text(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not text:
        await message.answer("Please send text.", reply_markup=back_menu())
        return
    if len(text) > 4000:
        await message.answer("Please keep the text under 4,000 characters.", reply_markup=back_menu())
        return

    cleaned = "\n".join(
        " ".join(line.split()) for line in text.splitlines() if line.strip()
    )
    await state.clear()
    await message.answer(
        f"<b>Cleaned Text</b>\n\n<code>{escape(cleaned)}</code>",
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "count")
async def count_start(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(ToolState.count)
    await call.message.edit_text(
        "<b>Count Text</b>\n\n"
        "Send text to count words, characters, and lines.",
        reply_markup=back_menu(),
    )
    await call.answer()


@router.message(ToolState.count)
async def count_text(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not text:
        await message.answer("Please send text.", reply_markup=back_menu())
        return
    if len(text) > 4000:
        await message.answer("Please keep the text under 4,000 characters.", reply_markup=back_menu())
        return

    await state.clear()
    await message.answer(
        "<b>Text Count</b>\n\n"
        f"Characters: <b>{len(text)}</b>\n"
        f"Words: <b>{len(text.split())}</b>\n"
        f"Lines: <b>{len(text.splitlines())}</b>",
        reply_markup=main_menu(),
    )


@router.callback_query(F.data == "format")
async def format_start(call: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(ToolState.format_text)
    await call.message.edit_text(
        "<b>Format Text</b>\n\n"
        "Send the text you want to format.",
        reply_markup=back_menu(),
    )
    await call.answer()


@router.message(ToolState.format_text)
async def format_input(message: Message, state: FSMContext) -> None:
    text = (message.text or "").strip()
    if not text:
        await message.answer("Please send text.", reply_markup=back_menu())
        return
    if len(text) > 4000:
        await message.answer("Please keep the text under 4,000 characters.", reply_markup=back_menu())
        return

    await state.update_data(format_text=text)
    await message.answer("Choose a format:", reply_markup=format_menu())


@router.callback_query(F.data.startswith("fmt:"))
async def format_apply(call: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    text = data.get("format_text")

    if not text:
        await state.clear()
        await call.message.edit_text(home_text(), reply_markup=main_menu())
        await call.answer("Please start again.")
        return

    mode = call.data.split(":", 1)[1]
    result = {
        "upper": text.upper(),
        "lower": text.lower(),
        "title": text.title(),
    }.get(mode)

    if result is None:
        await call.answer("Unknown format.")
        return

    await state.clear()
    await call.message.edit_text(
        f"<b>Formatted Text</b>\n\n<code>{escape(result)}</code>",
        reply_markup=main_menu(),
    )
    await call.answer()
