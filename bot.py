import os, asyncio, humanize
from aiohttp import web
from plugins import web_server
import pyromod.listen
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from config import API_HASH, API_ID, LOGGER, BOT_TOKEN, TG_BOT_WORKERS, FORCE_SUB_CHANNEL, FORCE_SUB_CHANNEL2, CHANNEL_ID, PORT
import pyrogram.utils

# Set MIN_CHANNEL_ID for compatibility
pyrogram.utils.MIN_CHANNEL_ID = -1009999999999

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=API_ID,
            plugins={"root": "plugins"},
            workers=TG_BOT_WORKERS,
            bot_token=BOT_TOKEN
        )
        self.LOGGER = LOGGER

    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()

        # Handle FORCE_SUB_CHANNEL logic
        if FORCE_SUB_CHANNEL:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL)).invite_link
                self.invitelink = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).info("Bot stopped due to FORCE_SUB_CHANNEL setup issue.")
                sys.exit()

        # Handle FORCE_SUB_CHANNEL2 logic
        if FORCE_SUB_CHANNEL2:
            try:
                link = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                if not link:
                    await self.export_chat_invite_link(FORCE_SUB_CHANNEL2)
                    link = (await self.get_chat(FORCE_SUB_CHANNEL2)).invite_link
                self.invitelink2 = link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).info("Bot stopped due to FORCE_SUB_CHANNEL2 setup issue.")
                sys.exit()

        # Set up the DB channel
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id=db_channel.id, text="Hey 🖐")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).info("Bot stopped due to CHANNEL_ID setup issue.")
            sys.exit()

        # Web server setup
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, PORT).start()

        self.LOGGER(__name__).info("Bot running..!")
        self.username = usr_bot_me.username

    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot Stopped...")

# Commenting out all non-essential code and functionalities
# @Bot.on_message(filters.command('start') & filters.private & subscribed)
# async def start_command(client: Client, message: Message):
#     # Start command code here (commented out for simplicity)

# Only keeping the video ID functionality
@Bot.on_message(filters.video & filters.private)
async def get_video_id(client, message):
    video_id = message.video.file_id
    await message.reply(f"Video ID: `{video_id}`", quote=True)

# Initialize the bot
if __name__ == "__main__":
    bot = Bot()
    bot.run()
