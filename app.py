import os
import handlers
from aiogram import executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from data import config
from loader import dp, db, bot
import filters
import logging

filters.setup(dp)

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.environ.get("PORT", 5000))
user_message = "User"
admin_message = "Admin"


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row(user_message, admin_message)

    await message.answer(
        """🎨 <b>Welcome to SUPERLUXE</b> 🎨

🤖 Your exclusive gateway to fine art and Web3 innovations.

🛍️ <a href="https://superluxe.io/collections/">Explore our curated collections</a> using the /menu command.

💰 <a href="https://superluxe.io/artx-token/">Purchase using $ARTX tokens</a> or traditional payment methods.

❓ Questions? Use /sos to connect with our art specialists.

🌟 <i>"Where Fine Art Meets Web3"</i>
    """,
        reply_markup=markup,
    )


@dp.message_handler(text=user_message)
async def user_mode(message: types.Message):
    cid = message.chat.id
    if cid in config.ADMINS:
        config.ADMINS.remove(cid)

    await message.answer("User mode enabled.", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(text=admin_message)
async def admin_mode(message: types.Message):
    cid = message.chat.id
    if cid not in config.ADMINS:
        config.ADMINS.append(cid)

    await message.answer("Admin mode enabled.", reply_markup=ReplyKeyboardRemove())


async def on_startup(dp):
    logging.basicConfig(level=logging.INFO)
    db.create_tables()

    await bot.delete_webhook()
    if config.WEBHOOK_URL:
        await bot.set_webhook(config.WEBHOOK_URL)


async def on_shutdown():
    logging.warning("Shutting down..")
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bot down")


if __name__ == "__main__":
    # Debug: Print ALL environment variables
    print("=== ENVIRONMENT VARIABLES ===")
    for key, value in os.environ.items():
        if 'BOT' in key or 'ADMIN' in key or 'RAILWAY' in key or 'WEBHOOK' in key:
            print(f"{key}: {value}")
        elif key in ['PATH', 'HOME', 'PWD']:
            continue  # Skip common env vars
        else:
            print(f"{key}: [SET]")

    print("\n=== CONFIG VALUES ===")
    print(f"BOT_TOKEN from config: {'***SET***' if config.BOT_TOKEN else 'NOT SET'}")
    print(f"ADMINS from config: {config.ADMINS}")
    print(f"WEBHOOK_URL from config: {config.WEBHOOK_URL}")

    # Exit if no token
    if not config.BOT_TOKEN:
        print("\n❌ ERROR: BOT_TOKEN not found! Check Railway environment variables.")
        exit(1)

    # Force polling mode for Railway (webhooks don't work in containers)
    if "RAILWAY_PUBLIC_DOMAIN" in os.environ:
        print("\n✅ Railway detected - using polling mode...")
        executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
    elif "HEROKU_APP_NAME" in os.environ:
        print("\n✅ Starting webhook mode for Heroku...")
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=config.WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
    else:
        print("\n✅ Starting polling mode...")
        executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
    elif "HEROKU_APP_NAME" in os.environ:
        print("Starting webhook mode for Heroku...")
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=config.WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
    else:
        print("Starting polling mode...")
        executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
