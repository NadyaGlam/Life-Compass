from fastapi import APIRouter, HTTPException
from app.schemas.profile import ProfileRequest, LifeCompassResponse
from app.services.places import find_coordinates
from app.services.timezones import timezone_name_from_coords, to_utc_birth_moment
from app.services.astro_calc import calc_nodes
from app.services.destiny_profile import DestinyProfileService, NodePlacement


router = APIRouter(prefix="/profile", tags=["life-compass"])

@router.post("", response_model=LifeCompassResponse)
def build_profile(payload: ProfileRequest) -> LifeCompassResponse:
    try:
        coords = find_coordinates(payload.birth_place)
        tz_name = timezone_name_from_coords(lat=coords.lat, lon=coords.lon)

        moment = to_utc_birth_moment(
            birth_date=payload.birth_date,
            birth_time=payload.birth_time,
            tz_name=tz_name,
        )
        nodes = calc_nodes(utc_dt=moment.utc_dt, lat=coords.lat, lon=coords.lon)

        south = nodes["south"]
        north = nodes["north"]

        service = DestinyProfileService()
        result = service.build(
            south=NodePlacement(sign=south["sign"], house=int(south["house"])),
            north=NodePlacement(sign=north["sign"], house=int(north["house"])),
        )

        return LifeCompassResponse(**result)


    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))