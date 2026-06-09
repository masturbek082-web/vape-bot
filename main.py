from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import json

TOKEN = '8931007305:AAGewyuIKAX_pt2YxzpWj9WYP1lMD5i6XdM'
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    web_app = WebAppInfo(url='https://myshop-sooty-tau.vercel.app')
    btn = InlineKeyboardButton(text="🛒 Открыть", web_app=web_app)
    kb = InlineKeyboardMarkup(inline_keyboard=[[btn]])
    await message.answer("Жми кнопку:", reply_markup=kb)

@dp.message()
async def echo(message: types.Message):
    if message.web_app_data:
        data = json.loads(message.web_app_data.data)
        await message.answer(f"Заказ принят!\nИмя: {data['name']}\nТелефон: {data['phone']}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
