import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
import yt_dlp
import os

from aiogram.filters import CommandStart
from aiogram.types import FSInputFile

from config import settings
from utils import setup_logging


dp = Dispatcher()

DOWNLOAD_DIR = "downloads/"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    await message.reply("YouTube shorts linkini tashlang va yuklab oling")


@dp.message(F.text.startswith('https://youtube.com/shorts/'))
async def download_youtube_shorts(message: types.Message, bot: Bot):
    url = message.text.strip()

    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{DOWNLOAD_DIR}%(title)s.%(ext)s',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        try:
            video = FSInputFile(file_path)
            await bot.send_video(
                chat_id=message.chat.id,
                video=video,
                caption=message.text,
            )
        except Exception as e:
            await message.reply(f"An error occurred: {e}")

        os.remove(file_path)
        await message.delete()
    except Exception as e:
        logging.error(f"An error occurred: {e}")


async def main():
    setup_logging()
    bot = Bot(token=settings.BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot has a problem!")
