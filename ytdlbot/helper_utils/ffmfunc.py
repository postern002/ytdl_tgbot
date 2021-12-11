import os
import subprocess

from ytdlbot import Config


async def fetch_thumb(user_id, thumbnail_url, video_id):
    down_dir = os.path.join(os.getcwd(), Config.DOWNLOAD_DIR, str(user_id), video_id)
    if not os.path.exists(down_dir):
        os.makedirs(down_dir)
    thumb_path = os.path.join(down_dir, video_id + ".jpg")

    # https://unix.stackexchange.com/a/349116
    subprocess.Popen(
        args=["ffmpeg", "-v", "quiet", "-n", "-i", thumbnail_url, thumb_path]
    ).communicate()
    return thumb_path
