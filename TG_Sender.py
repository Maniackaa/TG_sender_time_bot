import asyncio

import logging

from sqlalchemy.orm import Session

from config_data.config import load_config
from aiogram import Bot, Dispatcher

from database.db import engine, BotSettings
from handlers import user_handlers, echo
from services.TG_read_smser_func import get_smser_dict
from services.task_func import get_task_to_send, make_task_and_get_message, \
    format_smser_message

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
           u'[%(asctime)s] - %(name)s - %(message)s')


def read_sender_settings():
    bot_settings = {}
    session = Session(bind=engine)
    with session:
        all_settings: list[BotSettings] = session.query(BotSettings).all()
        for setting in all_settings:
            bot_settings[setting.name] = setting.value
        session.commit()
    return bot_settings


async def timer(bot: Bot):
    refresh_delay = 10
    while True:
        try:
            bot_settings = read_sender_settings()
            alarms_list = []
            if bot_settings.get('is_work') != '0':
                refresh_delay = 1
                session = Session(bind=engine)
                bot_settings = read_sender_settings()

                if bot_settings.get('send_test') == '1':
                    test_msg = format_smser_message(get_smser_dict())
                    await bot.send_message(bot_settings.get('alarm_id'), test_msg)

                with session:
                    # Список задач на выполнение если они есть:
                    tasks_to_send = get_task_to_send(session)
                    for task_to_send in tasks_to_send:
                        # Проверка на изменение данных:
                        # check_alarm()

                        # Выполнение задачи и формирование сообщения для отправки
                        message, alarms_list = make_task_and_get_message(task_to_send,
                                                            session,
                                                            bot_settings)
                        for alarm in alarms_list:
                            await bot.send_message(bot_settings.get('alarm_id'), alarm)

                        # Отправка сообщения в основную группу
                        if message:
                            await bot.send_message(
                                bot_settings.get('group_id'), message)
                    session.commit()
        except Exception as err:
            logger.error(err)
            await bot.send_message(bot_settings.get('alarm_id'), str(err))
            refresh_delay = 10
        await asyncio.sleep(refresh_delay)


async def main():
    logger.info('Starting bot')
    config = load_config('myenv.env')
    bot: Bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()

    asyncio.create_task(timer(bot))
    dp.include_router(user_handlers.router)
    dp.include_router(echo.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
