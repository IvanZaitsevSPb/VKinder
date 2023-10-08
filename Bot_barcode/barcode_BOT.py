import asyncio
import logging
import sys

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from Token_API import TOKEN_API
import io
from PIL import Image
import os
from Filters import IsPrivate

# Импорт функции
from my_function import BarcodeReader

TOKEN = TOKEN_API

# Все обработчики должны быть подключены к маршрутизатору (или диспетчеру)
dp = Dispatcher()


@dp.message(IsPrivate())
async def echo_handler(message: types.Message) -> None:
    """
        Обработчик для отлова фотографий без команды в личных сообщениях
    """

    # URI для скачивания фото
    URI_INFO = f"https://api.telegram.org/bot{TOKEN_API}/getFile?file_id="
    URI = f"https://api.telegram.org/file/bot{TOKEN_API}/"

    # Получение и обработка фото
    file_id = message.photo[3].file_id
    resp = requests.get(URI_INFO + file_id)
    img_path = resp.json()['result']['file_path']
    img = requests.get(URI + img_path)

    # Декодирование фотографии и сохранение
    img = Image.open(io.BytesIO(img.content))
    if not os.path.exists('static'):
        os.mkdir('static')
    img.save(f'static/001.png', format='PNG')
    img = BarcodeReader('static/001.png')
    try:
        # Отправление копии полученного сообщения и текста функции
        await message.send_copy(chat_id=message.chat.id),
        await message.reply(img)
    except TypeError:
        # Не все типы поддерживают копирование
        await message.answer("Nice try!")

@dp.message(Command('scan_barcode'))
async def echo_handler(message: types.Message) -> None:
    """
        Обработчик для отлова фотографий по команде '/scan_barcode' во всех чатах по команде
    """

    # URI для скачивания фото
    URI_INFO = f"https://api.telegram.org/bot{TOKEN_API}/getFile?file_id="
    URI = f"https://api.telegram.org/file/bot{TOKEN_API}/"

    # Получение и обработка фото
    file_id = message.photo[3].file_id
    resp = requests.get(URI_INFO + file_id)
    img_path = resp.json()['result']['file_path']
    img = requests.get(URI + img_path)

    # Декодирование фотографии и сохранение
    img = Image.open(io.BytesIO(img.content))
    if not os.path.exists('static'):
        os.mkdir('static')
    img.save(f'static/001.png', format='PNG')
    img = BarcodeReader('static/001.png')
    try:
        # Отправление копии полученного сообщения и текста функции
        await message.send_copy(chat_id=message.chat.id),
        await message.reply(img)
    except TypeError:
        # Не все типы поддерживают копирование
        await message.answer("Nice try!")


@dp.message(Command('scan_reply'))
async def echo_handler(message: types.Message) -> None:
    """
        Обработчик для отлова фотографий по команде '/scan_reply' во всех чатах по команде и реплаю
    """

    # URI для скачивания фото
    URI_INFO = f"https://api.telegram.org/bot{TOKEN_API}/getFile?file_id="
    URI = f"https://api.telegram.org/file/bot{TOKEN_API}/"

    # Получение и обработка фото
    file_id = message.reply_to_message.photo[3].file_id
    resp = requests.get(URI_INFO + file_id)
    img_path = resp.json()['result']['file_path']
    img = requests.get(URI + img_path)

    # Декодирование фотографии и сохранение
    img = Image.open(io.BytesIO(img.content))
    if not os.path.exists('static'):
        os.mkdir('static')
    img.save(f'static/001.png', format='PNG')
    img = BarcodeReader('static/001.png')
    try:
        await message.answer(img)
    except AttributeError:
        await message.answer("Nice try!")


async def main() -> None:
    # Инициализация для вызова API
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # Запуск диспетчера
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())