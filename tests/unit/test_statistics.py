from datetime import datetime

import pytest

from app.models import LaunchModel, LaunchpadModel, RocketModel
from app.statistics import (
    compute_success_rates_by_rocket,
    count_launches_per_site,
    get_launch_frequency_by_month,
    get_launch_frequency_by_year,
)


@pytest.fixture
def sample_launches():
    return [
        LaunchModel(
            id="l1",
            name="Mission Alpha",
            date_utc=datetime(2021, 1, 10),
            success=True,
            upcoming=False,
            rocket=RocketModel(id="r1", name="Falcon 9"),
            launchpad=LaunchpadModel(id="p1", name="CCSFS SLC 40"),
            flight_number=1,
            details=None,
            webcast=None,
            links={},
        ),
        LaunchModel(
            id="l2",
            name="Mission Beta",
            date_utc=datetime(2021, 1, 15),
            success=False,
            upcoming=False,
            rocket=RocketModel(id="r1", name="Falcon 9"),
            launchpad=LaunchpadModel(id="p1", name="CCSFS SLC 40"),
            flight_number=2,
            details=None,
            webcast=None,
            links={},
        ),
        LaunchModel(
            id="l3",
            name="Mission Gamma",
            date_utc=datetime(2022, 5, 20),
            success=True,
            upcoming=False,
            rocket=RocketModel(id="r2", name="Starship"),
            launchpad=LaunchpadModel(id="p2", name="Starbase"),
            flight_number=3,
            details=None,
            webcast=None,
            links={},
        ),
    ]


def test_compute_success_rates_by_rocket(sample_launches):
    rocket_map = {"r1": "Falcon 9", "r2": "Starship"}
    rates = compute_success_rates_by_rocket(sample_launches, rocket_map)
    assert rates["Falcon 9"] == 50.0
    assert rates["Starship"] == 100.0


def test_count_launches_per_site(sample_launches):
    launchpad_map = {"p1": "CCSFS SLC 40", "p2": "Starbase"}
    counts = count_launches_per_site(sample_launches, launchpad_map)
    assert counts["CCSFS SLC 40"] == 2
    assert counts["Starbase"] == 1


def test_get_launch_frequency_by_month(sample_launches):
    freq = get_launch_frequency_by_month(sample_launches)
    assert freq["2021-01"] == 2
    assert freq["2022-05"] == 1


def test_get_launch_frequency_by_year(sample_launches):
    freq = get_launch_frequency_by_year(sample_launches)
    assert freq["2021"] == 2
    assert freq["2022"] == 1
