from datetime import datetime, timezone

import pytest

from app.filters import (
    filter_by_date_range,
    filter_by_launchpad,
    filter_by_rocket_name,
    filter_by_success,
)
from app.models import LaunchModel, LaunchpadModel, RocketModel


@pytest.fixture
def sample_launches():
    return [
        LaunchModel(
            id="1",
            name="Mission Alpha",
            date_utc=datetime(2022, 1, 15).replace(tzinfo=timezone.utc),
            success=True,
            upcoming=False,
            rocket=RocketModel(id="r1", name="Falcon 9"),
            launchpad=LaunchpadModel(id="p1", name="CCSFS SLC 40"),
            flight_number=101,
            details=None,
            webcast=None,
            links={},
        ),
        LaunchModel(
            id="2",
            name="Mission Beta",
            date_utc=datetime(2021, 7, 10).replace(tzinfo=timezone.utc),
            success=False,
            upcoming=False,
            rocket=RocketModel(id="r2", name="Starship"),
            launchpad=LaunchpadModel(id="p2", name="Starbase"),
            flight_number=102,
            details=None,
            webcast=None,
            links={},
        ),
    ]


def test_filter_by_date_range(sample_launches):
    filtered = filter_by_date_range(sample_launches, "2022-01-01", "2022-12-31")
    assert len(filtered) == 1
    assert filtered[0].name == "Mission Alpha"


def test_filter_by_success_true(sample_launches):
    filtered = filter_by_success(sample_launches, True)
    assert len(filtered) == 1
    assert filtered[0].success is True


def test_filter_by_success_false(sample_launches):
    filtered = filter_by_success(sample_launches, False)
    assert len(filtered) == 1
    assert filtered[0].success is False


def test_filter_by_rocket_name_exact_match(sample_launches):
    filtered = filter_by_rocket_name(sample_launches, {}, "Falcon 9")
    assert len(filtered) == 1
    assert filtered[0].rocket.name == "Falcon 9"


def test_filter_by_rocket_name_case_insensitive(sample_launches):
    filtered = filter_by_rocket_name(sample_launches, {}, "falcon 9")
    assert len(filtered) == 1
    assert filtered[0].rocket.name.lower() == "falcon 9"


def test_filter_by_launchpad_name(sample_launches):
    filtered = filter_by_launchpad(sample_launches, {}, "Starbase")
    assert len(filtered) == 1
    assert filtered[0].launchpad.name == "Starbase"
