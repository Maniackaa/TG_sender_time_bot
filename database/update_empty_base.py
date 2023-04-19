import datetime

from sqlalchemy.orm import Session
from database.db import engine, Task, BotSettings

session = Session(bind=engine)

with session:
    tasks = session.query(Task).all()
    print('------------------', tasks)
    if not tasks:
        test_task1: Task = Task(
            title='Приветствие',
            target_time=str(datetime.time(hour=10, minute=0, second=15)),
            last_send=datetime.datetime(2023, 4, 16),
            type='msg',
            message='Доброе утро',
            is_active=1
        )
        test_task2: Task = Task(
            title='Котировки №1',
            target_time=str(datetime.time(hour=10, minute=1, second=0)),
            last_send=datetime.datetime(2023, 4, 16),
            type='smser',
            is_active=1
        )
        session.add_all([test_task1, test_task2])
        for x in range(2, 10):
            task = Task(
                title=f'Котировки №{x}',
                target_time=str(datetime.time(hour=10 + x, minute=0, second=0)),
                last_send=datetime.datetime(2023, 4, 16),
                type='smser',
                is_active=1
            )
            session.add(task)
        test_task3 = Task(
            title=f'Завершающая отправка',
            target_time=str(datetime.time(hour=18, minute=40, second=0)),
            last_send=datetime.datetime(2023, 4, 16),
            type='smser',
            is_active=1
        )
        session.add(test_task3)
        test_task4: Task = Task(
            title='Образец последний',
            target_time=str(datetime.time(hour=18, minute=40, second=30)),
            last_send=datetime.datetime(2023, 4, 16),
            type='last_msg',
            is_active=1
        )
        session.add_all([test_task4])
        test_task5: Task = Task(
            title='Плановая',
            target_time=str(datetime.time(hour=18, minute=40, second=30)),
            target_date='2023-04-18',
            last_send=None,
            type='plane_msg',
            is_active=1,
            message='С Новым Годом!\nС Новым счастьем!'
        )
        session.add(test_task5)
    session.commit()

with session:
    settings = session.query(BotSettings).all()
    if not settings:
        settings1 = BotSettings(
            name='is_work',
            value='0',
            description='1 - бот работает, 0 - бот не работает',
        )
        settings2 = BotSettings(
            name='group_id',
            value='5627135088',
            description='ID группы для отправки сообщений',
        )
        settings3 = BotSettings(
            name='alarm_id',
            value='5627135088',
            description='ID для отправки алармов',
        )
        settings4 = BotSettings(
            name='test_refresh',
            value='1',
            description='Проверка на обновление файла smser. 1-вкл, 0-откл',
        )
        settings5 = BotSettings(
            name='test_high_volatility',
            value='1',
            description='Проверка на волатильность. 1-вкл, 0-откл',
        )
        settings6 = BotSettings(
            name='volatility_target',
            value='5.0',
            description='Порог волатильности в % в формате 2.5',
        )
        settings7 = BotSettings(
            name='send_message_to_group',
            value='1',
            description='1 - отправка в группу включена, 0 - бот работает, но сообщения в группу не отправляются',
        )
        settings8 = BotSettings(
            name='send_test',
            value='0',
            description='1 - Каждые 10 секунд отправляет прочитанное сообщение smser в аларм-канал',
        )
        session.add_all([settings1, settings2, settings3, settings4, settings5, settings6, settings7, settings8])
    session.commit()