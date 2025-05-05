from unittest.mock import MagicMock, patch

import pytest

from app.api_client import SpaceXClient
from app.cache import SQLiteCache


@pytest.fixture
def mock_launch_data():
    return [
        {
            "id": "abc",
            "name": "Test Launch",
            "date_utc": "2023-01-01T00:00:00Z",
            "success": True,
            "upcoming": False,
            "rocket": "rocket_123",
            "launchpad": "pad_456",
            "flight_number": 42,
            "details": "Test",
            "webcast": None,
            "links": {},
        }
    ]


def test_get_launches_success(mock_launch_data):
    with patch("app.api_client.httpx.Client.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = mock_launch_data

        mock_cache = MagicMock(spec=SQLiteCache)
        mock_cache.is_valid.return_value = False
        mock_cache.write = MagicMock()

        client = SpaceXClient(
            launch_cache=mock_cache,
            rocket_cache=MagicMock(spec=SQLiteCache),
            launchpad_cache=MagicMock(spec=SQLiteCache),
        )
        result = client.get_launches()

        assert isinstance(result, list)
        assert result[0]["id"] == "abc"


def test_get_launches_fallback_to_cache(mock_launch_data):
    fake_cache = MagicMock(spec=SQLiteCache)
    fake_cache.is_valid.return_value = True
    fake_cache.load.return_value = mock_launch_data

    with patch("app.api_client.httpx.Client.get", side_effect=Exception("API down")):
        client = SpaceXClient(
            launch_cache=fake_cache,
            rocket_cache=MagicMock(spec=SQLiteCache),
            launchpad_cache=MagicMock(spec=SQLiteCache),
        )
        launches = client.get_launches()

    assert len(launches) == 1
    assert launches[0]["name"] == "Test Launch"
    fake_cache.load.assert_called_once()


def test_get_rockets_success():
    rocket_data = [{"id": "r1", "name": "Falcon 9"}]

    rocket_cache = MagicMock(spec=SQLiteCache)
    rocket_cache.is_valid.return_value = True
    rocket_cache.load.return_value = rocket_data

    client = SpaceXClient(
        launch_cache=MagicMock(spec=SQLiteCache),
        rocket_cache=rocket_cache,
        launchpad_cache=MagicMock(spec=SQLiteCache),
    )

    rockets = client.get_rockets()
    assert rockets[0]["name"] == "Falcon 9"


def test_get_launchpads_success():
    pad_data = [{"id": "p1", "name": "Starbase"}]

    launchpad_cache = MagicMock(spec=SQLiteCache)
    launchpad_cache.is_valid.return_value = True
    launchpad_cache.load.return_value = pad_data

    client = SpaceXClient(
        launch_cache=MagicMock(spec=SQLiteCache),
        rocket_cache=MagicMock(spec=SQLiteCache),
        launchpad_cache=launchpad_cache,
    )

    pads = client.get_launchpads()
    assert pads[0]["name"] == "Starbase"
