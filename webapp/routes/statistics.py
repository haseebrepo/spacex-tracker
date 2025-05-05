from typing import Dict

from fastapi import APIRouter, Depends

from app.models import LaunchModel
from app.statistics import (
    compute_success_rates_by_rocket,
    count_launches_per_site,
    get_launch_frequency_by_month,
    get_launch_frequency_by_year,
)
from webapp.dependencies import (
    get_launchpad_id_to_name_map,
    get_parsed_launches,
    get_rocket_id_to_name_map,
)

router = APIRouter()


@router.get("/success-rate", response_model=Dict[str, float])
def success_rate_by_rocket(
    launches: list[LaunchModel] = Depends(get_parsed_launches),
    rocket_map: dict = Depends(get_rocket_id_to_name_map),
):
    """
    Success rate of launches per rocket (as %).
    """
    return compute_success_rates_by_rocket(launches, rocket_map)


@router.get("/launchpads", response_model=Dict[str, int])
def total_launches_per_site(
    launches: list[LaunchModel] = Depends(get_parsed_launches),
    launchpad_map: dict = Depends(get_launchpad_id_to_name_map),
):
    """
    Number of launches per launch site.
    """
    return count_launches_per_site(launches, launchpad_map)


@router.get("/monthly", response_model=Dict[str, int])
def launches_by_month(launches: list[LaunchModel] = Depends(get_parsed_launches)):
    """
    Number of launches per month (YYYY-MM).
    """
    return get_launch_frequency_by_month(launches)


@router.get("/yearly", response_model=Dict[str, int])
def launches_by_year(launches: list[LaunchModel] = Depends(get_parsed_launches)):
    """
    Number of launches per year (YYYY).
    """
    return get_launch_frequency_by_year(launches)
