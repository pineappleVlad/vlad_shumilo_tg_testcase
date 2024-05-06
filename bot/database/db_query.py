from sqlalchemy import select

from .db_models import engine, User, Application, Base

#Создание таблиц в бд
async def create_tables():
    async with engine.begin() as conn:
        if not (await conn.run_sync(engine.dialect.has_table, "users")) or \
           not (await conn.run_sync(engine.dialect.has_table, "applications")):
            await conn.run_sync(Base.metadata.create_all)



#Сохранение юзера в бд
async def create_user(chat_id, tg_username, session):
    existing_user = await session.execute(select(User).filter(User.chat_id == chat_id))
    existing_user = existing_user.scalar_one_or_none()
    if existing_user:
        existing_user.tg_username = tg_username
        await session.commit()
        return existing_user
    else:
        new_user = User(tg_username=tg_username, chat_id=chat_id)
        session.add(new_user)
        await session.commit()
        return new_user

#Создание заявки в бд
async def create_application(user_id, session):
    existing_application = await session.execute(select(Application).filter(Application.user_id == user_id))
    existing_application = existing_application.scalar_one_or_none()
    if existing_application:
        return
    else:
        new_application = Application(user_id=user_id)
        session.add(new_application)
        await session.commit()

#Запись типа компании в базу
async def business_type_query(session, business_type, user_id):
    application = await session.execute(select(Application).filter(Application.user_id == user_id))
    application = application.scalar_one_or_none()
    application.business_type = business_type
    await session.commit()


#Запись типа платформы в базу
async def platform_type_query(session, platform_type, user_id):
    application = await session.execute(select(Application).filter(Application.user_id == user_id))
    application = application.scalar_one_or_none()
    application.platform_type = platform_type
    await session.commit()


#Сохранение бюджета в базу
async def budget_query(session, budget, user_id):
    application = await session.execute(select(Application).filter(Application.user_id == user_id))
    application = application.scalar_one_or_none()
    application.budget = budget
    await session.commit()


#Сохранение телефона в базу

async def phone_register_query(session, phone_number, user_id):
    application = await session.execute(select(Application).filter(Application.user_id == user_id))
    application = application.scalar_one_or_none()
    application.phone_number = phone_number
    await session.commit()

#Пополнение баланса
async def balance_update_query(session, new_balance, user_id):
    user = await session.execute(select(User).filter(User.chat_id == user_id))
    user = user.scalar_one_or_none()

    if user:
        user.balance += new_balance
        await session.commit()
    else:
        print("Юзер не найден")

#Отображение баланса юзера
async def balance_view_query(session, user_id):
    user = await session.execute(select(User).filter(User.chat_id == user_id))
    user = user.scalar_one_or_none()
    return user.balance


#Получение айдишников всех юзеров в боте
async def all_ids_info_query(session):
    users = await session.execute(select(User.chat_id))
    ids = [user.chat_id for user in users if user.chat_id != 7041005769]
    return ids


# Посмотреть все записи в таблице
async def view_all_rows(session):
    query = await session.execute(select(Application))
    users = query.scalars().all()
    return users


# Очистить таблицы
async def delete_all_rows(session):
    await session.execute(User.__table__.delete())
    await session.execute(Application.__table__.delete())
    await session.commit()


# Удалить таблицы

async def drop_all():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)



# Получение всей инфы по заявке

async def retrieve_application_info(session, user_id):
    application = await session.execute(select(Application).filter(Application.user_id == user_id))
    application = application.scalar_one_or_none()

    user = await session.execute(select(User).filter(User.chat_id == user_id))
    user = user.scalar_one_or_none()

    result_data = f"""
    Новая заявка \n
Имя пользователя в телеграмме - {user.tg_username}
Направление бизнеса - {application.business_type}
Платформа - {application.platform_type}
Бюджет - {application.budget}
Номер телефона - {application.phone_number}
    """
    return result_data


# Удаление заявки после отправки
async def delete_application(session, user_id):
    await session.execute(Application.__table__.delete().where(Application.user_id == user_id))
    await session.commit()
