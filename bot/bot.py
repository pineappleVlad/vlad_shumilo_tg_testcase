import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from handlers.basic import start, payment_success, mail_sender
from handlers.callback import send_application, platform_type_choose_call, budget_choose_call, phone_register_call, phone_input_call, buy_position, ukassa_pay, ukassa_result, check_balance, send_all_bot_users
from aiogram.filters import Command
from utils.states import States

load_dotenv()
TOKEN = os.getenv('TOKEN')



async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.message.register(start, Command('start'))


    # заявка
    dp.callback_query.register(send_application, F.data.startswith('send_application'))
    dp.callback_query.register(platform_type_choose_call, States.send_application)
    dp.callback_query.register(budget_choose_call, States.platform_type_choose)
    dp.message.register(phone_input_call, States.budget_choose)
    dp.message.register(phone_register_call, States.phone_input)

    # покупка
    dp.callback_query.register(buy_position, F.data.startswith('buy_position'))
    dp.callback_query.register(ukassa_pay, States.quantity_choose)
    dp.pre_checkout_query.register(ukassa_result, States.ukassa)
    dp.message.register(payment_success, F.successful_payment)

    # баланс
    dp.callback_query.register(check_balance, F.data.startswith('my_balance'))

    # рассылка
    dp.callback_query.register(send_all_bot_users, F.data.startswith('send_all'))
    dp.message.register(mail_sender, States.send_all_users)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(main())