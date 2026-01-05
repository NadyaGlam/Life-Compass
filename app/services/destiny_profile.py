from dataclasses import dataclass
from app.services.nodes_text import HOUSE_THEMES, SIGN_AXES

def ordinal(n: int) -> str:
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


@dataclass(frozen=True)
class NodePlacement:
    sign: str
    house: int

class DestinyProfileService:
    """
    Builds the final purpose-oriented narrative from:
    - South Node sign + house
    - North Node sign + house
    Using deterministic text blocks (no magic, no randomness).
    """

    def build(self, south: NodePlacement, north: NodePlacement) -> dict:
        # 1) Fetch sign axis themes using NORTH sign as key
        axis = SIGN_AXES.get(north.sign)
        if not axis:
            raise ValueError(f"Unsupported north node sign: {north.sign}")
        # 2) Fetch house themes

        sn_house = HOUSE_THEMES.get(south.house)
        nn_house = HOUSE_THEMES.get(north.house)
        if not sn_house or not nn_house:
            raise ValueError(f"Unsupported house: SN={south.house} NN={north.house}")

        title = (
            f"{south.sign} South Node ({ordinal(south.house)} House) → "
            f"{north.sign} North Node ({ordinal(north.house)} House)"
        )
        # 3) Compose sections
        sections = [
            {
                "context": f"☋ South {axis['south_title']}",
                "meaning": axis["south"],
            },
            {
                "context": f"☋ South Node in the {ordinal(south.house)} House — familiar life scenario",
                "meaning": sn_house["sn"],
                "direction": sn_house["key"],
            },
            {
                "context": f"☊ {axis['north_title']}",
                "meaning": axis["north"],
            },
            {
                "context": f"☊ North Node in the {ordinal(north.house)} House — where growth happens",
                "meaning": nn_house["nn"],
                "direction": nn_house["key"],
            },
        ]
        # 4) Recommendations: deterministic mix of sign+house
        recommendations = [
            f"Consciously develop: {axis['north']}",
            f"Let growth unfold through: {nn_house['title']}",
            f"Notice when you fall back into: {sn_house['title']}",
            f"Keep the core transition in mind: {axis['bridge']}",
        ]
        motto = axis.get("motto", "Shift the center of gravity toward growth.")
        return {
            "title": title,
            "bridge": axis["bridge"],
            "sections": sections,
            "recommendations": recommendations,
            "motto": motto,
        }