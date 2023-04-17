import datetime
import json
import logging

from sqlalchemy import func
from sqlalchemy.orm import Session

from database.db import engine, Task, Message, BotSettings
from services.TG_read_smser_func import get_smser_dict
from services.check_smser_func import test_refresh, test_high_volatility

logger = logging.getLogger(__name__)


def get_task_to_send(session) -> list[Task]:
    """Достанем задачи, дата последней отправки раньше чем сегодня"""
    tasks_to_send = []
    # session = Session(bind=engine)
    now_date = datetime.datetime.now().date()
    # Если сегодня суббота или вс, то не работаем
    if now_date.weekday() in (5, 6):
        logger.debug('Выходной')
        return tasks_to_send
    all_tasks = session.query(Task).filter(
        func.DATE(Task.last_send) < now_date, Task.is_active == 1).all()
    logger.debug(f'Все не отправленные задачи: {all_tasks}')
    # session.commit()

    if all_tasks:
        # Проверим не пора ли отправлять их.
        now_time = datetime.datetime.now().time()
        for task in all_tasks:
            task_time = datetime.datetime.strptime(
                            task.target_time, '%H:%M:%S'
                        ).time()
            logger.debug(f'Сверка задачи {task}: {now_time} '
                         f'{now_time > task_time} {task_time}'
                         f' last_send: {task.last_send}')
            if now_time > task_time:
                tasks_to_send.append(task)
    return tasks_to_send


def format_smser_message(msg_dict: dict) -> str:
    """Преобразование сообщением для отправки"""
    logger.debug(f'Формирование сообщения для отправки из {msg_dict}')
    format_message = '<code>'
    for key, val in msg_dict.items():
        logger.debug(f'{key} - {val}')
        format_message += (
            f'{(key+":"):10}'
            f'{" ".join([str(v) if v is not None else "-" for v in val])}\n'
        )
    format_message += '</code>'
    logger.debug(format_message)
    return format_message


def save_msg_to_db(message: str, task_id: int, session: Session):
    logger.debug(f'Сохраняем сообщение {message}')
    msg = Message()
    msg.task_id = task_id
    msg.message = json.dumps(message)
    session.add(msg)


def make_task_and_get_message(task_to_send: Task,
                              session: Session,
                              bot_settings: dict) -> tuple[str, list]:
    """Выполнение задачи. Изменение last_send"""
    try:
        alarm_list = []
        if task_to_send.type == 'smser':
            logger.debug('ВЫполняется задача типа smser')
            # Прочитаем файл
            message_dict = get_smser_dict()

            # Формируем сообщение из файла
            message = format_smser_message(message_dict)
            # Проверим алармы
            if bot_settings.get('test_refresh') == '1':
                logger.debug('Проверка test_refresh')
                old_sms = session.query(Message).all()
                if old_sms:
                    if not test_refresh(
                            json.loads(old_sms[-1].message), message_dict):
                        alarm_list.append('Внимание. Данные не актуальны')
                        logger.warning('Внимание. Данные не актуальны')

            if bot_settings.get('test_high_volatility') == '1':
                logger.debug('Проверка test_high_volatility')
                old_sms = session.query(Message).all()
                if old_sms:
                    high_volatility_message = test_high_volatility(
                        json.loads(old_sms[-1].message),
                        message_dict,
                        target=bot_settings.get('volatility_target'),
                        )
                    if high_volatility_message:
                        alarm_list.append(high_volatility_message)
                        logger.info('Внимание. Высокая волатильность')

            # Сохраним файл-смс в архив
            save_msg_to_db(message_dict, task_to_send.id, session)

        if task_to_send.type == 'msg':
            message = task_to_send.message

        if task_to_send.type == 'last_msg':
            day_week = datetime.datetime.now().weekday()
            message = 'Хорошего вечера'\
                      if day_week != 4 \
                      else 'Хороших выходных'

        # Изменение времени отправки
        task_to_send.last_send = datetime.datetime.now()
        # Зафиксируем отправленное сообщение
        logger.info(f'Подготовили сообщение {message}')
        return message, alarm_list

    except Exception as err:
        logger.error('Ошибка в функции make_task_and_get_message')
        raise err

