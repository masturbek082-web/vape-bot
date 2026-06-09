from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio, json, os

TOKEN = '8931007305:AAGewyuIKAX_pt2YxzpWj9WYP1lMD5i6XdM'
MANAGER_ID = 123456789  # <--- ВСТАВЬ СЮДА ID МЕНЕДЖЕРА!
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для сохранения номера заказа
def get_next_order_id():
    count = 1
    if os.path.exists("order_count.txt"):
        with open("order_count.txt", "r") as f:
            count = int(f.read().strip()) + 1
    with open("order_count.txt", "w") as f:
        f.write(str(count))
    return count

@dp.message(Command("start"))
async def start(message: types.Message):
    btn = types.InlineKeyboardButton(text="🛒 Открыть магазин", web_app=types.WebAppInfo(url="https://myshop-sooty-tau.vercel.app"))
    kb = types.InlineKeyboardMarkup(inline_keyboard=[[btn]])
    await message.answer("Добро пожаловать в магазин! Нажми кнопку ниже:", reply_markup=kb)

@dp.message()
async def handle_data(message: types.Message):
    if message.web_app_data:
        data = json.loads(message.web_app_data.data)
        order_id = get_next_order_id()
        total = sum([i['price'] for i in data['cart']])
        items_text = "\n".join([f"• {i['item']} ({i['price']} ₸)" for i in data['cart']])
        
        full_text = (f"✅ ЗАКАЗ №{order_id}\n\n👤 Клиент: {data['name']}\n📱 Тел: {data['phone']}\n🏠 Адрес: {data['addr']}\n\n"
                     f"🛒 Товары:\n{items_text}\n\n💰 Итого: {total} ₸")

        # Отправляем менеджеру
        await bot.send_message(MANAGER_ID, f"🔔 НОВЫЙ ЗАКАЗ!\n\n{full_text}")
        # Отправляем клиенту
        await message.answer(f"Спасибо! Ваш заказ принят.\n\n{full_text}\n\n📞 Свяжемся с вами в ближайшее время.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
