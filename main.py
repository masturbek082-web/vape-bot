import asyncio
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# ====== НАСТРОЙКА БОТА ======
TOKEN = "8931007305:AAGewyuIKAX_pt2YxzpWj9WYP1lMD5i6XdM" 
WEB_APP_URL = "https://myshop-sooty-tau.vercel.app" 

# Данные менеджера (Ярослав)
MANAGER_ID = 8940897499  
MANAGER_USERNAME = "vk6996"
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
        
        # 1. Чек, который прилетает тебе в личку (от бота)
        order_text_to_manager = (
            f"🔔 НОВЫЙ ЗАКАЗ ИЗ МАГАЗИНА!\n\n"
            f"👤 Покупатель: {username} (ID: {user.id})\n"
            f"📝 Имя в заказе: {data.get('name')}\n"
            f"📞 Телефон: {data.get('phone')}\n"
            f"📍 Адрес доставки: {data.get('address')}\n"
            f"💳 Способ оплаты: {data.get('payment')}\n\n"
            f"📦 Состав заказа: {data.get('items')}\n"
            f"💰 Сумма к оплате: {data.get('total')} ₸"
        )
        await bot.send_message(chat_id=MANAGER_ID, text=order_text_to_manager)
        
        # 2. Подробный чек, который видит сам КЛИЕНТ в чате с ботом
        order_text_to_client = (
            f"✅ Спасибо за заказ, {data.get('name')}!\n\n"
            f"🧾 ВАШ ЗАКАЗ:\n"
            f"───────────────────\n"
            f"📦 Товары: {data.get('items')}\n"
            f"💰 Итого: {data.get('total')} ₸\n"
            f"💳 Оплата: {data.get('payment')}\n"
            f"📍 Доставка: {data.get('address')}\n"
            f"───────────────────\n\n"
            f"Менеджер уже обрабатывает ваш заказ и свяжется с вами по номеру {data.get('phone')}.\n\n"
            f"👨‍💻 По всем вопросам пишите менеджеру: @{MANAGER_USERNAME}"
        )
        await message.answer(order_text_to_client)

async def main():
    print("Бот успешно запущен и ждет заказов...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
