from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from webapp.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_launches():
    return [
        {
            "id": "launch_1",
            "name": "Test Launch A",
            "date_utc": "2022-01-10T00:00:00Z",
            "success": True,
            "upcoming": False,
            "rocket": {"id": "r1", "name": "Falcon 9"},
            "launchpad": {"id": "p1", "name": "CCSFS SLC 40"},
            "flight_number": 101,
            "details": None,
            "webcast": None,
            "links": {},
        },
        {
            "id": "launch_2",
            "name": "Test Launch B",
            "date_utc": "2021-05-20T00:00:00Z",
            "success": False,
            "upcoming": False,
            "rocket": {"id": "r2", "name": "Starship"},
            "launchpad": {"id": "p2", "name": "Starbase"},
            "flight_number": 102,
            "details": None,
            "webcast": None,
            "links": {},
        },
    ]


@patch("webapp.dependencies.get_parsed_launches")
def test_launches_basic_filtering(mock_data, client, mock_launches):
    mock_data.return_value = mock_launches

    response = client.get("/launches?rocket_name=Falcon 9&success=true")
    assert response.status_code == 200
    data = response.json()
    assert len(data) != 0
    assert data[0]["rocket"]["name"] == "Falcon 9"
    assert data[0]["success"] is True
