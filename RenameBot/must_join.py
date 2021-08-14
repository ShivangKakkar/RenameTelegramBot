from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import ChatAdminRequired, UserNotParticipant
from Config import MUST_JOIN


@Client.on_message(filters=(~filters.edited & ~filters.service & filters.user & filters.incoming), group=-1)
async def must_join_channel(bot: Client, msg: Message):
    try:
        try:
            await bot.get_chat_member(MUST_JOIN, msg.from_user.id)
        except UserNotParticipant:
            if MUST_JOIN.isalpha():
                link = "https://t.me/" + MUST_JOIN
            else:
                chat_info = await bot.get_chat(MUST_JOIN)
                link = chat_info.invite_link
            await msg.reply(
                f"You must join [this channel]({link}) to use this bot. After joining try again !",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✨ Join Channel ✨", url=link)]
                ])
            )
            await msg.stop_propagation()
    except ChatAdminRequired:
        print(f"I'm not admin in the MUST_JOIN chat : {MUST_JOIN} !")
