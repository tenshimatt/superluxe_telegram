from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp
from filters import IsAdmin, IsUser

catalog = "🎨 Art Collections"
balance = "💰 $ARTX Balance"
cart = "🛒 Art Cart"
delivery_status = "🚚 Order Status"

settings = "⚙️ Catalog Settings"
orders = "🚚 Orders"
questions = "❓ Questions"


@dp.message_handler(IsAdmin(), commands="menu")
async def admin_menu(message: Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(settings)
    markup.add(questions, orders)

    await message.answer("Menu", reply_markup=markup)


@dp.message_handler(IsUser(), commands="menu")
async def user_menu(message: Message):
    # Reply keyboard for bot functions
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(catalog)
    markup.add(balance, cart)
    markup.add(delivery_status)

    # Inline keyboard with website links
    inline_markup = InlineKeyboardMarkup()
    inline_markup.row(
        InlineKeyboardButton("🛍️ Shop Collections", url="https://superluxe.io/collections/"),
        InlineKeyboardButton("🎨 View Artists", url="https://superluxe.io/artists/")
    )
    inline_markup.row(
        InlineKeyboardButton("🏠 Art Rental", url="https://superluxe.io/art-rental/"),
        InlineKeyboardButton("💰 $ARTX Token", url="https://superluxe.io/artx-token/")
    )

    await message.answer("Menu", reply_markup=markup)
    await message.answer(
        "🌐 <b>Explore SUPERLUXE Online:</b>",
        reply_markup=inline_markup,
        parse_mode="HTML"
    )
