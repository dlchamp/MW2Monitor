from datetime import datetime, timedelta
from typing import Optional

import disnake
from disnake.ext import commands

from mw2bot import data
from mw2bot.bot import MW2Bot
from mw2bot.exceptions import MonitorStarted, NoActiveSession


class Commands(commands.Cog):
    """Add some commands"""

    def __init__(self, bot: MW2Bot):
        self.bot = bot

    @commands.slash_command(name="leaderboard")
    async def leaderboard(self, inter: disnake.AppCmdInter) -> None:
        """Display the leaderboard for time spent playing COD"""

        guild = inter.guild
        # load players and sort by total time played (seconds)
        players = data.load_players()

        if players == [] or players is None:
            return await inter.response.send_message(
                "No players have logged any sessions", ephemeral=True
            )

        players = sorted(players, key=lambda p: p.total, reverse=True)

        # join the players into a formatted string
        players = "\n".join(
            [
                f"{i}. {guild.get_member(p._id).mention} - {p.total_as_string}"
                for i, p in enumerate(players, 1)
            ]
        )

        # build and send the emebd as the inter response
        embed = disnake.Embed(title="MW2 Time Played Leaderboard", description=players)
        await inter.response.send_message(embed=embed)

    @commands.slash_command(name="start_session")
    async def add_start(self, inter: disnake.AppCmdInter) -> None:
        """Logs a new session's start time"""

        player = data.load_player(inter.author.id)

        if player is not None and player.is_active:
            return await inter.response.send_message(
                "You're already in an active session. You must stop the current session before starting a new one.",
                ephemeral=True,
            )

        started = disnake.utils.utcnow()
        started_as_timestamp = datetime.timestamp(started)

        if player is None:
            player = data.Player(
                _id=inter.author.id,
                is_active=True,
                times=[],
            )

        player.add_start_time(started_as_timestamp)
        data.update_player(player)

        embed = disnake.Embed(
            title=f"{inter.author.display_name} has started a session",
            description=f'Started at - {disnake.utils.format_dt(started, "T")}\n'
            f'Active Since - {disnake.utils.format_dt(started, "R")}',
        )

        await inter.response.send_message(embed=embed)

    @commands.slash_command(name="end_session")
    async def add_end(self, inter: disnake.AppCmdInter) -> None:
        """Ends a currently running session"""

        command = self.bot.get_slash_command("start_session")
        player = data.load_player(inter.author.id)

        if player is None:

            return await inter.response.send_message(
                f"You haven't logged any sessions.  Please load up Modern Warfare 2, or start a new session with </{command.name}:{command.id}>",
                ephemeral=True,
            )

        ended = disnake.utils.utcnow()
        ended_as_timestamp = datetime.timestamp(ended)

        if player and not player.is_active:
            return await inter.response.send_message(
                f"You don't have any currently active sessions.  Please start up Modern Warfare or start a session with </{command.name}:{command.id}>"
            )

        activity = player.add_end_time(ended_as_timestamp)
        data.update_player(player)

        embed = disnake.Embed(
            title=f"{inter.author.display_name} has ended their session",
            description=f'Ended at - {disnake.utils.format_dt(ended, "T")}\n'
            f'Started {disnake.utils.format_dt(activity.start, "R")}',
        )

        await inter.response.send_message(embed=embed)

    @commands.slash_command(name="add_session")
    async def new_session(
        self,
        inter: disnake.AppCmdInter,
        hours: Optional[int] = commands.Param(default=0, max_value=23),
        minutes: Optional[int] = commands.Param(default=0, max_value=59),
    ) -> None:
        """Add a new session by length.

        Parameters
        ----------
        hours: :type:`Optional[int]`
            How many hours was your session? (Default 0)
        minutes: :type:`Optional[int]`
            How many minutes was your session? (Default 0)
        """
        player = data.load_player(inter.author.id)

        now = disnake.utils.utcnow()
        started_at = now - timedelta(hours=hours, minutes=minutes)

        if player is None:
            player = data.Player(_id=inter.author.id, is_active=False, times=[])

        player.add_session(datetime.timestamp(started_at), datetime.timestamp(now))

        # store the updated player in json
        data.update_player(player)

        # build the emebd and send response
        embed = disnake.Embed(
            title=f"{inter.author.display_name} added a new session!",
            description=f'Started at - {disnake.utils.format_dt(started_at, "T")}\n'
            f'Ended at - {disnake.utils.format_dt(now, "T")}\n',
        )

        await inter.response.send_message(embed=embed)


def setup(bot: MW2Bot) -> None:
    bot.add_cog(Commands(bot))
