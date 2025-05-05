from datetime import datetime, timezone
from typing import Any, Dict, List

from app.models import LaunchModel, LaunchpadModel, RocketModel


def parse_date(date_str: str) -> datetime:
    try:
        dt = datetime.fromisoformat(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        raise ValueError(f"Invalid ISO date string: {date_str}")


def enrich_launches(
    raw_launches: List[Dict[str, Any]],
    rocket_map: Dict[str, str],
    launchpad_map: Dict[str, str],
) -> List[LaunchModel]:
    enriched = []

    for launch in raw_launches:
        rocket_id = launch.get("rocket")
        launchpad_id = launch.get("launchpad")

        launch["rocket"] = RocketModel(
            id=rocket_id, name=rocket_map.get(rocket_id, "Unknown")
        )
        launch["launchpad"] = LaunchpadModel(
            id=launchpad_id, name=launchpad_map.get(launchpad_id, "Unknown")
        )

        enriched.append(LaunchModel(**launch))

    return enriched
