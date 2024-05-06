from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, PreCheckoutQuery
from keyboards.inline import business_type_task_keyboard, platform_type_task_keyboard, buy_product_keyboard
from utils.states import States
from utils.data import remind_to_fill_application, schedule_reminder
from database.db_query import (create_application, view_all_rows, business_type_query, platform_type_query,
                               budget_query, phone_register_query, retrieve_application_info, balance_update_query, balance_view_query,
                               delete_application, all_ids_info_query)
from database.db_models import get_session, UKASSA_TEST_TOKEN
from handlers.basic import start
import asyncio


async def send_application(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(States.send_application)
    async with await get_session() as session:
        await create_application(user_id=call.from_user.id, session=session)
    await call.message.answer(text='Какое направление вашего бизнеса?', reply_markup=business_type_task_keyboard())
    reminder_task = asyncio.create_task(schedule_reminder(call.message.chat.id, bot))
    await state.update_data(reminder_task=reminder_task)


async def platform_type_choose_call(call: CallbackQuery, bot: Bot, state: FSMContext):
    if call.data == 'selling':
        business_type = 'Продажа'
    elif call.data == 'production':
        business_type = 'Производство'
    else:
        business_type = 'Оказание услуг'
    await state.set_state(States.platform_type_choose)
    async with await get_session() as session:
        await business_type_query(session=session, user_id=call.from_user.id, business_type=business_type)
    await call.message.answer(text='На какой платформе вы хотите разработать чат-бот?', reply_markup=platform_type_task_keyboard())
    await call.message.delete()

async def budget_choose_call(call: CallbackQuery, bot: Bot, state: FSMContext):
    if call.data == 'telegram':
        platform_type = 'Телеграм'
    elif call.data == 'wats_up':
        platform_type = 'Ватсап'
    else:
        platform_type = 'Вайбер'
    await state.set_state(States.budget_choose)
    async with await get_session() as session:
        await platform_type_query(session=session, user_id=call.from_user.id, platform_type=platform_type)
    await call.message.answer(text='Какой у вас бюджет? \n'
                                'Напишите в формате "От ... до ...')
    # await call.message.delete()


async def phone_input_call(call: CallbackQuery, bot: Bot, state: FSMContext):
    budget_str = call.text
    await state.set_state(States.phone_input)
    async with await get_session() as session:
        await budget_query(session=session, user_id=call.from_user.id, budget=budget_str)
    await bot.send_message(text='Введите ваш номер телефона', chat_id=call.chat.id)


async def phone_register_call(call: CallbackQuery, bot: Bot, state: FSMContext):
    phone = call.text
    await state.set_state(States.start)

    async with await get_session() as session:
        await phone_register_query(session=session, user_id=call.from_user.id, phone_number=phone)
    data = await state.get_data()
    reminder_task = data.get('reminder_task')
    if reminder_task:
        reminder_task.cancel()

    result_position = await retrieve_application_info(user_id=call.from_user.id, session=session)

    admin_chat_id = "716775112"
    await bot.send_message(chat_id=admin_chat_id, text=result_position)

    await bot.send_message(text='Заявка успешно отправлена', chat_id=call.chat.id)
    async with await get_session() as session:
        await delete_application(session=session, user_id=call.from_user.id)

    await start(call, bot, state)



async def buy_position(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(States.quantity_choose)
    await call.message.answer(text='Укажите размер покупки', reply_markup=buy_product_keyboard())
    await call.message.delete()

async def ukassa_pay(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(States.ukassa)
    basic_price = 100

    if call.data == 'buy_two_time':
        basic_price *= 2

    await bot.send_invoice(chat_id=call.from_user.id, title='Оплата покупки', description='Описание товара', payload='Товар', provider_token=UKASSA_TEST_TOKEN,
                     currency='RUB', start_parameter='bot_payment', prices=[{'label': "Руб", 'amount': basic_price * 100}])

    await call.message.delete()


async def ukassa_result(pre_checkout_query: PreCheckoutQuery, bot: Bot, state: FSMContext):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)



async def check_balance(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(States.my_balance)
    async with await get_session() as session:
        balance = await balance_view_query(session=session, user_id=call.from_user.id)
    await call.message.answer(text=f'У вас {balance} условных единиц')
    await start(call.message, bot, state)
    await call.message.delete()



async def send_all_bot_users(call: CallbackQuery, bot: Bot, state: FSMContext):
    await state.set_state(States.send_all_users)
    await call.message.answer(text='Введите сообщение для рассылки')
    await call.message.delete()






