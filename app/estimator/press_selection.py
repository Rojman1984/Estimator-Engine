"""Press recommendation logic for supported POC jobs."""

from __future__ import annotations


def suggest_press(total_colors: int, laminated: bool, total_dies: int) -> tuple[str | None, list[str]]:
    flags: list[str] = []
    if total_colors <= 4 and (not laminated) and total_dies == 1:
        return "Mark Andy 2200", flags
    if total_colors <= 8:
        return "Mark Andy 4200", flags
    flags.append("OUT_OF_SCOPE_COLORS_GT_8")
    return None, flags


def complexity_score(printed: bool, total_colors: int, laminated: bool, total_dies: int, shape: str | None) -> float:
    score = 0.0
    if printed:
        score += 2.0
    score += total_colors * 0.5
    if laminated:
        score += 2.0
    if total_dies > 1:
        score += 1.5

    shape_text = (shape or "").lower()
    if any(token in shape_text for token in ("custom", "oval", "circle", "contour")):
        score += 1.0
    return score
