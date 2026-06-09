from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import json
import os

TOKEN = '8931007305:AAGewyuIKAX_pt2YxzpWj9WYP1lMD5i6XdM'
bot = Bot(token=TOKEN)
dp = Dispatcher()
URL = 'https://myshop-sooty-tau.vercel.app'
COUNTER_FILE = "order_count.txt"

# Твой контакт или контакт менеджера
MANAGER_CONTACT = "@manager_username" 

def get_next_order_id():
    if not os.path.exists(COUNTER_FILE):
        count = 0
    else:
        with open(COUNTER_FILE, "r") as f:
            count = int(f.read().strip())
    count += 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(count))
    return count

@dp.message(Command("start"))
async def start(message: types.Message):
    web_app = WebAppInfo(url=URL)
    btn = InlineKeyboardButton(text="🛒 Открыть магазин", web_app=web_app)
    kb = InlineKeyboardMarkup(inline_keyboard=[[btn]])
    await message.answer("Добро пожаловать! Выбери товары:", reply_markup=kb)

@dp.message()
async def handle_data(message: types.Message):
    if message.web_app_data:
        data = json.loads(message.web_app_data.data)
        order_id = get_next_order_id()
        
        # Словарь цен для расчета (названия должны совпадать с index.html)
        prices = {"Husky": 3500, "Lost Mary": 5500}
        
        total_price = 0
        order_details = ""
        for i in data['order']:
            price = prices.get(i['item'], 0)
            total_price += price
            order_details += f"\n• {i['item']} ({i['flavor']}) — {price} ₸"
        
        # Формируем красивое сообщение для клиента
        text = (
            f"✅ ЗАКАЗ №{order_id} ПРИНЯТ!\n\n"
            f"👤 Имя: {data['name']}\n"
            f"📱 Тел: {data['phone']}\n"
            f"🏠 Адрес: {data['addr']}\n\n"
            f"🛒 Ваш заказ:{order_details}\n\n"
            f"💰 Итого к оплате: {total_price} ₸\n\n"
            f"📞 По вопросам заказа: {MANAGER_CONTACT}"
        )
        
        await message.answer(text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
