from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter, Text, BaseFilter
from aiogram.types import CallbackQuery, Message

from config_data.config import config


class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        self.admin_ids = config.tg_bot.admin_ids

    async def __call__(self, message: Message) -> bool:
        print(f'Проверка на админа\n'
              f'{message.from_user.id in self.admin_ids}')
        return message.from_user.id in self.admin_ids


router = Router()
router.message.filter(IsAdmin())


@router.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    text = 'start'
    await message.answer(text,
                         parse_mode='html',
                         )


# Последний эхо-фильтр
@router.message()
async def send_echo(message: Message):
    print(message)
    await message.reply(text=message.text)

