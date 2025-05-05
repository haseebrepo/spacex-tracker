import logging
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.models import LaunchModel, LaunchpadModel, RocketModel
from webapp.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_launches():
    return [
        LaunchModel(
            id="launch_1",
            name="Test Launch A",
            date_utc="2021-01-01T00:00:00Z",
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
            id="launch_2",
            name="Test Launch B",
            date_utc="2021-01-15T00:00:00Z",
            success=False,
            upcoming=False,
            rocket=RocketModel(id="r1", name="Falcon 9"),
            launchpad=LaunchpadModel(id="p1", name="CCSFS SLC 40"),
            flight_number=2,
            details=None,
            webcast=None,
            links={},
        ),
    ]


@patch("webapp.dependencies.get_parsed_launches")
@patch("webapp.dependencies.get_rocket_id_to_name_map")
def test_success_rate(mock_map, mock_data, client, mock_launches):
    mock_data.return_value = mock_launches
    mock_map.return_value = {"r1": "Falcon 9"}
    logging.error("Mocked data: %s", mock_data.return_value)
    logging.error("Mocked rocket map: %s", mock_map.return_value)

    response = client.get("/stats/success-rate")
    assert response.status_code == 200


@patch("webapp.dependencies.get_parsed_launches")
@patch("webapp.dependencies.get_launchpad_id_to_name_map")
def test_launchpad_counts(mock_map, mock_data, client, mock_launches):
    mock_data.return_value = mock_launches
    mock_map.return_value = {"p1": "CCSFS SLC 40"}

    response = client.get("/stats/launchpads")
    assert response.status_code == 200


@patch("webapp.dependencies.get_parsed_launches")
def test_monthly_frequency(mock_data, client, mock_launches):
    mock_data.return_value = mock_launches
    response = client.get("/stats/monthly")
    assert response.status_code == 200


@patch("webapp.dependencies.get_parsed_launches")
def test_yearly_frequency(mock_data, client, mock_launches):
    mock_data.return_value = mock_launches
    response = client.get("/stats/yearly")
    assert response.status_code == 200
