from __future__ import annotations
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Coordinates:
    lat: float
    lon: float
_PLACES_PATH = Path(__file__).resolve().parents[2] / "data" / "places.json"

def find_coordinates(place: str) -> Coordinates:
    if not _PLACES_PATH.exists():
        raise ValueError("places.json not found")
    data = json.loads(_PLACES_PATH.read_text(encoding="utf-8"))
    if place not in data:
        raise ValueError("Unknown birth_place. Must match a key from places.json exactly.")
    item = data[place]
    return Coordinates(lat=float(item["lat"]), lon=float(item["lon"]))