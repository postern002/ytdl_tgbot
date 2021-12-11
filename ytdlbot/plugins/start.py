from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command(["start"]))
async def _start(_, message):
    # return
    joinButton = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Channel", url="https://t.me/aryan_bots")],
            [InlineKeyboardButton("Report Bugs 😊", url="https://t.me/aryanvikash")],
        ]
    )
    welcomed = f"Hey <b>{message.from_user.first_name}</b>\n/help for More info"
    await message.reply_text(welcomed, reply_markup=joinButton)


@Client.on_message(filters.command(["help"]))
async def _help(_, message):
    helptxt = (
        "Currently Only supports Youtube Single  (No playlist) Just Send Youtube Url"
    )
    await message.reply_text(helptxt)
