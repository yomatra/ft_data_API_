# Standalone Conveyor Belt Inspection Dummy API

This is a small one-file API for local integration testing. It contains only
the dummy routes and dummy data, without database code or the main project
package.

## Run

```bash
pip install -r requirements.txt
uvicorn dummy_api:app --reload
```

Open:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- OpenAPI JSON: http://localhost:8000/openapi.json
- Health: http://localhost:8000/health

## Routes

- `GET /health`
- `GET /current_part`
- `GET /parts/last?limit=10`
- `GET /parts/since?timestamp=2026-05-31T08:01:03Z`
- `GET /parts/{part_id}`
- `GET /pictures?limit=10`
- `GET /parts/{part_id}/picture`
- `GET /groups`
- `GET /parts/{part_id}/group`
- `GET /parts/{part_id}/state`
