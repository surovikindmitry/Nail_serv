from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.database.requests import get_barbers, get_services, get_days, get_hours

contact = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отправить контакт', request_contact=True)]
], resize_keyboard=True, input_field_placeholder='Нажмите кнопку ниже.')


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Приступим')],
    [KeyboardButton(text='Записаться')]
], resize_keyboard=True)


async def barbers():
    all_barbers = await get_barbers()
    keyboard = InlineKeyboardBuilder()
    for barber in all_barbers:
        keyboard.add(InlineKeyboardButton(text=barber.name, callback_data=f'barber_{barber.id}'))
    return keyboard.adjust(1).as_markup()


async def services():
    all_services = await get_services()
    keyboard = InlineKeyboardBuilder()
    for service in all_services:
        keyboard.add(InlineKeyboardButton(text=service.name, callback_data=f'service_{service.id}'))
    return keyboard.adjust(1).as_markup()

async def days():
    all_days = await get_days()
    keyboard = InlineKeyboardBuilder()
    for day in all_days:
        keyboard.add(InlineKeyboardButton(text=day.name, callback_data=f'day_{day.id}'))
    return keyboard.adjust(1).as_markup()

async def hours():
    all_hours = await get_hours()
    keyboard = InlineKeyboardBuilder()
    for hour in all_hours:
        keyboard.add(InlineKeyboardButton(text=hours.name, callback_data=f'hour_{hour.id}'))
    return keyboard.adjust(1).as_markup()