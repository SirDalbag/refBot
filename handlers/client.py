from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode
from temp import dp, bot
from keyboards import kb_client

import aiogram.utils.markdown as md


class RefForm(StatesGroup):
    name = State()
    group = State()
    phoneNum = State()
    ref = State()

async def command_start(message: types.Message):
    await message.answer('Для получения справки нажмите на кнопку или же напишите команду /ref\n\nВнимание! Ошибки допущенные при заполнении данных будут у Вас в справке!\n\nДля отмены нажмите на кнопку или же напишите команду /cancel\n\nСправка будет готова в течении 3-х рабочих дней. Забрать её можно будет в n кабинете', reply_markup=kb_client)


async def command_ref(message: types.Message):
    await RefForm.name.set()
    await message.reply("Ваше ФИО?")


async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('OK')


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await RefForm.next()
    await message.reply('Ваша группа?')


async def load_group(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['group'] = message.text
    await RefForm.next()
    await message.reply('Ваш номер телефона?')


async def load_phoneNum(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phoneNum'] = message.text
    await RefForm.next()
    await message.reply('Какая справка Вам нужна?')


async def load_ref(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ref'] = message.text
    await bot.send_message(
        message.chat.id,
        md.text(
            md.text('Имя студента:', data['name']),
            md.text('Группа:', data['group']),
            md.text('Номер телефона:', data['phoneNum']),
            md.text('Справка:', data['ref']),
            sep='\n',
        ),
        parse_mode=ParseMode.MARKDOWN,
    )
    await bot.answer('Справка будет готова в течении 3-х рабочих дней. Забрать её можно будет в n кабинете')
    chat_id = message.chat.id
    admin_id = 920986648
    button_url = f'tg://openmessage?user_id={chat_id}'
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(text='Профиль', url=button_url))
    await bot.send_message(admin_id, text=md.text(
            md.text('Имя студента:', data['name']),
            md.text('Группа:', data['group']),
            md.text('Номер телефона:', data['phoneNum']),
            md.text('Справка:', data['ref']),
            sep='\n',
        ), reply_markup=markup)
    await state.finish()


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=[
                                'start', 'help'], state=None)
    dp.register_message_handler(command_ref, commands=['ref'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=['cancel'])
    dp.register_message_handler(cancel_handler, Text(
        equals='cancel', ignore_case=True), state="*")
    dp.register_message_handler(load_name, state=RefForm.name)
    dp.register_message_handler(load_group, state=RefForm.group)
    dp.register_message_handler(load_phoneNum, state=RefForm.phoneNum)
    dp.register_message_handler(load_ref, state=RefForm.ref)
