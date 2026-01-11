from __future__ import annotations

from statistics import mean


def compute_severity(values: list[int], fallback: int = 0) -> int:
    if not values:
        return fallback
    avg = round(mean(values))
    return max(0, min(100, avg))