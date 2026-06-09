from aiogram import Bot, Dispatcher, types
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio

# Твой токен
TOKEN = '8931007305:AAGewyuIKAX_pt2YxzpWj9WYP1lMD5i6XdM'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Та самая ссылка
URL = 'https://myshop-sooty-tau.vercel.app'

@dp.message(Command("start"))
async def start(message: types.Message):
    # Кнопка с веб-аппом
    web_app = WebAppInfo(url=URL)
    btn = InlineKeyboardButton(text="🛒 Открыть магазин", web_app=web_app)
    kb = InlineKeyboardMarkup(inline_keyboard=[[btn]])
    
    await message.answer("Добро пожаловать в Vape Shop!", reply_markup=kb)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
