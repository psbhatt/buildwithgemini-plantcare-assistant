import math
from typing import Any, Dict

def calculate_watering_schedule(
    species: str,
    pot_diameter_inches: float,
    pot_type: str = "plastic",
    season: str = "spring"
) -> Dict[str, Any]:
    """Calculate customized watering interval and recommended water volume based on plant species, pot size, material, and season.

    Args:
        species: Plant species name (e.g., 'Monstera Deliciosa', 'Snake Plant', 'Fiddle Leaf Fig').
        pot_diameter_inches: Diameter of the pot in inches (e.g. 4.0, 6.0, 10.0).
        pot_type: Type of pot material ('terracotta', 'plastic', 'glazed ceramic'). Defaults to 'plastic'.
        season: Current season ('spring', 'summer', 'fall', 'winter'). Defaults to 'spring'.

    Returns:
        A dictionary with calculated watering interval in days, recommended water volume in mL, and care notes.
    """
    spec = species.lower()

    # Base watering days by plant type
    if "snake" in spec or "sansevieria" in spec or "succulent" in spec or "cactus" in spec:
        base_days = 18.0
    elif "pothos" in spec or "philodendron" in spec:
        base_days = 7.0
    elif "monstera" in spec:
        base_days = 7.0
    elif "fig" in spec or "ficus" in spec:
        base_days = 9.0
    elif "fern" in spec or "calathea" in spec:
        base_days = 4.0
    else:
        base_days = 7.0

    # Pot size factor (larger pots retain moisture longer)
    # 6-inch is reference baseline (factor = 1.0)
    size_factor = max(0.6, math.sqrt(pot_diameter_inches / 6.0))

    # Pot material factor (terracotta evaporates quickly; plastic/glazed retains)
    material_multiplier = 0.75 if pot_type.lower() == "terracotta" else 1.0

    # Seasonal evaporation factor
    season_multipliers = {
        "summer": 0.8,
        "spring": 1.0,
        "fall": 1.2,
        "winter": 1.5,
    }
    season_factor = season_multipliers.get(season.lower(), 1.0)

    # Compute final interval in days
    interval_days = round(base_days * size_factor * material_multiplier * season_factor)
    interval_days = max(2, interval_days)

    # Recommended water volume estimate (approx 20-25% of pot volume in mL)
    radius_cm = (pot_diameter_inches * 2.54) / 2.0
    height_cm = pot_diameter_inches * 2.54 * 0.95
    pot_volume_ml = math.pi * (radius_cm ** 2) * height_cm
    water_volume_ml = round(pot_volume_ml * 0.22)

    return {
        "species": species,
        "pot_diameter_inches": pot_diameter_inches,
        "pot_type": pot_type,
        "season": season,
        "recommended_interval_days": interval_days,
        "recommended_water_volume_ml": water_volume_ml,
        "guidance": (
            f"Water approximately {water_volume_ml} mL every {interval_days} days. "
            f"Always check that the top soil is dry before watering."
        )
    }
