from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from keep_alive import keep_alive  # 👈 запуск Flask-сервера
keep_alive()  # 👈 активує сервер

TOKEN = "7847656840:AAEoG9zSN9gCmJ25VHzmzqOXtlO7aV14_TI"
ADMIN_ID = 486443841  # заміни на свій Telegram ID

user_data = {}

# Обробник команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я твій бот.")

# Основна функція
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Бот запущено!")
app.run_polling()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📲 Залишити заявку", "📍 Локація сервісу"],
                ["💬 Зв’язок з майстром"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "Привіт! Я бот для запису на ремонт iPhone 📱",
        reply_markup=reply_markup)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📲 Залишити заявку":
        await update.message.reply_text("Введи модель iPhone:")
        user_data[update.effective_user.id] = {"step": "model"}
    elif text == "📍 Локація сервісу":
        await update.message.reply_text(
            "Наша адреса: 📍 м. Львів, вул. Мельника 18 Leoland ")
    elif text == "💬 Зв’язок з майстром":
        await update.message.reply_text("Напиши нам у Telegram: @Enforcer1")
    else:
        uid = update.effective_user.id
        if uid in user_data:
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
                data = user_data[uid]
                message = (
                    f"📥 Нова заявка від @{update.effective_user.username or 'Користувач без username'}\n\n"
                    f"📱 Модель: {data['model']}\n"
                    f"⚠️ Проблема: {data['problem']}\n"
                    f"📞 Телефон: {data['phone']}")
                await context.bot.send_message(chat_id=ADMIN_ID, text=message)
                await update.message.reply_text(
                    "✅ Дякуємо! Майстер скоро зв’яжеться з тобою.")
                del user_data[uid]


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,
                               handle_message))
app.run_polling()
