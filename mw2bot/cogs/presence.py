from datetime import datetime

import disnake
from disnake.ext import commands
from loguru import logger

from mw2bot import data
from mw2bot.bot import MW2Bot


class Presence(commands.Cog):
    """Add some presence monitoring event callbacks"""

    def __init__(self, bot: MW2Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_presence_update(self, before: disnake.Member, after: disnake.Member) -> None:
        """Callback for presence changes"""

        # activity we're checking for
        name = (
            "Call of Duty",
            "Modern Warfare",
            "\u200bM\u200bo\u200bd\u200be\u200br\u200bn\u200bW\u200ba\u200br\u200bf\u200ba\u200br\u200be\u200b®\u200b2"
            "\u200bC\u200ba\u200bl\u200bl\u200b \u200bo\u200bf\u200b \u200bD\u200bu\u200bt\u200by\u200b®",
        )

        # check if member has started playing COD
        if not any(word in [a.name for a in before.activities] for word in name) and any(
            word in [a.name for a in after.activities] for word in name
        ):

            activity = [a for a in after.activities if name in a.name][0]
            start_time = datetime.timestamp(activity.start)

            player = data.load_player(after.member.id)

            if player is None:
                player = data.Player(_id=after.member.id, is_active=True, times=[])

            player.add_start_time(start_time)
            data.update_player(player)

            logger.info(f"{after.display_name} started paying COD at {activity.start} UTC")
            return

        # check if member has stopped playing COD
        if not any(word in [a.name for a in after.activities] for word in name) and any(
            word in [a.name for a in before.activities] for word in name
        ):

            end_time = datetime.timestamp(disnake.utils.utcnow())

            player = data.load_player(after.member.id)

            if player is None:
                # player doesn't exist and has no start time, so we'll just return
                # until they start a new session and are added to the json data
                return

            player.add_end_time(end_time)
            data.update_player(player)

            logger.info(
                f"{after.display_name} has stopped playing COD at {disnake.utils.utcnow()} UTC"
            )
            return


def setup(bot: MW2Bot) -> None:
    bot.add_cog(Presence(bot))
