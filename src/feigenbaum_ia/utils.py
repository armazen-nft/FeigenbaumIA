from __future__ import annotations


def estimate_water_usage(kwh: float, liters_per_kwh: float = 0.7) -> float:
    """Estimate datacenter water usage in liters from energy consumption."""
    return kwh * liters_per_kwh
