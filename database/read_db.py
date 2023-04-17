
import logging

from sqlalchemy import func
from sqlalchemy.orm import Session

from database.db import engine, Task, Message, BotSettings

logger = logging.getLogger(__name__)

def run_bot():
    session = Session(bind=engine)
    is_work: BotSettings = session.query(BotSettings).filter(
        BotSettings.name == 'is_work').first()
    is_work.value = 1
    session.commit()
    logger.warning('Бот включен')


def stop_bot():
    session = Session(bind=engine)
    is_work: BotSettings = session.query(BotSettings).filter(
        BotSettings.name == 'is_work').first()
    is_work.value = 0
    session.commit()
    logger.warning('Бот выключен')
