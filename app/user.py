from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


from config.bot_config import API_TOKEN, ADMIN_ID
from app.database.requests import set_user, update_user, set_reserve
from app.database.models import get_data
import app.keyboards as kb


router = Router()

bot = Bot(token=API_TOKEN)
chat_id = ADMIN_ID

class Reg(StatesGroup):
    name = State()
    contact = State()


class Reserve(StatesGroup):
    barber = State()
    service = State()
    day = State()
    hour = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user = await set_user(message.from_user.id)
    if user:
        await message.answer(f'Доброго времени суток, {user.name}!', reply_markup=kb.main)
        await state.clear()
    else:
        await message.answer('Добро пожаловать! Пожалуйста пройдите регистрацию.\n\nВведите Ваше имя.')
        await state.set_state(Reg.name)

#начало процедуры регистрации
@router.message(Reg.name)
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.contact)
    await message.answer('Отправьте свои контактные данные в формате контакта', reply_markup=kb.contact)


@router.message(Reg.contact, F.contact)
async def reg_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    await update_user(message.from_user.id, data['name'], message.contact.phone_number)
    await state.clear()
    await message.answer(f'Воспользуйтесь меню для продолжения.', reply_markup=kb.main)
#окончание процедуры регистрации


#выбор мастера
@router.message(F.text == 'Приступим к записи')
async def get_service(message: Message, state: FSMContext):
    await state.set_state(Reserve.barber)
    await message.answer('Выберите мастера', reply_markup=await kb.barbers())

#запись мастера и переход к выбору услуги
@router.callback_query(F.data.startswith('barber_'), Reserve.barber)
async def get_service_2(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Мастер выбран.')
    await state.update_data(barber=callback.data.split('_')[1]) #обновилосось состояние выбора мастера
    await state.set_state(Reserve.service)
    await callback.message.answer('Выберите услугу', reply_markup=await kb.services()) #предлагается выборать услугу


@router.callback_query(F.data.startswith('service_'), Reserve.service) #получение ответа на выбор услуги
async def get_service_3(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Услуга выбрана.')
    await state.update_data(service=callback.data.split('_')[1]) #обновилось состояние выбора сервиса
    await state.set_state(Reserve.day)
    await callback.message.answer('Выберите день недели', reply_markup=await kb.days()) #предлагается выбрать день недели


@router.callback_query(F.data.startswith('day_'), Reserve.day)
async def get_service_4(callback: CallbackQuery, state: FSMContext):
    await callback.answer('День недели выбран.')
    await state.update_data(day=callback.data.split('_')[1])
    await state.set_state(Reserve.hour)
    await callback.message.answer('Выберите время', reply_markup=await kb.hours())


@router.callback_query(F.data.startswith('hour_'), Reserve.hour)
async def get_service_5(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Время выбрано.')
    await state.update_data(hour=callback.data.split('_')[1])
    data = await state.get_data()
    await set_reserve(callback.from_user.id, data['barber'], data['day'], data['hour'], callback.data.split('_')[1])
    await callback.message.answer('Услуги выбраны. Пожалуйста, нажмите кнопку "Завершить запись" для передачи информации менеджеру и завершения записи.', reply_markup=kb.main)


@router.message(F.text == 'Завершить запись')
async def cmd_stop(message: Message, bot: Bot, state: FSMContext):
    try:
        data_to_send = await get_data()
        formatted_data = '\n'.join([f'{item[0]} - {item[1]}, {item[2]}, {item[3]}, {item[4]}, {item[5]}' for item in data_to_send])
        await bot.send_message(chat_id, 'У вас новая запись: {}' .format(formatted_data))
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
    user = await set_user(message.from_user.id)
    await message.answer(f'До свидания, {user.name}! Благодарим за обращение в наш салон, менеджер свяжется с Вами в ближайшее время!', reply_markup=kb.main)
    await state.clear()




