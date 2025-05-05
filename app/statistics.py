from collections import defaultdict
from typing import Dict, List

from app.models import LaunchModel


def compute_success_rates_by_rocket(
    launches: List[LaunchModel], rocket_id_to_name: Dict[str, str]
) -> Dict[str, float]:
    """
    Returns success rate (%) per rocket.
    """
    stats = defaultdict(lambda: {"total": 0, "success": 0})

    for launch in launches:
        rocket_name = launch.rocket.name
        stats[rocket_name]["total"] += 1
        if launch.success is True:
            stats[rocket_name]["success"] += 1

    return {
        rocket: round((data["success"] / data["total"]) * 100, 2)
        for rocket, data in stats.items()
        if data["total"] > 0
    }


def count_launches_per_site(
    launches: List[LaunchModel], launchpad_id_to_name: Dict[str, str]
) -> Dict[str, int]:
    """
    Returns number of launches per launch site.
    """
    count = defaultdict(int)

    for launch in launches:
        site_name = launch.launchpad.name
        count[site_name] += 1

    return dict(count)


def get_launch_frequency_by_month(launches: List[LaunchModel]) -> Dict[str, int]:
    """
    Returns monthly launch frequency in YYYY-MM format.
    """
    count = defaultdict(int)

    for launch in launches:
        key = launch.date_utc.strftime("%Y-%m")
        count[key] += 1

    return dict(sorted(count.items()))


def get_launch_frequency_by_year(launches: List[LaunchModel]) -> Dict[str, int]:
    """
    Returns yearly launch frequency in YYYY format.
    """
    count = defaultdict(int)

    for launch in launches:
        year = str(launch.date_utc.year)
        count[year] += 1

    return dict(sorted(count.items()))
