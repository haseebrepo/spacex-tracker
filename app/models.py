from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class RocketModel(BaseModel):
    id: str
    name: str
    type: Optional[str] = None
    description: Optional[str] = None
    active: Optional[bool] = None
    stages: Optional[int] = None
    boosters: Optional[int] = None
    cost_per_launch: Optional[int] = Field(None, alias="cost_per_launch")


class LaunchpadModel(BaseModel):
    id: str
    name: str
    locality: Optional[str] = None
    region: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    launch_attempts: Optional[int] = None
    launch_successes: Optional[int] = None


class LaunchModel(BaseModel):
    id: str
    name: str
    date_utc: datetime
    success: Optional[bool]
    upcoming: bool
    rocket: RocketModel
    launchpad: LaunchpadModel
    flight_number: Optional[int]
    details: Optional[str]
    webcast: Optional[HttpUrl] = None
    links: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)
