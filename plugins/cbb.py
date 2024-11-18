from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text = (
                f"<b>📝 ᴏᴡɴᴇʀ :</b> <a href='https://t.me/rai_yan_00'>Rᴀɪ Yᴀɴ</a>\n"
                f"<b>📚 ᴍᴀɪɴ ᴄʜʜᴀɴɴᴇʟ :</b> <a href='https://t.me/ani_weebs'>ᴀɴɪᴍᴇ ᴡᴇᴇʙs</a>\n"
                f"<b>🎬 ᴀɪʀɪɴɢ :</b> <a href='https://t.me/ongoing_anime_weebs'>ᴏɴɢᴏɪɴɢ ᴀɴɪᴍᴇ ᴡᴇᴇʙs</a>\n"
                f"<b>📖 ᴍᴀɴʜᴡᴀ :</b> <a href='https://t.me/manhwa_weebs'>ᴍᴀɴʜᴡᴀ ᴡᴇᴇʙs</a>\n"
                f"<b>💬 ᴀɴɪᴍᴇ ᴄʜᴀᴛ :</b> <a href='https://t.me/Weebs_Gc'>ᴡᴇᴇʙs ɢᴄ</a>"
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 ᴄʟᴏsᴇ", callback_data="close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

# Rai Yan Developer 
# Don't Remove Credit 🥺
# Main Channel @ani_weebs
# Airing Channel @ongoing_anime_weebs
# Manhwa Channel @manhwa_weebs
# Chat Group @Weebs_Gc
# Owner @rai_yan_00# Backup Channel @JishuBotz
# Developer @JishuDeveloper
