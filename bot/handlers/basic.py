from aiogram import Bot
from keyboards.inline import main_menu_keyboard, main_menu_for_admin_keyboard
from database.db_query import create_tables, create_user, view_all_rows, delete_all_rows, drop_all
from database.db_models import get_session
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from utils.states import States
from utils.data import admin_ids

from database.db_query import balance_update_query, all_ids_info_query



async def start(message: Message, bot: Bot, state: FSMContext):
    async with await get_session() as session:
        try:
            await create_tables()
            await create_user(chat_id=message.from_user.id, tg_username=message.from_user.full_name, session=session)
        finally:
            await session.close()

    await state.set_state(States.start)
    if message.chat.id in admin_ids:
        await bot.send_message(text='Привет! Выбери действие в меню ниже', chat_id=message.chat.id,
                               reply_markup=main_menu_for_admin_keyboard())
    else:
        await bot.send_message(text='Привет! Выбери действие в меню ниже', chat_id=message.chat.id, reply_markup=main_menu_keyboard())



async def mail_sender(message: Message, bot: Bot, state: FSMContext):
    await state.set_state(States.start)
    async with await get_session() as session:
        all_ids = await all_ids_info_query(session)
    for id in all_ids:
        await bot.send_message(text=message.text, chat_id=id)

async def payment_success(message: Message, bot: Bot, state: FSMContext):
    if message.successful_payment.total_amount == 10000:
        new_balance = 1
    else:
        new_balance = 2
    await state.set_state(States.start)

    async with await get_session() as session:
        try:
            await balance_update_query(session=session, user_id=message.from_user.id, new_balance=new_balance)
        finally:
            await session.close()
    await bot.send_message(chat_id=message.from_user.id, text='Для отображения меню вызовите /start')
    await start(message, bot, state)