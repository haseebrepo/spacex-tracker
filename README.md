# SpaceX Tracker

A production-grade FastAPI application that tracks and analyzes historical SpaceX launch data. Built for performance, maintainability, and clarity, it follows best practices in architecture, testing, and Dockerization.

---

### 📽 Demo

[Click to watch demo video on Google Drive](https://shorturl.at/eEeth)

---

## Project Overview

**Goal:** Build a RESTful API using Python and FastAPI to serve filtered and processed launch data from the SpaceX API. The application supports:

* Efficient **data caching** with expiration
* Filtering of launches via query parameters
* Multiple **statistical summaries** and **data export** formats
* Complete **test suite** with `pytest`
* Fully **dockerized environment** for dev and test

---

## Tech Stack

* **FastAPI**: Web framework
* **httpx**: HTTP client
* **SQLite**: Lightweight cache storage
* **Docker**: Containerization
* **Pytest**: Testing framework

---

## Key Features

### Launch Endpoints

* `GET /launches/` - Filterable list of launches

### Statistics

* `GET /stats/success-rate` - Success rate per rocket
* `GET /stats/launchpad-counts` - Launches per launchpad
* `GET /stats/monthly-frequency` - Launches per month
* `GET /stats/yearly-frequency` - Launches per year

### Export

* `GET /export/?format=json|csv` - Export launch data

### Filtering Options (for `/launches/`)

* `success=true|false`
* `rocket_name=Falcon 9`
* `launchpad_name=Starbase`
* `date_from`, `date_to` (ISO format)

---

## Project Structure

```
spacex-tracker/
├── app/
│   ├── api_client.py         # API integration & cache logic
│   ├── cache.py              # SQLite-based cache interface
│   └── settings.py           # Environment settings
├── webapp/
│   ├── routes/               # All API routes
│   ├── main.py               # FastAPI app
│   └── dependencies.py       # Dependency injection logic
├── tests/                    # Unit, integration, API tests
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/spacex-tracker.git
cd spacex-tracker
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env`

```env
SPACEX_API_BASE=https://api.spacexdata.com/v4
CACHE_TTL_HOURS=6
CACHE_DB_PATH=cache/launch_cache.db
```

---

## Run the Server

### Local

```bash
uvicorn webapp.main:app --reload
```

### Docker

```bash
docker compose up --build
```

Access the API at: `http://localhost:8000`

Docs:

* Swagger UI: `http://localhost:8000/docs`
* ReDoc: `http://localhost:8000/redoc`

---

## Testing

### Run All Tests Locally

```bash
pytest
```

### Run Tests in Docker

```bash
docker compose run --rm test
```

Test Coverage:

* Launch filters and response correctness
* Cache behavior (fresh and fallback)
* Statistics generation
* API-level integration tests

---

## Caching

Caching is handled using **SQLite**, stored in `cache/launch_cache.db`, with separate tables for:

* `launches`
* `rockets`
* `launchpads`

Cache expires after the TTL set in the `.env` file (`CACHE_TTL_HOURS`).

---

## Development Practices

* Follows clean architecture: separation of API, data, and services
* Uses dependency injection for testability
* Imports auto-sorted with `isort`
* Code formatted with `black`
* Fully type-annotated and linted


---

## Author

Built with care by \[Haseeb Khalid]
