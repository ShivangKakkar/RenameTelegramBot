from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from RenameBot.database import SESSION
from RenameBot.database.users_sql import Users


@Client.on_message(filters.private & filters.command("settings") & ~filters.edited)
async def _settings(_, msg: Message):
    q = SESSION.query(Users).get(msg.from_user.id)
    if q.video_to.lower() == "video":
        conversion_to = "Video"
    else:
        conversion_to = "Document"
    SESSION.close()
    await msg.reply(
        "**ıllıllııllıllı★ SETTINGS ★ıllıllııllıllı** \n\nBelow are the settings of Rename Bot. Use below buttons to interact with bot and change settings.",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(f"Video to : {conversion_to}", callback_data="video_to_setting")]
        ])
    )
