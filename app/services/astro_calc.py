from __future__ import annotations
from datetime import datetime
import swisseph as swe

SIGNS = [
    "Aries", "Taurus", "Gemini", "Cancer",
    "Leo", "Virgo", "Libra", "Scorpio",
    "Sagittarius", "Capricorn", "Aquarius", "Pisces"
]
def _sign_from_lon(lon: float) -> str:
    idx = int((lon % 360.0) // 30)
    return SIGNS[idx % 12]
def _julian_day_utc(dt_utc: datetime) -> float:
    y, m, d = dt_utc.year, dt_utc.month, dt_utc.day
    hour = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0
    return swe.julday(y, m, d, hour, swe.GREG_CAL)
def _planet_lon_ut(jd_ut: float, planet: int) -> float:
    pos, _ = swe.calc_ut(jd_ut, planet, swe.FLG_SWIEPH)
    return float(pos[0]) % 360.0
def _normalize_cusps(cusps_raw) -> list[float]:

    if len(cusps_raw) == 13:
        return [float(cusps_raw[i]) for i in range(1, 13)]
    if len(cusps_raw) == 12:
        return [float(c) for c in cusps_raw]
    raise RuntimeError(f"Unexpected cusps length from swe.houses_ex: {len(cusps_raw)}")
def _house_index_from_lon(lon: float, cusps: list[float]) -> int:
    lon = lon % 360.0
    cusps = [(c % 360.0) for c in cusps]
    for i in range(12):
        start = cusps[i]
        end = cusps[(i + 1) % 12]
        if start <= end:
            if start <= lon < end:
                return i + 1
        else:
            if lon >= start or lon < end:
                return i + 1
    return 1
def calc_nodes(*, utc_dt: datetime, lat: float, lon: float, house_system: bytes = b'P') -> dict:
    """
    Returns North Node & South Node: sign + house.
    North Node is computed via Swiss Ephemeris (Mean Node).
    South Node is opposite longitude and opposite house axis.
    """
    jd = _julian_day_utc(utc_dt)
    # Node longitude (Mean Node)
    nn_lon = _planet_lon_ut(jd, swe.MEAN_NODE)
    nn_sign = _sign_from_lon(nn_lon)
    # Houses
    cusps_raw, _ = swe.houses_ex(jd, lat, lon, house_system, swe.FLG_SWIEPH)
    cusps = _normalize_cusps(cusps_raw)
    nn_house = _house_index_from_lon(nn_lon, cusps)
    # South Node = opposite point
    sn_lon = (nn_lon + 180.0) % 360.0
    sn_sign = _sign_from_lon(sn_lon)

    sn_house = ((nn_house + 5) % 12) + 1
    return {
        "north": {"lon": nn_lon, "sign": nn_sign, "house": nn_house},
        "south": {"lon": sn_lon, "sign": sn_sign, "house": sn_house},
    }