import logging
from typing import List, Optional

from fastapi import APIRouter, Depends, Query

logger = logging.getLogger(__name__)

from app.filters import (
    filter_by_date_range,
    filter_by_launchpad,
    filter_by_rocket_name,
    filter_by_success,
)
from app.models import LaunchModel
from webapp.dependencies import (
    get_launchpad_id_to_name_map,
    get_parsed_launches,
    get_rocket_id_to_name_map,
)

router = APIRouter()


@router.get("/", response_model=List[LaunchModel])
def list_launches(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    success: Optional[bool] = Query(None, description="Filter by launch success"),
    rocket_name: Optional[str] = Query(None, description="Filter by rocket name"),
    launchpad_name: Optional[str] = Query(
        None, description="Filter by launch site name"
    ),
    launches: List[LaunchModel] = Depends(get_parsed_launches),
    rocket_map: dict = Depends(get_rocket_id_to_name_map),
    launchpad_map: dict = Depends(get_launchpad_id_to_name_map),
):
    """
    Retrieve filtered list of SpaceX launches.
    """
    filtered = filter_by_date_range(launches, start_date, end_date)
    filtered = filter_by_success(filtered, success)
    filtered = filter_by_rocket_name(filtered, rocket_map, rocket_name)
    filtered = filter_by_launchpad(filtered, launchpad_map, launchpad_name)

    return filtered
