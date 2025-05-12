import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import yt_dlp
from aiogram.utils import executor
import re

API_TOKEN = '7036607708:AAFpRYZJvYwS_mlMbPKoj_SzBx4tPoTLFQA'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

async def download_video(url):
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_file = ydl.prepare_filename(info_dict)
    return video_file

def is_valid_url(url):
    youtube_pattern = r'(https?://(?:www\.)?youtube\.com/watch\?v=[\w-]+)'
    vk_pattern = r'(https?://(?:www\.)?vk\.com/video[\w-]+)'

    return re.match(youtube_pattern, url) or re.match(vk_pattern, url)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Скачать видео с YouTube", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    keyboard.add(button)

    await message.reply("Привет! Отправь мне ссылку на видео, и я помогу скачать!", reply_markup=keyboard)

@dp.message_handler()
async def handle_video_link(message: types.Message):
    url = message.text.strip()

    if not is_valid_url(url):
        await message.reply("Это не ссылка на видео с YouTube или VK! Пожалуйста, отправьте правильную ссылку.")
        return

    await message.reply("Загружаю видео...")
    try:
        video_path = await download_video(url)
        with open(video_path, 'rb') as video_file:
            await bot.send_video(message.chat.id, video_file)
        os.remove(video_path)
    except Exception as e:
        await message.reply(f"Ошибка при скачивании: {str(e)}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
