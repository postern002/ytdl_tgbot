# from datetime import datetime

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser


def humanbytes(size):
    # https://stackoverflow.com/a/43690506
    for unit in ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]:
        if size < 1024.0 or unit == "PiB":
            break
        size /= 1024.0
    return f"{size:.2f} {unit}"


def width_and_height(thumbnail_path):
    metadata = extractMetadata(createParser(thumbnail_path))
    return metadata.get("width"), metadata.get("height")


def media_duration(media_path):
    metadata = extractMetadata(createParser(media_path))
    return metadata.get("duration").seconds


def time_formatter(seconds: int) -> str:
    result = ""
    remainder = seconds
    r_ange_s = {"days": (24 * 60 * 60), "hours": (60 * 60), "minutes": 60, "seconds": 1}
    for age, divisor in r_ange_s.items():
        v_m, remainder = divmod(remainder, divisor)
        v_m = int(v_m)
        if v_m != 0:
            result += f"{v_m} {age} "
    return result or "0 seconds"


"""def make_template(title, duration, upload_date):
    # Thanks to Userge-X
    # The template below was inspired after,
    # https://github.com/code-rgb/USERGE-X/blob/alpha/userge/plugins/bot/utube_inline.py#L448-L474
    formatted_duration = time_formatter(duration)
    uploaded = datetime.strptime(upload_date, "%Y%m%d").strftime("%d %B %Y")
    template = (
        f"<b>Title:</b> {title}\n\n"
        f"<b>Duration:</b> {formatted_duration}\n"
        f"<b>Uploaded on</b> {uploaded}"
    )
    return template"""
