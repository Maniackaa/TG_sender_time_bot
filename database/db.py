import datetime
from sqlalchemy import create_engine, ForeignKey, Date
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


from config_data.config import config

engine = create_engine(f"sqlite:///{config.db.db_path}", echo=False)
connection = engine.connect()


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = 'task'
    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True,
                                    comment='Первичный ключ')
    title: Mapped[str] = mapped_column(nullable=True)
    target_time: Mapped[str] = mapped_column()
    last_send: Mapped[str] = mapped_column(default='1999-01-01')
    type: Mapped[str] = mapped_column(default='smser')
    message: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[int] = mapped_column(default='1')
    send_messages: Mapped[list['Message']] = relationship(back_populates='task')

    def __repr__(self):
        return f'{self.id}. {self.target_time}'


class BotSettings(Base):
    __tablename__ = 'bot_settings'
    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True,
                                    comment='Первичный ключ')
    name: Mapped[str] = mapped_column()
    value: Mapped[str] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)


class Message(Base):
    __tablename__ = 'messages'
    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True,
                                    comment='Первичный ключ')
    task_id: Mapped[int] = mapped_column(ForeignKey('task.id'))
    message: Mapped[str] = mapped_column()
    task: Mapped['Task'] = relationship(back_populates='send_messages')
    send_time: Mapped[str] = mapped_column(default=str(datetime.datetime.now()))


Base.metadata.create_all(engine)

from sqlalchemy.orm import Session
from database.db import engine
session = Session(bind=engine)

with session:
    tasks = session.query(Task).all()
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