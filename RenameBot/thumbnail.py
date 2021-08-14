from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from RenameBot.database import SESSION
from RenameBot.database.users_sql import Users
from io import BytesIO


@Client.on_message(filters.private & filters.command(["thumbnail", "tn"]) & ~filters.edited)
async def _thumbnail(_, msg: Message):
    q = SESSION.query(Users).get(msg.from_user.id)
    if q.thumbnail_status:
        switch = "On"
    else:
        switch = "Off"
    if q.thumbnail:
        thumbnail = q.thumbnail
        thumbnail = BytesIO(thumbnail)
        thumbnail.name = "image.jpg"
        await msg.reply_photo(
            thumbnail,
            caption="This is the current thumbnail",
            reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✨ Change Thumbnail ✨", callback_data="change_tn")],
                    [InlineKeyboardButton("✨ Remove Thumbnail ✨", callback_data="remove_tn")],
                    [InlineKeyboardButton(f"Thumbnail Status : {switch}", callback_data="tn_status_change")]
            ])
        )
    else:
        await msg.reply(
            "No Thumbnail Found",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✨ Add Thumbnail ✨", callback_data="add_tn")]
            ])
        )
    SESSION.close()
