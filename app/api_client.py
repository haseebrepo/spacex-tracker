import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import httpx

from app.cache import ICache, SQLiteCache
from app.settings import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class ISpaceXLaunchTracker(ABC):
    """
    Abstract interface for any SpaceX launch tracker implementation.
    """

    @abstractmethod
    def get_launches(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_rockets(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    def get_launchpads(self) -> List[Dict[str, Any]]:
        raise NotImplementedError


class SpaceXLaunchTrackerFactory:
    @staticmethod
    def get_tracker() -> ISpaceXLaunchTracker:
        return SpaceXClient(
            launch_cache=SQLiteCache(table="launches"),
            rocket_cache=SQLiteCache(table="rockets"),
            launchpad_cache=SQLiteCache(table="launchpads"),
        )


class SpaceXClient:
    def __init__(
        self,
        launch_cache: Optional[ICache] = None,
        rocket_cache: Optional[SQLiteCache] = None,
        launchpad_cache: Optional[SQLiteCache] = None,
    ):

        self._http_client = httpx.Client(timeout=10.0, headers=config.HEADERS)
        self._launch_cache = launch_cache
        self._rocket_cache = rocket_cache
        self._launchpad_cache = launchpad_cache

    def get_launches(self) -> List[Dict[str, Any]]:
        if self._launch_cache.is_valid():
            logger.info("Using valid cached launch data.")
            return self._launch_cache.load()
        logger.info("Fetching fresh launch data from API.")
        response = self._http_client.get(config.LAUNCHES_ENDPOINT)
        launches = response.json()
        self._launch_cache.save(launches)
        return launches

    def get_rockets(self) -> List[Dict[str, Any]]:
        if self._rocket_cache.is_valid():
            logger.info("Using cached rocket data.")
            return self._rocket_cache.load()
        logger.info("Fetching rocket data from API.")
        response = self._http_client.get(config.ROCKETS_ENDPOINT)
        rockets = response.json()
        self._rocket_cache.save(rockets)
        return rockets

    def get_launchpads(self) -> List[Dict[str, Any]]:
        if self._launchpad_cache.is_valid():
            logger.info("Using cached launchpad data.")
            return self._launchpad_cache.load()
        logger.info("Fetching launchpad data from API.")
        response = self._http_client.get(config.LAUNCHPADS_ENDPOINT)
        pads = response.json()
        self._launchpad_cache.save(pads)
        return pads
