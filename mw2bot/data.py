from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Tuple

from mw2bot.exceptions import NoActiveSession

__all__ = (
    "Activity",
    "Player",
    "log_start_time",
    "log_end_time",
    "load_players",
    "load_player",
    "update_player",
)

path = "./mw2bot/data/time.json"


@dataclass
class Activity:
    """Represents an activity"""

    start: float
    end: Optional[float] = None


@dataclass
class Player:

    _id: int
    is_active: bool
    times: List[Activity]
    total: int = None

    def __post_init_(self):
        """auto runs with class init"""
        self.calculate_total()

    @classmethod
    def from_tuple(cls, data: Tuple[str, dict]) -> Player:
        """Creates a player instance from dict data"""
        _id, times = data

        activities = [Activity(start=a["start"], end=a["end"]) for a in times]
        is_active = True if any(a.end is None for a in activities) else False
        player = cls(_id=int(_id), is_active=is_active, times=activities)
        player.calculate_total()

        return player

    def to_dict(self):
        """Returns this object as a dict"""
        return {str(self._id): [{"start": a.start, "end": a.end} for a in self.times]}

    def calculate_total(self):
        total = 0

        for a in self.times:
            if a.start and not a.end:
                continue
            total += (datetime.fromtimestamp(a.end) - datetime.fromtimestamp(a.start)).seconds

        self.total = total

    @property
    def total_as_string(self) -> str:
        """Return self.total as a formatted string"""
        days, remainder = divmod(self.total, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, remainder = divmod(remainder, 60)
        seconds, remainder = divmod(remainder, 60)

        return f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"

    def add_session(self, start: float, end: float) -> None:
        """Adds a new session to the player's times and updates total"""
        self.times.append(Activity(start=start, end=end))
        self.total = self.calculate_total()

    def add_start_time(self, start: float) -> None:
        self.times.append(Activity(start=start, end=None))

    def add_end_time(self, end: float) -> None:
        for time in self.times:
            if time.start and time.end is None:
                time.end = end
                return time


def load_data() -> dict[str, List[dict[str, float]]]:
    """Loads the data from json and returns a list of player objects"""
    with open(path) as f:
        return json.load(f)


def dump_data(data: dict) -> None:
    """Dumps the updated data to json"""
    with open(path, "w") as f:
        json.dump(data, f, indent=4)


def load_players() -> List[Player]:
    """Loads player data from the json and returns a list of `Player`"""
    data = load_data()
    players = []

    for k, v in data.items():
        players.append(Player.from_tuple((k, v)))

    return players


def load_player(member_id: int) -> Player:
    """Loads a player's data from the json data and returns the Player object"""
    data = load_data()

    for k, v in data.items():
        if k == str(member_id):
            return Player.from_tuple((k, v))


def update_player(player: Player) -> None:
    """Updates the player's json data"""
    player_data = player.to_dict()
    data = load_data()

    data.update(player_data)
    dump_data(data)
