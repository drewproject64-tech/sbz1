from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧹 Clean Text", callback_data="clean")],
            [InlineKeyboardButton(text="🔢 Count Text", callback_data="count")],
            [InlineKeyboardButton(text="🔤 Format Text", callback_data="format")],
        ]
    )


def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Main Menu", callback_data="main")]
        ]
    )


def format_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="UPPERCASE", callback_data="fmt:upper")],
            [InlineKeyboardButton(text="lowercase", callback_data="fmt:lower")],
            [InlineKeyboardButton(text="Title Case", callback_data="fmt:title")],
            [InlineKeyboardButton(text="⬅️ Main Menu", callback_data="main")],
        ]
    )
