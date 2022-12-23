from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from temp import bot

class AdminForm(StatesGroup):
    id = State()
    ref = State()

async def command_admin(message: types.Message):
    await AdminForm.id.set()
    await message.reply("ID запроса?")

async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')

async def load_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['id'] = message.text
    await AdminForm.next()
    await message.reply('Какая справка?')

async def load_ref(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ref'] = message.text
    chat_id = data['id']
    await bot.send_message(chat_id, f'Ваша справка \"{data["ref"]}\" готова!\n\nЗаберите её в n кабинете в течении 3-х дней.')
    await state.finish()

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_admin, commands=['final'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_handler, Text(
        equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(load_id, state=AdminForm.id)
    dp.register_message_handler(load_ref, state=AdminForm.ref)