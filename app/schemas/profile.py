from __future__ import annotations
from datetime import date, time
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class ProfileRequest(BaseModel):
    birth_date: date = Field(..., description="Date of birth (YYYY-MM-DD)")
    birth_time: time = Field(..., description="Time of birth (HH:MM)")
    birth_place: str = Field(..., min_length=2, description="Place of birth (must exist in places.json)")

    @field_validator("birth_date")
    @classmethod
    def validate_birth_date(cls, v: date) -> date:
        from datetime import date as d
        if v > d.today():
            raise ValueError("Date can't be from the future")
        if v < d(1900, 1, 1):
            raise ValueError("Too old date (min 1900-01-01)")
        return v

class Section(BaseModel):
    context: str
    meaning: str
    direction: Optional[str] = None

class LifeCompassResponse(BaseModel):
    title: str
    bridge: str
    sections: List[Section]
    recommendations: List[str]
    motto: str
