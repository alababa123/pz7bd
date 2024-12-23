from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import Message
from database import init_db, log_message
from datetime import datetime

API_TOKEN = "ВАШ_ТОКЕН"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Инициализация базы данных
init_db()

@dp.message_handler(commands=["start", "help"])
async def handle_commands(message: Message):
    log_message(
        user_id=message.from_user.id,
        username=message.from_user.username,
        message=message.text,
        command=message.text.split()[0],
        date=datetime.now().strftime("%Y-%m-%d")
    )
    await message.reply(f"Вы вызвали команду: {message.text}")

@dp.message_handler()
async def handle_messages(message: Message):
    log_message(
        user_id=message.from_user.id,
        username=message.from_user.username,
        message=message.text,
        command=None,
        date=datetime.now().strftime("%Y-%m-%d")
    )
    await message.reply("Ваше сообщение сохранено.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)