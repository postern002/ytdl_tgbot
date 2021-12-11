import logging
import shutil

from pyrogram import Client

from ytdlbot import Config

logger = logging.getLogger(__name__)
"""
logger.info(f"{Config.APP_ID}")
logger.info(f"{Config.API_HASH}")
logger.info(f"{Config.BOT_TOKEN}")
print(Config.APP_ID)
print(Config.API_HASH)
print(Config.BOT_TOKEN)
"""
class YtDLBot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()

        plugins = dict(root=f"{name}/plugins")
        super().__init__(
            session_name=":memory:",
            api_id=Config.APP_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=100,
            plugins=plugins,
        )

    async def start(self):
        await super().start()
        bot = await self.get_me()
        logger.info(f"YtDLBot was started on @{bot.username}.")

    async def stop(self, *args):
        await super().stop()

        shutil.rmtree(Config.DOWNLOAD_DIR, ignore_errors=True)
        logger.info("YtDLBot stopped. Bye.")


if __name__ == "__main__":
    YtDLBot().run()
