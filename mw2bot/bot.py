import os
from datetime import datetime
from sys import version as sys_version

import disnake
from disnake import __version__ as disnake_version
from disnake.ext import commands
from loguru import logger

from mw2bot import __version__ as bot_version

__all__ = ("MW2Bot",)


class MW2Bot(commands.InteractionBot):
    """Base bot instance"""

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.times = {}

    async def on_ready(self) -> None:

        print(
            "----------------------------------------------------------------------\n"
            f'Bot started at: {datetime.now().strftime("%m/%d/%Y - %H:%M:%S")}\n'
            f"System Version: {sys_version}\n"
            f"Disnake Version: {disnake_version}\n"
            f"Bot Version: {bot_version}\n"
            f"Connected to Discord as {self.user} ({self.user.id})\n"
            "----------------------------------------------------------------------\n"
        )

    def load_extensions(self) -> None:
        """Load all extensions available on 'cogs'"""
        for item in os.listdir("mw2bot/cogs"):
            if "__" in item:
                continue

            self.load_extension(f"mw2bot.cogs.{item[:-3]}")
            logger.info(f"Cog loaded: {item[:-3]}")
