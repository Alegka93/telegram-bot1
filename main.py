from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

from keep_alive import keep_alive  # 👈 запуск Flask-сервера
keep_alive()  # 👈 активує сервер

TOKEN = "ВСТАВ_СВІЙ_ТОКЕН_ТУТ"
ADMIN_ID = 123456789  # заміни на свій Telegram ID

user_data = {}

# Обробник команди /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я твій бот.")

# Основна функція
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))

print("Бот запущено!")
app.run_polling()
