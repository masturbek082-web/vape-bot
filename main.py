from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio
from aiohttp import web
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
    await message.answer("Добро пожаловать! Нажми кнопку:", reply_markup=kb)

@dp.message()
async def handle_data(message: types.Message):
    if message.web_app_data:
        data = json.loads(message.web_app_data.data)
        text = f"✅ НОВЫЙ ЗАКАЗ!\n\nТовар: {data['item']}\nВкус: {data['flavor']}\nИмя: {data['name']}\nТелефон: {data['phone']}"
        await message.answer(text)

async def handle(request):
    return web.Response(text="Bot is running")

async def main():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
