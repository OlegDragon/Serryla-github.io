from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# Вставьте сюда ваш токен от BotFather
TOKEN = "7753390143:AAHj_SalBwNYe6-hO4DdK7Qqlt8aK8fvgeQ"

# Функция для команды /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я ваш бот. Чем могу помочь?")

# Функция для ответа на текстовые сообщения
async def echo(update: Update, context):
    await update.message.reply_text(f"Вы написали: {update.message.text}")

# Главная функция
def main():
    # Создаем приложение
    application = Application.builder().token(TOKEN).build()

    # Обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()
