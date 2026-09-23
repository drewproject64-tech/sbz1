from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔎 Search Channels", callback_data="search")],
            [InlineKeyboardButton(text="📂 Browse Channels", callback_data="browse")],
            [InlineKeyboardButton(text="⭐ Featured Channels", callback_data="featured")],
        ]
    )


def back_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Main Menu", callback_data="main")]
        ]
    )


def categories_menu(categories: list[str]) -> InlineKeyboardMarkup:
    rows = [
        [InlineKeyboardButton(text=f"📁 {category}", callback_data=f"cat:{category}")]
        for category in categories
    ]
    rows.append([InlineKeyboardButton(text="⬅️ Main Menu", callback_data="main")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def search_result_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Search Again", callback_data="search")],
            [InlineKeyboardButton(text="⬅️ Main Menu", callback_data="main")],
        ]
    )
