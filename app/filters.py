from datetime import datetime, timezone
from typing import List, Optional

from app.models import LaunchModel
from app.utils import parse_date


def filter_by_date_range(
    launches: List[LaunchModel],
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> List[LaunchModel]:
    if not start_date and not end_date:
        return launches

    start = (
        parse_date(start_date)
        if start_date
        else datetime.min.replace(tzinfo=timezone.utc)
    )
    end = (
        parse_date(end_date) if end_date else datetime.max.replace(tzinfo=timezone.utc)
    )

    return [launch for launch in launches if start <= launch.date_utc <= end]


def filter_by_success(
    launches: List[LaunchModel], success: Optional[bool] = None
) -> List[LaunchModel]:
    if success is None:
        return launches

    return [launch for launch in launches if launch.success == success]


def filter_by_rocket_name(
    launches: List[LaunchModel],
    rocket_id_to_name: dict,
    rocket_name: Optional[str] = None,
) -> List[LaunchModel]:
    if not rocket_name:
        return launches

    return [
        launch
        for launch in launches
        if launch.rocket.name.lower() == rocket_name.lower()
    ]


def filter_by_launchpad(
    launches: List[LaunchModel],
    launchpad_id_to_name: dict,
    launchpad_name: Optional[str] = None,
) -> List[LaunchModel]:
    if not launchpad_name:
        return launches

    return [
        launch
        for launch in launches
        if launch.launchpad.name.lower() == launchpad_name.lower()
    ]
