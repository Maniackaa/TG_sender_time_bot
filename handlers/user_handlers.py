from aiogram import Dispatcher, types, Router
from aiogram.filters import Command, CommandStart, Text
from aiogram.types import CallbackQuery, Message, URLInputFile


from aiogram.fsm.context import FSMContext

from lexicon.lexicon import LEXICON
from services.TG_read_smser_func import get_smser_dict
from services.task_func import format_smser_message

router: Router = Router()



@router.message(Command(commands=["start"]))
async def process_start_command(message: CallbackQuery | Message, state: FSMContext):
    await state.clear()
    text = LEXICON['/start']
    msg_dict = get_smser_dict()
    text = format_smser_message(msg_dict)
    await message.answer(text,
                         parse_mode='html',
                         )





