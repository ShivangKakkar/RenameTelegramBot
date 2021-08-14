import shutil
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from Data import Data
from RenameBot.database import SESSION
from RenameBot.database.users_sql import Users


async def image_to_binary(image):
    with open(image, 'rb') as f:
        binary = f.read()
    return binary


# Callbacks
@Client.on_callback_query()
async def _callbacks(bot: Client, callback_query: CallbackQuery):
    user = await bot.get_me()
    mention = user["mention"]
    query = callback_query.data.lower()
    if query == "home":
        chat_id = callback_query.from_user.id
        message_id = callback_query.message.message_id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=Data.START.format(callback_query.from_user.mention, mention),
            reply_markup=InlineKeyboardMarkup(Data.buttons),
        )
    elif query == "about":
        chat_id = callback_query.from_user.id
        message_id = callback_query.message.message_id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=Data.ABOUT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )
    elif query == "help":
        chat_id = callback_query.from_user.id
        message_id = callback_query.message.message_id
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text="**Here's How to use me**\n" + Data.HELP,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(Data.home_buttons),
        )
    elif query in ["add_tn", "change_tn"]:
        await callback_query.message.delete()
        image_message = await bot.ask(callback_query.from_user.id, "Send a image to set as thumbnail",
                                      filters=filters.photo)
        await bot.send_message(callback_query.from_user.id, "Wait...Downloading and Saving...")
        image = await image_message.download()
        binary = await image_to_binary(image)
        q = SESSION.query(Users).get(callback_query.from_user.id)
        q.thumbnail = binary
        q.thumbnail_status = True
        SESSION.commit()
        await image_message.reply("Thumbnail Set !", quote=True)
        shutil.rmtree("downloads")
    elif query == "remove_tn":
        q = SESSION.query(Users).get(callback_query.from_user.id)
        q.thumbnail = ""
        q.thumbnail_status = False
        SESSION.commit()
        await callback_query.message.delete()
        await bot.send_message(callback_query.from_user.id, "Thumbnail Removed !")
    elif query == "tn_status_change":
        q = SESSION.query(Users).get(callback_query.from_user.id)
        if q.thumbnail_status:
            q.thumbnail_status = False
            switch = "Off"
        else:
            q.thumbnail_status = True
            switch = "On"
        SESSION.commit()
        await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Change Thumbnail", callback_data="change_tn")],
                [InlineKeyboardButton("Remove Thumbnail", callback_data="remove_tn")],
                [InlineKeyboardButton(f"Thumbnail Status : {switch}", callback_data="tn_status_change")]
            ])
        )
    elif query == "video_to_setting":
        q = SESSION.query(Users).get(callback_query.from_user.id)
        if q.video_to.lower() == "video":
            q.video_to = "document"
            now = "Document"
        else:
            q.video_to = "video"
            now = "Video"
        await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(f"Video to : {now}", callback_data="video_to_setting")]
            ])
        )
        SESSION.commit()
