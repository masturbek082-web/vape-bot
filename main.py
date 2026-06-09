from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio

# Твой токен
TOKEN = '8931007305:AAGewyuIKAX_pt2YxzpWj9WYP1lMD5i6XdM'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Ссылка на твой магазин
WEB_APP_URL = 'https://myshop-sooty-tau.vercel.app'

@dp.message(Command("start"))
async def start(message: types.Message):
    # Кнопка для открытия Web App
    web_app = WebAppInfo(url=WEB_APP_URL)
    button = InlineKeyboardButton(text="🛒 Открыть магазин", web_app=web_app)
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    
    await message.answer("Добро пожаловать в магазин! Нажми кнопку ниже:", reply_markup=markup)

# Обработка данных из магазина (всё, что придет из Web App)
@dp.message()
async def handle_data(message: types.Message):
    if message.web_app_data:
        await message.answer(f"✅ Новый заказ получен!\n\nДетали: {message.web_app_data.data}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
