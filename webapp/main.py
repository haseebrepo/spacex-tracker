from fastapi import FastAPI

from webapp.routes import export, launches, statistics

app = FastAPI(
    title="SpaceX Launch Tracker API",
    version="1.0.0",
    description="Track and analyze SpaceX launches using the SpaceX API.",
)

# Register routes
app.include_router(launches.router, prefix="/launches", tags=["Launches"])
app.include_router(statistics.router, prefix="/stats", tags=["Statistics"])
app.include_router(export.router, prefix="/export", tags=["Export"])
