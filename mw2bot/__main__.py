import asyncio
import os
import signal
import sys

import disnake
from loguru import logger

if os.name == "nt":
    try:
        import dotenv
    except ModuleNotFoundError:
        pass

    else:
        if dotenv.find_dotenv():
            logger.info("Found .env file, loading environment variables from it.")
            dotenv.load_dotenv(override=True)


from mw2bot.bot import MW2Bot
from mw2bot.config import Config

_intents = disnake.Intents.none()
_intents.guilds = True
_intents.presences = True
_intents.members = True


async def main() -> None:
    """Create and run the bot"""
    bot = MW2Bot(intents=_intents, reload=True)

    try:
        bot.load_extensions()
    except Exception:
        await bot.close()
        raise

    logger.info("Bot is starting...")

    if os.name != "nt":
        # start process for linux based OS (Docker)

        loop = asyncio.get_event_loop()

        future = asyncio.ensure_future(bot.start(Config.token or ""), loop=loop)
        loop.add_signal_handler(signal.SIGINT, lambda: future.cancel())
        loop.add_signal_handler(signal.SIGTERM, lambda: future.cancel())

        try:
            await future
        except asyncio.CancelledError:

            logger.warning("Kill command was sent to the bot. Closing bot and event loop")
            if not bot.is_closed():
                await bot.close()
    else:
        await bot.start(Config.token)


if __name__ == "__main__":

    sys.exit(asyncio.run(main()))
