from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import requests

router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Привет, <b>{message.from_user.full_name}</b>! Это бот для отслеживания товаров Wildberries, для отслеживания введите в чат артикул товара!")


@router.message(lambda message: message.text.isdigit())
async def handle_artikul(message: Message) -> None:
    artikul = int(message.text)
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/products",
            json={"artikul": artikul},
            headers={"Content-Type": "application/json"}
        )
        if response.status_code == 200:
            product = response.json()["product"]
            keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                InlineKeyboardButton(text="Подписаться", callback_data=f"subscribe_{artikul}")
            ]])
            await message.reply(
                f"Название товара: {product['name']}\n"
                f"Артикул: {product['artikul']}\n"
                f"Цена: {product['price']} RUB\n"
                f"Рейтинг: {product['rating']}\n"
                f"Количество: {product['volume']}",
                reply_markup=keyboard
            )
        else:
            await message.reply(f"Товар с артикулом {artikul} не найден")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")


@router.callback_query(lambda callback_query: callback_query.data.startswith("subscribe_"))
async def handle_subscribe(callback_query: CallbackQuery) -> None:
    artikul = int(callback_query.data.split("_")[1])
    try:
        response = requests.get(
            f"http://127.0.0.1:8000/api/v1/subscribe/{artikul}"
        )
        if response.status_code == 200:
            await callback_query.message.reply("Вы успешно подписались на уведомления о товаре!")
        else:
            await callback_query.message.reply("Не удалось оформить подписку. Попробуйте позже.")
    except Exception as e:
        await callback_query.message.reply(f"Произошла ошибка: {e}")
