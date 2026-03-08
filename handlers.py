from aiogram import types, Router, F
from aiogram.filters.command import Command
import requests
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder
import random


router = Router()
with open('cat_api.txt', 'r') as file:
    api = file.read().strip()
    print(api)
    

slovar = ['тута','здеся','прямо тутка', 'Чуть чуть левее тута', 'чуть чуть правее тута', 'около здеся','вот прям тут', 'здесь', 'тут', 'в данном месте']


@router.message(F.location)
async def get_loc(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    randomize = int(random.uniform(0, 10))
    await message.answer(f'температура {slovar[randomize]} на данный момент составляет:\n{get_temp(lat,lon)}°C\n{get_weather(lat,lon)}')


@router.callback_query(F.data == 'about_project')
async def about_project(callback: types.CallbackQuery):
    await callback.message.answer('Данный проект предназначен для определения температуры в разных точках мира!\nЧТобы воспользоваться ботом, просто отправьте в личные сообщения геолокацию желанной точки')

@router.message(Command('start'))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text='О проекте', callback_data='about_project'))
    await message.answer('Бот запущен!\nЕсли хотите больше узнать о боте, то нажмите кнопку ниже', reply_markup=builder.as_markup())

def get_temp(lat,lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,rain,snowfall"
    print(url)
    responce = requests.get(url).json()
    temp = responce['current']['temperature_2m']
    return str(temp)
def get_weather(lat,lon):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,rain,snowfall"
    responce = requests.get(url).json()
    issnowfall = responce['current']['snowfall']
    israin = responce['current']['rain']
    final = ''
    if issnowfall > 0:
        final += '🌨️'
    if israin > 0:
        final += '🌧️'
    if final:
        return f'Погода: {final}'
    else:
        return ''




    