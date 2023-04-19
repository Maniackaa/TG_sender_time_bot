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
    target_date: Mapped[str] = mapped_column(nullable=True, default=None)
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

