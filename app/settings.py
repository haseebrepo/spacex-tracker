import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Config(BaseModel):
    BASE_URL: str = os.getenv("SPACEX_API_BASE", "https://api.spacexdata.com/v4")
    LAUNCHES_ENDPOINT: str = f"{BASE_URL}/launches"
    ROCKETS_ENDPOINT: str = f"{BASE_URL}/rockets"
    LAUNCHPADS_ENDPOINT: str = f"{BASE_URL}/launchpads"

    DB_PATH: str = os.getenv("CACHE_DB_PATH", "cache/launch_cache.db")
    CACHE_TTL_SECONDS: int = int(os.getenv("CACHE_TTL_SECONDS", "3600"))

    HEADERS: dict = {
        "Accept": "application/json",
        "User-Agent": "SpaceX-Launch-Tracker/1.0",
    }


config = Config()
