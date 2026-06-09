import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# ====== НАСТРОЙКА БОТА ======
TOKEN = "8931007305:AAGewyuIKAX_pt2YxzpWj9WYP1lMD5i6XdM" 
WEB_APP_URL = "https://myshop-sooty-tau.vercel.app" 

# !!! ОБЯЗАТЕЛЬНО: Впиши сюда свой ID из @userinfobot вместо этих цифр:
MANAGER_ID = 123456789  
# ============================

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="🛒 Открыть магазин", web_app=types.WebAppInfo(url=WEB_APP_URL))]
        ],
        resize_keyboard=True
    )
    await message.answer("💨 Добро пожаловать! Нажми на кнопку ниже, чтобы открыть каталог товаров:", reply_markup=keyboard)

@dp.message()
async def handle_order(message: types.Message):
    if message.web_app_data:
        data = json.loads(message.web_app_data.data)
        user = message.from_user
        
        username = f"@{user.username}" if user.username else user.first_name
        
        order_text = (
            f"🔔 ЧЕЛОВЕК СДЕЛАЛ ЗАКАЗ!\n\n"
            f"👤 Покупатель: {username} (ID: {user.id})\n"
            f"📦 Товар: {data.get('item')}\n"
            f"💰 Цена: {data.get('price')} ₸"
        )
        
        await bot.send_message(chat_id=MANAGER_ID, text=order_text)
        await message.answer("✅ Твой заказ отправлен менеджеру! Он свяжется с тобой в ближайшее время.")

async def main():
    print("Бот успешно запущен и ждет заказов...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
