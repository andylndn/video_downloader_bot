import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
import re
import requests

# Получаем токен из переменной окружения, используя имя секрета
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я твой видеобот! Отправь мне ссылку на видео.")

# Функция для проверки ссылок и скачивания видео
def get_video_url(link: str):
    # Псевдокод для обработки разных типов ссылок
    if "youtube" in link:
        # Используем сервис для скачивания с YouTube
        return "https://youtube.save.com/" + link
    elif "vk" in link:
        # Используем сервис для скачивания из ВК
        return "https://vk.download.com/" + link
    else:
        return None

# Обработчик получения ссылки от пользователя
@dp.message_handler()
async def handle_message(message: types.Message):
    # Проверка, является ли сообщение ссылкой
    link = message.text
    if re.match(r'https?://(?:www\.)?.+', link):
        video_url = get_video_url(link)

        if video_url:
            # Если ссылка подходит, отправляем ссылку на видео
            await message.reply(f"Загружаю видео с: {video_url}")
            # Здесь добавь логику для скачивания видео, например через requests
            video = requests.get(video_url)

            # Отправка видео пользователю
            with open("video.mp4", "wb") as f:
                f.write(video.content)
            
            # Отправка видео пользователю
            with open("video.mp4", "rb") as f:
                await bot.send_video(message.chat.id, f)
        else:
            await message.reply("Я не могу обработать эту ссылку. Попробуй другую.")
    else:
        await message.reply("Это не ссылка. Пожалуйста, отправь правильную ссылку.")

# Запуск бота
if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
