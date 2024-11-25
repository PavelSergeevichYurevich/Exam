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

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher()

user_dict: dict[int, dict[str, str | int | bool]] = {}
class FSMFillForm(StatesGroup):
    fill_username = State()
    fill_password = State()

button_reg = InlineKeyboardButton(
    text='Register',
    callback_data='button_reg_pressed'
)
button_show = InlineKeyboardButton(
    text='Show tasks',
    callback_data='button_show_pressed'
)
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_reg],
        [button_show]
    ]
)

@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(text = 'Привет!', reply_markup = keyboard)

@dp.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего',
        reply_markup = keyboard
    )

@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из процесса.',
        reply_markup = keyboard
    )
    await state.clear()
    
@dp.callback_query(F.data == 'button_reg_pressed', StateFilter(default_state))
async def process_button_reg_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Пожалуйста, введите ваше имя пользователя')
    await state.set_state(FSMFillForm.fill_username)

@dp.message(StateFilter(FSMFillForm.fill_username))
async def process_username_sent(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите ваш пароль')
    await state.set_state(FSMFillForm.fill_password)

@dp.message(StateFilter(FSMFillForm.fill_password))
async def process_password_sent(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    user_dict[message.from_user.id] = await state.get_data()
    await state.clear()
    button_show_data = InlineKeyboardButton(
        text='Посмотреть данные',
        callback_data='button_show_data_pressed'
    )
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_show_data],
    ]
)
    await message.answer(text='Спасибо! Ваши данные сохранены!', reply_markup=keyboard)

@dp.callback_query(F.data == 'button_show_data_pressed', StateFilter(default_state))
async def process_button_reg_press(callback: CallbackQuery):
    if callback.from_user.id in user_dict:
        await callback.answer(
            text=f'Имя: {user_dict[callback.from_user.id]["username"]}\n'
                f'Пароль: {user_dict[callback.from_user.id]["password"]}'
        )
    
if __name__ == '__main__':
    dp.run_polling(bot)