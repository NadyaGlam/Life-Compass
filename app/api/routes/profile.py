from fastapi import APIRouter, HTTPException
from app.logger import logger
from app.core import LifeCompassService
from app.schemas.profile import ProfileRequest, LifeCompassResponse
from app.services.places import find_coordinates
from app.services.timezones import timezone_name_from_coords

router = APIRouter(prefix="/profile", tags=["life-compass"])

service = LifeCompassService()

@router.post("", response_model=LifeCompassResponse)
def build_profile(payload: ProfileRequest) -> LifeCompassResponse:
    try:
        result = service.build_profile(
            birth_date=payload.birth_date,
            birth_time=payload.birth_time,
            birth_place=payload.birth_place,
        )
        return LifeCompassResponse(**result)
    except ValueError as e:
        logger.warning(f"Validation error in /profile: {e}")
        raise HTTPException(status_code=422, detail=str(e))

    except Exception as e:
        logger.error(f"Unexpected error in /profile: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/place")
def resolve_place(q: str):

    try:
        coords = find_coordinates(q)
        tz_name = timezone_name_from_coords(lat=coords.lat, lon=coords.lon)

        logger.info(f"Place resolved: q='{q}' -> lat={coords.lat}, lon={coords.lon}, tz={tz_name}")

        return {"query": q, "lat": coords.lat, "lon": coords.lon, "timezone": tz_name}

    except ValueError as e:
        logger.warning(f"Place not found: q='{q}'. Error: {e}")
        raise HTTPException(status_code=404, detail=str(e))

    except Exception as e:
        logger.error(f"Unexpected error in /profile/place: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")