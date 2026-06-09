from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio
from aiohttp import web

# 1. Твой токен
TOKEN = '8931007305:AAGewyuIKAX_pt2YxzpWj9WYP1lMD5i6XdM'
bot = Bot(token=TOKEN)
dp = Dispatcher()

# 2. Ссылка на Vercel
URL = 'https://myshop-sooty-tau.vercel.app'

@dp.message(Command("start"))
async def start(message: types.Message):
    web_app = WebAppInfo(url=URL)
    btn = InlineKeyboardButton(text="🛒 Открыть магазин", web_app=web_app)
    kb = InlineKeyboardMarkup(inline_keyboard=[[btn]])
    await message.answer("Магазин запущен!", reply_markup=kb)

# 3. ЭТО ЗАСТАВИТ RENDER ПЕРЕСТАТЬ РУГАТЬСЯ НА ПОРТЫ
async def handle(request):
    return web.Response(text="Bot is running")

async def main():
    # Запускаем веб-сервер на порту, который требует Render
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 10000) # Render требует этот порт
    await site.start()
    
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
