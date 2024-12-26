from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from ton import TonlibClient
import requests

TOKEN = "7753390143:AAHj_SalBwNYe6-hO4DdK7Qqlt8aK8fvgeQ"
TONCENTER_API_URL = "https://toncenter.com/api/v2/"
TONCENTER_API_KEY = "7929acef3401314e40e8e24ee0af20e75a9c954ac738459fc58555c5e4b1d650"

# Инициализация TON клиента
client = TonlibClient(ls_index=0, config="testnet.config.json")
client.init()

# Создание нового кошелька
def create_wallet():
    wallet = client.create_wallet()
    return wallet["address"], wallet["mnemonic"]

# Проверка баланса
def check_balance(address):
    url = f"{TONCENTER_API_URL}getAddressInformation"
    params = {
        "address": address,
        "api_key": TONCENTER_API_KEY
    }
    response = requests.get(url, params=params).json()
    return float(response["result"]["balance"]) / 1e9  # Конвертация нанотонов в TON

# Отправка монет
def send_transaction(wallet, to_address, amount):
    response = client.send_transaction(
        wallet=wallet,
        to_address=to_address,
        amount=int(amount * 1e9),  # Конвертация TON в нанотоны
    )
    return response

# Команда /start
async def start(update: Update, context):
    await update.message.reply_text("Привет! Я тестнет-бот для TON.")

# Команда /new_wallet
async def new_wallet(update: Update, context):
    address, mnemonic = create_wallet()
    await update.message.reply_text(f"Новый кошелёк создан!\nАдрес: {address}\nСекретная фраза: {' '.join(mnemonic)}")

# Команда /balance
async def balance(update: Update, context):
    if len(context.args) != 1:
        await update.message.reply_text("Использование: /balance <адрес>")
        return
    address = context.args[0]
    balance = check_balance(address)
    await update.message.reply_text(f"Баланс адреса {address}: {balance} TON")

# Команда /send
async def send(update: Update, context):
    if len(context.args) != 3:
        await update.message.reply_text("Использование: /send <кошелёк> <адрес> <сумма>")
        return
    wallet, to_address, amount = context.args
    response = send_transaction(wallet, to_address, float(amount))
    await update.message.reply_text(f"Транзакция отправлена! Ответ сети: {response}")

# Запуск бота
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("new_wallet", new_wallet))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("send", send))

    app.run_polling()

if __name__ == "__main__":
    main()
