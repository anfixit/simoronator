from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from utils.magic_encoder import encode_magic_code

router = Router()


class MagicCodeStates(StatesGroup):
    waiting_for_intent = State()
    waiting_for_fio_birthdate = State()


@router.message(F.text.lower() == "/magic_code")
async def start_magic_code(message: Message, state: FSMContext):
    await message.answer("\U0001F52E Напиши своё намерение. Пример: \n\nДля изобилия и радости в жизни")
    await state.set_state(MagicCodeStates.waiting_for_intent)


@router.message(MagicCodeStates.waiting_for_intent)
async def get_intent(message: Message, state: FSMContext):
    await state.update_data(intent=message.text.strip())
    await message.answer("Теперь напиши ФИО и дату рождения через пробел.\n\nПример: Иванова Светлана Николаевна 02.07.1985")
    await state.set_state(MagicCodeStates.waiting_for_fio_birthdate)


@router.message(MagicCodeStates.waiting_for_fio_birthdate)
async def get_fio_and_generate(message: Message, state: FSMContext):
    data = await state.get_data()
    intent = data.get("intent")
    user_input = message.text.strip()

    if len(user_input.split()) < 4:
        await message.answer("Формат некорректный. Укажи ФИО и дату рождения через пробел, например: Иванова Светлана Николаевна 02.07.1985")
        return

    full_text = f"{intent} {user_input}"
    code = encode_magic_code(full_text)

    await message.answer(
        f"\u2728 Твой ЛИЧНЫЙ ВОЛШЕБНЫЙ КОД СИМОРОН:\n\n`{code}`\n\nНанеси его на бумагу, прошепчи в зеркало или просто сохрани в сердце — магия началась.",
        parse_mode="Markdown"
    )
    await state.clear()
