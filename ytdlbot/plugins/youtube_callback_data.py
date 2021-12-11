import asyncio
import logging
import os
import re
import shutil

from pyrogram import Client, filters
from pyrogram.types import (
    InputMediaAudio,
    InputMediaVideo,
)

from ytdlbot import Config
from ytdlbot.helper_utils.util import media_duration, width_and_height
from ytdlbot.helper_utils.ytdlfunc import yt_download

logger = logging.getLogger(__name__)
ytdata = re.compile(r"^(Video|Audio)_(\d{1,3})_(empty|none)_([\w\-]+)$")


@Client.on_callback_query(filters.regex(ytdata))
async def catch_youtube_dldata(_, q):
    cb_data = q.data
    logger.info(cb_data)
    # caption = q.message.caption
    user_id = q.from_user.id
    # Callback Regex capturing
    media_type = q.matches[0].group(1)
    format_id = q.matches[0].group(2)
    av_codec = q.matches[0].group(3)
    video_id = q.matches[0].group(4)

    userdir = os.path.join(os.getcwd(), Config.DOWNLOAD_DIR, str(user_id), video_id)

    if not os.path.isdir(userdir):
        os.makedirs(userdir)
    await q.edit_message_caption("Downloading...!")
    # await q.edit_message_reply_markup([[InlineKeyboardButton("Processing..")]])

    fetch_media, caption = await yt_download(
        video_id, media_type, av_codec, format_id, userdir
    )
    if not fetch_media:
        await asyncio.gather(q.message.reply_text(caption), q.message.delete())
        shutil.rmtree(userdir, ignore_errors=True)
        return
    else:
        logger.info(os.listdir(userdir))
        file_name = None
        for content in os.listdir(userdir):
            if ".jpg" not in content:
                file_name = os.path.join(userdir, content)

    if not os.path.exists(file_name):
        await asyncio.gather(q.message.reply_text("Failed"), q.message.delete())
        logger.info("Media not found")
        return

    thumb = os.path.join(userdir, video_id + ".jpg")
    if not os.path.exists(thumb):
        thumb = None
        width = height = 0
    else:
        width, height = width_and_height(thumb)

    duration = media_duration(file_name)
    media = None
    if media_type == "Audio":
        media = InputMediaAudio(
            media=file_name,
            thumb=thumb,
            duration=duration,
            caption=caption,
            title=caption,
        )

    elif media_type == "Video":
        media = InputMediaVideo(
            media=file_name,
            thumb=thumb,
            width=width,
            height=height,
            duration=duration,
            caption=caption,
            supports_streaming=True,
        )

    logger.info(media)
    try:
        await q.edit_message_media(media=media)
    except Exception as e:
        logger.info(e)
        await q.edit_message_text(e)
    finally:
        shutil.rmtree(userdir, ignore_errors=True)  # Cleanup
