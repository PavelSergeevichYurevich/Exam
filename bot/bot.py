import os
import dotenv
import logging

logging.basicConfig(level=logging.DEBUG, format='[{asctime}] #{levelname:8} {filename}:'
           '{lineno} - {name} - {message}',
           style='{'
)
logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('logs.log', mode='w')
logger.addHandler(file_handler)

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!')
    
if __name__ == '__main__':
    dp.run_polling(bot)