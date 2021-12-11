import asyncio
import re
from datetime import datetime, timedelta

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup
from yt_dlp.utils import DownloadError, ExtractorError

from ytdlbot import Config, user_time
from ytdlbot.helper_utils.ffmfunc import fetch_thumb
from ytdlbot.helper_utils.ytdlfunc import extract_formats

ytregex = re.compile(
    r"^((?:https?:)?//)?((?:www|m)\.)?(youtube\.com|youtu.be)(/(?:[\w\-]+\?v=|embed/|v/)?)([\w\-]+)(\S+)?$"
)


@Client.on_message(filters.regex(ytregex))
async def ytdl(_, message):
    user_id = message.from_user.id
    userLastDownloadTime = user_time.get(user_id)
    if userLastDownloadTime and userLastDownloadTime > datetime.now():
        wait_time = round(
            (userLastDownloadTime - datetime.now()).total_seconds() / 60, 2
        )
        await message.reply_text(f"`Wait {wait_time} Minutes before next Request`")
        return

    url = message.text.strip()
    await message.reply_chat_action("typing")
    try:
        video_id, thumbnail_url, title, buttons = await extract_formats(url)

        now = datetime.now()
        user_time[user_id] = now + timedelta(minutes=Config.TIMEOUT)

    except (DownloadError, ExtractorError) as error:
        await asyncio.gather(
            message.reply_chat_action("cancel"),
            message.reply_text(f"{error}", quote=True, disable_web_page_preview=True),
        )
        return

    status = await message.reply_text("Fetching thumbnail...", quote=True)
    if Config.CUSTOM_THUMB:
        await asyncio.sleep(Config.EDIT_TIME)
        await status.edit_text("Found Custom thumbnail, Gotta pull it now.")
        thumbnail_url = Config.CUSTOM_THUMB
    thumbnail = await fetch_thumb(user_id, thumbnail_url, video_id)
    try:
        await asyncio.gather(
            message.reply_photo(
                thumbnail, caption=title, reply_markup=InlineKeyboardMarkup(buttons)
            ),
            status.delete(),
        )
    except Exception as e:
        await status.edit(f"<code>{e}</code> #Error")
