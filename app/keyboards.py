from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.requests import get_manicurists, get_services, get_hours, get_days

contact = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Отправить контакт', request_contact=True)]
], resize_keyboard=True, input_field_placeholder='Нажмите кнопку ниже.')


main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Записаться на услугу')],
#    [KeyboardButton(text='Завершить')]
], resize_keyboard=True)

#считывание из базы всей информации
async def manicurists():
    all_manicurists = await get_manicurists()
    keyboard = InlineKeyboardBuilder()
    for manicurist in all_manicurists:
        keyboard.add(InlineKeyboardButton(text=manicurist.name, callback_data=f'manicurist_{manicurist.id}'))
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
        keyboard.add(InlineKeyboardButton(text=hour.name, callback_data=f'hour_{hour.id}'))
    return keyboard.adjust(1).as_markup()