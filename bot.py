from telegram import Update
from telegram.ext import Application, CommandHandler
from pytonlib import TonlibClient

TOKEN = "7753390143:AAHj_SalBwNYe6-hO4DdK7Qqlt8aK8fvgeQ"

# Инициализация TON клиента
client = TonlibClient(ls_index=0, config="https://ton.org/global-config-testnet.json")
client.init()

# Создание нового кошелька
def create_wallet():
    wallet = client.create_wallet()
    return wallet["address"], wallet["mnemonic"]

# Команда /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я тестнет-бот для TON.")

# Команда /new_wallet
async def new_wallet(update: Update, context):
    address, mnemonic = create_wallet()
    await update.message.reply_text(f"Новый кошелёк создан!\nАдрес: {address}\nСекретная фраза: {' '.join(mnemonic)}")

# Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("new_wallet", new_wallet))

    app.run_polling()

if __name__ == "__main__":
    main()
