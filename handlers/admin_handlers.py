from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter, Text, BaseFilter
from aiogram.types import CallbackQuery, Message, BotCommand

from config_data.config import config
from database.read_db import run_bot, stop_bot
from lexicon.lexicon import LEXICON_COMMANDS_RU


class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        self.admin_ids = config.tg_bot.admin_ids

    async def __call__(self, message: Message) -> bool:
        print(f'Проверка на админа\n'
              f'{message.from_user.id in self.admin_ids}')
        return message.from_user.id in self.admin_ids


router = Router()
router.message.filter(IsAdmin())




async def set_main_menu(bot: Bot):
    main_menu_commands = []
    await bot.set_my_commands(main_menu_commands)


# async def set_main_menu(bot: Bot):
#     main_menu_commands = [
#         BotCommand(command=command, description=description)
#         for command, description in LEXICON_COMMANDS_RU.items()]
#     await bot.set_my_commands(main_menu_commands)


@router.message(Command(commands=["start"]))
async def process_start_command(message: Message, bot):
    await set_main_menu(bot)
    title_group = message.chat.title
    group_id = message.chat.id
    print(group_id)
    await message.answer(f'Привет. {title_group} {group_id}',
                         parse_mode='html',
                         )


@router.message(Command(commands=["run_bot"]))
async def process_start_command(message: Message):
    run_bot()
    await message.answer('Бот запущен',
                         parse_mode='html',
                         )


@router.message(Command(commands=["stop_bot"]))
async def process_start_command(message: Message):
    stop_bot()
    await message.answer('Бот остановлен',
                         parse_mode='html',
                         )

# # Последний эхо-фильтр
# @router.message()
# async def send_echo(message: Message):
#     print(message)
#     await message.reply(text=message.text)


