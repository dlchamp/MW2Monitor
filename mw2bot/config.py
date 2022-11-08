import os


class Config:
    """Handles the bot config"""

    token: str = os.getenv("TOKEN")
