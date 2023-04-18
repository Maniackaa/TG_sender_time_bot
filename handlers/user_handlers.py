import logging

from aiogram import Router, Bot
from aiogram.exceptions import TelegramBadRequest

from aiogram.types import Message

from config_data.config import config


router = Router()
logger = logging.getLogger(__name__)


# Определение группы
@router.message()
async def send_echo(message: Message, bot: Bot):
    print(message)
    if message.new_chat_members:
        for member in message.new_chat_members:
            if member.id == bot.id:
                text = (f'Бот с ID {member.id} {member.full_name}'
                        f' добавлен в чат {message.chat.id} {message.chat.title}')
                admins = config.tg_bot.admin_ids
                for admin in admins:
                    try:
                        await bot.send_message(admin, text)
                    except TelegramBadRequest as err:
                        logger.info(f'Не могу отправить сообщение для ID {admin}')
                        logger.warning(err)
