from aiogram.utils.keyboard import InlineKeyboardBuilder

# Оставление заявки
def business_type_task_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Продажа', callback_data='selling')
    keyboard_builder.button(text='Производство', callback_data='production')
    keyboard_builder.button(text='Оказание услуг', callback_data='service')
    keyboard_builder.adjust(1, 1, 1)
    return keyboard_builder.as_markup()

def platform_type_task_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Телеграм', callback_data='telegram')
    keyboard_builder.button(text='Ватсап', callback_data='wats_up')
    keyboard_builder.button(text='Вайбер', callback_data='viber')
    keyboard_builder.adjust(1, 1, 1)
    return keyboard_builder.as_markup()

# Купить товар

def buy_product_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Купить 1 раз', callback_data='buy_one_time')
    keyboard_builder.button(text='Купить 2 раза', callback_data='buy_two_time')
    keyboard_builder.adjust(1, 1, 1)
    return keyboard_builder.as_markup()


def main_menu_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Оставить заявку ✉️', callback_data='send_application')
    keyboard_builder.button(text='Купить товар 💸', callback_data='buy_position')
    keyboard_builder.button(text='Мой баланс 💰', callback_data='my_balance')
    keyboard_builder.adjust(1, 1, 1)
    return keyboard_builder.as_markup()


def main_menu_for_admin_keyboard():
    keyboard_builder = InlineKeyboardBuilder()
    keyboard_builder.button(text='Оставить заявку ✉️', callback_data='send_application')
    keyboard_builder.button(text='Купить товар 💸', callback_data='buy_position')
    keyboard_builder.button(text='Мой баланс 💰', callback_data='my_balance')
    keyboard_builder.button(text='Отправить сообщение пользователям 🔔', callback_data='send_all')
    keyboard_builder.adjust(1, 1, 1, 1)
    return keyboard_builder.as_markup()
