# BOT_TOKEN=7908854058:AAHcVeeVzEqriXeUxH80oi-BO4s1QZaNOeg
# # https://thecatapi.com/ (Optional)
# CAT_API_KEY=live_JxjUsjPKYcS1UCAU4fHZK6Fa09r2DwaV8W6XcUowqzZ5Z1f7aTZTy17JzQ93xEQ9
# # https://openweathermap.org/home/sign_up
# WEATHER_API_KEY=339667a9305fe469a7036a9afd4725d8

from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import requests

API_TOKEN = '7908854058:AAHcVeeVzEqriXeUxH80oi-BO4s1QZaNOeg'
WEATHER_API_KEY = '339667a9305fe469a7036a9afd4725d8'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Create buttons
button_hello = KeyboardButton('/hello')
button_cat = KeyboardButton('/cat')
button_weather = KeyboardButton('/weather')

# Create main menu keyboard
keyboard_markup = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_markup.add(button_hello, button_cat, button_weather)

# Create location request button for weather
location_button = KeyboardButton('Share location', request_location=True)
location_keyboard = ReplyKeyboardMarkup(
    one_time_keyboard=True, resize_keyboard=True
).add(location_button)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply(
        "Hello! I'm your friendly bot. I can do the following:\n\n"
        "/hello - Greet you with your nickname.\n"
        "/cat - Send you a random cat picture.\n"
        "/weather - Show your local weather.\n\n"
        "Choose an option below:",
        reply_markup=keyboard_markup
    )

@dp.message_handler(commands=['hello'])
async def hello(message: types.Message):
    user_name = message.from_user.username or message.from_user.first_name
    await message.reply(f"Hello {user_name}!")

@dp.message_handler(commands=['cat'])
async def send_cat_picture(message: types.Message):
    url = 'https://api.thecatapi.com/v1/images/search'
    response = requests.get(url)
    data = response.json()
    cat_image_url = data[0]['url']
    await bot.send_photo(chat_id=message.chat.id, photo=cat_image_url)

@dp.message_handler(commands=['weather'])
async def weather(message: types.Message):
    await message.reply(
        "Please share your location to get the local weather:",
        reply_markup=location_keyboard
    )

@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    weather_url = (
        f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}'
        f'&appid={WEATHER_API_KEY}&units=metric'
    )
    response = requests.get(weather_url)
    data = response.json()

    if data.get('main'):
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        city = data['name']
        await message.reply(
            f"The weather in {city} is {temp}°C with {description}."
        )
    else:
        await message.reply(
            "Sorry, I couldn't retrieve the weather for your location."
        )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
