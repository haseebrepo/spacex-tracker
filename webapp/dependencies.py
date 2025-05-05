from functools import lru_cache

from app.api_client import ISpaceXLaunchTracker, SpaceXLaunchTrackerFactory
from app.models import LaunchModel
from app.utils import enrich_launches


@lru_cache()
def get_tracker() -> ISpaceXLaunchTracker:
    return SpaceXLaunchTrackerFactory.get_tracker()


@lru_cache()
def get_rocket_id_to_name_map() -> dict:
    tracker = get_tracker()
    return {r["id"]: r["name"] for r in tracker.get_rockets()}


@lru_cache()
def get_launchpad_id_to_name_map() -> dict:
    tracker = get_tracker()
    return {p["id"]: p["name"] for p in tracker.get_launchpads()}


def get_parsed_launches() -> list[LaunchModel]:
    tracker = get_tracker()
    rocket_map = get_rocket_id_to_name_map()
    launchpad_map = get_launchpad_id_to_name_map()
    raw = tracker.get_launches()
    return enrich_launches(raw, rocket_map, launchpad_map)
