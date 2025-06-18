import logging
import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from keep_alive import keep_alive

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int os.getenv (486443841)  # ← перетворення в int

keep_alive()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

user_data = {}

def get_start_keyboard():
    return ReplyKeyboardMarkup(keyboard=[["🚀 Почати ремонт"]], resize_keyboard=True)

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            ["📲 Залишити заявку", "📍 Локація сервісу"],
            ["💬 Зв’язок з майстром"]
        ],
        resize_keyboard=True
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"User {update.effective_user.id} started the bot.")
    await update.message.reply_text(
        "Привіт! Я бот для запису на ремонт iPhone 📱",
        reply_markup=get_main_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    uid = update.effective_user.id

    if text == "🚀 Почати ремонт":
        return await start(update, context)

    if text == "📲 Залишити заявку":
        user_data[uid] = {"step": "model"}
        await update.message.reply_text("Введи модель iPhone:")

    elif text == "📍 Локація сервісу":
        await update.message.reply_text("Наша адреса: 📍 м. Львів, вул. Мельника 18 Leoland 🏛️")

    elif text == "💬 Зв’язок з майстром":
        await update.message.reply_text("Напиши нам у Telegram: @Enforcer1")

    else:
        if uid not in user_data:
            await update.message.reply_text(
                "Натисни кнопку нижче для запуску 👇",
                reply_markup=get_start_keyboard()
            )
            return

        step = user_data[uid].get("step")

        if step == "model":
            user_data[uid]["model"] = text
            user_data[uid]["step"] = "problem"
            await update.message.reply_text("Опиши проблему з iPhone:")

        elif step == "problem":
            user_data[uid]["problem"] = text
            user_data[uid]["step"] = "phone"
            await update.message.reply_text("Введи свій номер телефону:")

        elif step == "phone":
            user_data[uid]["phone"] = text
            data = user_data.pop(uid)

            username = update.effective_user.username or "Користувач без username"
            message = (
                f"📥 Нова заявка від @{username}\n\n"
                f"📱 Модель: {data['model']}\n"
                f"⚠️ Проблема: {data['problem']}\n"
                f"📞 Телефон: {data['phone']}"
            )
            await context.bot.send_message(chat_id=ADMIN_ID, text=message)
            await update.message.reply_text(
                "✅ Дякуємо! Майстер скоро зв’яжеться з тобою.",
                reply_markup=get_main_keyboard()
            )
        else:
            user_data.pop(uid, None)
            await update.message.reply_text(
                "Сталася помилка. Будь ласка, почни заново /start",
                reply_markup=get_main_keyboard()
            )

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    if update and hasattr(update, "message") and update.message:
        await update.message.reply_text("Сталася помилка. Спробуйте ще раз пізніше.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    print("Бот запущено!")
    app.run_polling()
