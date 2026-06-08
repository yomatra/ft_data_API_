from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, ConfigDict, Field


API_DESCRIPTION = """
REST API with dummy conveyor-belt inspection results.

This standalone version is meant for local integration testing. It has no
database connection and no dependency on the main project package.
"""

OPENAPI_TAGS = [
    {
        "name": "system",
        "description": "Operational endpoints for checking API availability.",
    },
    {
        "name": "parts",
        "description": "Inspection records for parts moving through the conveyor.",
    },
    {
        "name": "pictures",
        "description": "Captured image references for inspected parts.",
    },
    {
        "name": "groups",
        "description": "Part grouping labels used by the inspection workflow.",
    },
    {
        "name": "inspection",
        "description": "Damage inspection results for individual parts.",
    },
]


class HealthResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "status": "ok",
                    "timestamp": "2026-05-31T18:30:00Z",
                }
            ]
        }
    )

    status: str = Field(description="Current API health status.")
    timestamp: datetime = Field(description="Server time when the health check was generated.")


class Part(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa1",
                    "picture": "base_64_picture",
                    "group": "example_group",
                    "is_damaged": False,
                    "timestamp": "2026-05-31T08:00:03Z",
                }
            ]
        }
    )

    id: UUID = Field(description="Unique identifier for the inspected part.")
    picture: str = Field(description="Base64-encoded image data for the captured part.")
    group: str = Field(description="Inspection group assigned to the part.")
    is_damaged: bool = Field(description="Whether damage was detected on the part.")
    timestamp: datetime = Field(description="Time when this inspection result was produced.")


PART_1_ID = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa1")
PART_2_ID = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa2")
PART_3_ID = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa3")

DUMMY_PARTS: list[Part] = [
    Part(
        id=PART_1_ID,
        picture="base_64_picture",
        group="example_group",
        is_damaged=False,
        timestamp=datetime(2026, 5, 31, 8, 0, 3, tzinfo=timezone.utc),
    ),
    Part(
        id=PART_2_ID,
        picture="base_64_picture",
        group="example_group",
        is_damaged=False,
        timestamp=datetime(2026, 5, 31, 8, 1, 3, tzinfo=timezone.utc),
    ),
    Part(
        id=PART_3_ID,
        picture="base_64_picture",
        group="example_group",
        is_damaged=False,
        timestamp=datetime(2026, 5, 31, 8, 2, 3, tzinfo=timezone.utc),
    ),
]

app = FastAPI(
    title="Conveyor Belt Inspection Dummy API",
    summary="Standalone dummy API with part image, group, and damage data.",
    description=API_DESCRIPTION,
    version="0.1.0",
    openapi_tags=OPENAPI_TAGS,
)


def get_part_or_404(part_id: UUID) -> Part:
    for part in DUMMY_PARTS:
        if part.id == part_id:
            return part
    raise HTTPException(status_code=404, detail="Part inspection not found")


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["system"],
    summary="Check API health",
    response_description="The current service health status.",
)
def health() -> HealthResponse:
    return HealthResponse(status="ok", timestamp=datetime.now(timezone.utc))


@app.get(
    "/current_parts",
    response_model=Part,
    tags=["parts"],
    summary="Get the current part",
    response_description="The part currently available in the dummy inspection stream.",
)
def get_current_part() -> Part:
    return DUMMY_PARTS[0]


@app.get(
    "/parts/last",
    response_model=list[Part],
    tags=["parts"],
    summary="List recent parts",
    response_description="Recent part inspections ordered newest first.",
)
def get_last_parts(
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=100,
            description="Maximum number of latest part inspections to return.",
        ),
    ] = 10,
) -> list[Part]:
    return sorted(DUMMY_PARTS, key=lambda part: part.timestamp, reverse=True)[:limit]


@app.get(
    "/parts/{part_id}",
    response_model=Part,
    tags=["parts"],
    summary="Get a part by ID",
    response_description="The matching part inspection.",
    responses={404: {"description": "Part inspection not found."}},
)
def get_part(part_id: UUID) -> Part:
    return get_part_or_404(part_id)


@app.get(
    "/pictures",
    response_model=list[str],
    tags=["pictures"],
    summary="List recent pictures",
    response_description="Base64 image values for recent part inspections ordered newest first.",
)
def list_pictures(
    limit: Annotated[
        int,
        Query(
            ge=1,
            le=100,
            description="Maximum number of latest part pictures to return.",
        ),
    ] = 10,
) -> list[str]:
    latest_parts = sorted(DUMMY_PARTS, key=lambda part: part.timestamp, reverse=True)
    return [part.picture for part in latest_parts[:limit]]


@app.get(
    "/parts/{part_id}/picture",
    response_model=str,
    tags=["pictures"],
    summary="Get a part picture",
    response_description="Base64 image value for the requested part.",
    responses={404: {"description": "Part inspection not found."}},
)
def get_picture(part_id: UUID) -> str:
    return get_part_or_404(part_id).picture


@app.get(
    "/groups",
    response_model=list[str],
    tags=["groups"],
    summary="List part groups",
    response_description="Unique group labels across all dummy part inspections.",
)
def list_groups() -> list[str]:
    return sorted({part.group for part in DUMMY_PARTS})


@app.get(
    "/parts/{part_id}/group",
    response_model=str,
    tags=["groups"],
    summary="Get the group for a part",
    response_description="Group label for the requested part.",
    responses={404: {"description": "Part inspection not found."}},
)
def get_group(part_id: UUID) -> str:
    return get_part_or_404(part_id).group


@app.get(
    "/parts/{part_id}/state",
    response_model=bool,
    tags=["inspection"],
    summary="Get part damage state",
    response_description="Whether damage was detected on the requested part.",
    responses={404: {"description": "Part inspection not found."}},
)
def get_state(part_id: UUID) -> bool:
    return get_part_or_404(part_id).is_damaged
