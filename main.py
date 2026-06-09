from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import json

TOKEN = '8931007305:AAGewyuIKAX_pt2YxzpWj9WYP1lMD5i6XdM'
bot = Bot(token=TOKEN)
dp = Dispatcher()
URL = 'https://myshop-sooty-tau.vercel.app'

@dp.message(Command("start"))
async def start(message: types.Message):
    web_app = WebAppInfo(url=URL)
    btn = InlineKeyboardButton(text="🛒 Открыть магазин", web_app=web_app)
    kb = InlineKeyboardMarkup(inline_keyboard=[[btn]])
    await message.answer("Магазин открыт!", reply_markup=kb)

@dp.message()
async def handle_data(message: types.Message):
    # Эта часть ловит данные, когда ты нажимаешь кнопку в WebApp
    if message.web_app_data:
        data = json.loads(message.web_app_data.data)
        await message.answer(f"✅ ЗАКАЗ!\nТовар: {data['item']}\nИмя: {data['name']}\nТел: {data['phone']}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
