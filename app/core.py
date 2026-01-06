from app.logger import logger
from app.services.places import find_coordinates
from app.services.timezones import timezone_name_from_coords, to_utc_birth_moment
from app.services.astro_calc import calc_nodes
from app.services.destiny_profile import DestinyProfileService, NodePlacement
from datetime import date,time

class LifeCompassService:

    def __init__(self) -> None:
        self._destiny = DestinyProfileService()
        logger.info("LifeCompassService initialized")

    def build_profile(self, birth_date: date, birth_time: time, birth_place: str) -> dict:
        logger.info(f"Start build_profile: place='{birth_place}'")

        coords = find_coordinates(birth_place)
        logger.info(f"Coordinates found: lat={coords.lat}, lon={coords.lon}")

        tz_name = timezone_name_from_coords(lat=coords.lat, lon=coords.lon)
        logger.info(f"Timezone resolved: {tz_name}")

        moment = to_utc_birth_moment(
            birth_date=birth_date,
            birth_time=birth_time,
            tz_name=tz_name,
        )

        logger.info(f"Birth moment (UTC): {moment.utc_dt}")

        nodes = calc_nodes(utc_dt=moment.utc_dt, lat=coords.lat, lon=coords.lon)
        south = nodes["south"]
        north = nodes["north"]

        result = self._destiny.build(
            south=NodePlacement(sign=south["sign"], house=int(south["house"])),
            north=NodePlacement(sign=north["sign"], house=int(north["house"])),
        )

        logger.info("Profile built successfully")
        return result
