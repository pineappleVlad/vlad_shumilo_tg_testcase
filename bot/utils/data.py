import asyncio

admin_ids = [1390542002, 716775112]

async def remind_to_fill_application(chat_id, bot):
    await bot.send_message(chat_id, "Ты забыл заполнить заявку!")

async def schedule_reminder(chat_id, bot):
    await asyncio.sleep(600)
    await remind_to_fill_application(chat_id, bot)

