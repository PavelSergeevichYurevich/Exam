import os
import dotenv
import logging
import aiohttp

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
button_show_all = InlineKeyboardButton(
    text='Show all tasks',
    callback_data='button_show_all_pressed'
)
button_show_active = InlineKeyboardButton(
    text='Show all active tasks',
    callback_data='button_show_active_pressed'
)
button_show_closed = InlineKeyboardButton(
    text='Show all closed tasks',
    callback_data='button_show_closed_pressed'
)
keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_reg],
        [button_show_all],
        [button_show_active],
        [button_show_closed]
    ]
)

@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(text = 'Привет!', reply_markup = keyboard)

@dp.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы вышли из процесса.',
        reply_markup = keyboard
    )
    await state.clear()

@dp.callback_query(F.data == 'button_show_all_pressed')
async def process_button_show_all_press(callback: CallbackQuery):
    user_telegram_id = callback.from_user.id
    async with aiohttp.ClientSession() as session:
        response = await session.get(f'http://127.0.0.1:8000/task/show/{user_telegram_id}')
        text = await response.text()
        await callback.message.answer(text=text, reply_markup = keyboard)
        
@dp.callback_query(F.data == 'button_show_active_pressed')
async def process_button_show_all_press(callback: CallbackQuery):
    user_telegram_id = callback.from_user.id
    async with aiohttp.ClientSession() as session:
        response = await session.get(f'http://127.0.0.1:8000/task/showactive/{user_telegram_id}')
        text = await response.text()
        await callback.message.answer(text=text, reply_markup = keyboard)
        
@dp.callback_query(F.data == 'button_show_closed_pressed')
async def process_button_show_all_press(callback: CallbackQuery):
    user_telegram_id = callback.from_user.id
    async with aiohttp.ClientSession() as session:
        response = await session.get(f'http://127.0.0.1:8000/task/showclosed/{user_telegram_id}')
        text = await response.text()
        await callback.message.answer(text=text, reply_markup = keyboard)
        

@dp.callback_query(F.data == 'button_reg_pressed', StateFilter(default_state))
async def process_button_reg_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Пожалуйста, введите ваше имя пользователя или /cancel для отмены')
    await state.set_state(FSMFillForm.fill_username)

@dp.message(StateFilter(FSMFillForm.fill_username))
async def process_username_sent(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await message.answer(text='Спасибо!\n\nА теперь введите ваш пароль или /cancel для отмены')
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
    button_sent_data = InlineKeyboardButton(
        text='Зарегистрироваться',
        callback_data='button_sent_data_pressed'
    )
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [button_show_data],
        [button_sent_data]
    ]
)
    await message.answer(text='Спасибо! Ваши данные сохранены!', reply_markup=keyboard)

@dp.callback_query(F.data == 'button_show_data_pressed', StateFilter(default_state))
async def process_button_reg_press(callback: CallbackQuery):
    if callback.from_user.id in user_dict:
        await callback.message.answer(
            text=f'Имя: {user_dict[callback.from_user.id]["username"]}\n'
                f'Пароль: {user_dict[callback.from_user.id]["password"]}'
        )

@dp.callback_query(F.data == 'button_sent_data_pressed', StateFilter(default_state))
async def process_button_reg_press(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    username = user_dict[callback.from_user.id]["username"]
    password = user_dict[callback.from_user.id]["password"]
    async with aiohttp.ClientSession() as session:
        data = {"username": username, "password": password, "telegram_id": telegram_id}
        response = await session.post('http://127.0.0.1:8000/user/add_tlg', json=data)
        if response.status == 200:
            await callback.message.answer(text=f'Вы успешно зарегистрировались в системе\n Ваш login: {username}\nPassword: {password}', parse_mode='html', reply_markup=keyboard)
        else:
            await callback.message.answer(text=f"Что-то пошло не так.")
    
if __name__ == '__main__':
    dp.run_polling(bot)