from aiogram.fsm.state import State, StatesGroup

class States(StatesGroup):
    start = State()

    #Основное меню
    send_application = State()
    my_balance = State()
    send_all_users = State()

    #Оставить заявку
    platform_type_choose = State()
    budget_choose = State()
    phone_input = State()

    #Купить товар
    quantity_choose = State()
    ukassa = State()

