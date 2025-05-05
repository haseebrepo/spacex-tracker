import csv
import json
from io import StringIO
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse, StreamingResponse

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


@router.get("/", summary="Export launch data as CSV or JSON")
def export_launches(
    format: str = Query(
        ..., pattern="^(csv|json)$", description="Export format: csv or json"
    ),
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    success: Optional[bool] = None,
    rocket_name: Optional[str] = None,
    launchpad_name: Optional[str] = None,
    launches: list[LaunchModel] = Depends(get_parsed_launches),
    rocket_map: dict = Depends(get_rocket_id_to_name_map),
    launchpad_map: dict = Depends(get_launchpad_id_to_name_map),
):
    """
    Export filtered launch data in CSV or JSON format.
    """
    # Apply filters
    filtered = filter_by_date_range(launches, start_date, end_date)
    filtered = filter_by_success(filtered, success)
    filtered = filter_by_rocket_name(filtered, {}, rocket_name)
    filtered = filter_by_launchpad(filtered, {}, launchpad_name)

    if format == "json":
        return JSONResponse(
            content=[json.loads(launch.model_dump_json()) for launch in filtered]
        )

    elif format == "csv":
        return stream_csv(filtered)

    raise HTTPException(status_code=400, detail="Unsupported export format")


def stream_csv(launches: list[LaunchModel]) -> StreamingResponse:
    def generate():
        buffer = StringIO()
        writer = csv.writer(buffer)

        header = [
            "id",
            "name",
            "date_utc",
            "success",
            "rocket_name",
            "launchpad_name",
            "flight_number",
        ]
        writer.writerow(header)
        yield buffer.getvalue()
        buffer.seek(0)
        buffer.truncate(0)

        for launch in launches:
            writer.writerow(
                [
                    launch.id,
                    launch.name,
                    launch.date_utc.isoformat(),
                    launch.success,
                    launch.rocket.name,
                    launch.launchpad.name,
                    launch.flight_number,
                ]
            )
            yield buffer.getvalue()
            buffer.seek(0)
            buffer.truncate(0)

    return StreamingResponse(
        generate(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=launches.csv"},
    )
