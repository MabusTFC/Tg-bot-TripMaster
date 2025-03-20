from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import json

# Токен вашего бота
BOT_TOKEN = "7172385372:AAETZ_QzAfjJIpZLLfHiLM0ZmDUJhi2_0GA"

# Команда /start
async def start(update: Update, context: CallbackContext):
    # Создаем кнопку для открытия Web App
    keyboard = [
        [InlineKeyboardButton("Открыть карту", web_app=WebAppInfo(url="https://c37f-162-19-19-218.ngrok-free.app"))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Нажмите кнопку, чтобы открыть карту:", reply_markup=reply_markup)

# Основная функция для запуска бота
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    #application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()