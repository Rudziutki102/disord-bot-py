import os
from dotenv import dotenv_values
from typing import Final
from dotenv import load_dotenv
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")
MONGO_URI: Final[str] = os.getenv("MONGO_URI")
ALLOWED_ROLES: Final[int] = os.getenv("ALLOWED_ROLES").split(",")
CHANNELS_WITHOUT_TRACKING: Final[int] = set(
    map(int, os.getenv("NOT_TRACKABLE_CHANNELS").split(',')))
