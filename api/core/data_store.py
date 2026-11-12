"""Loads the JSON data files once and reloads them only when they change on disk."""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "years"
HISTORICAL = "historical"

_cache: Dict[str, Tuple[float, dict]] = {}


def _load(name: str) -> Optional[dict]:
    path = DATA_DIR / f"{name}.json"
    try:
        mtime = path.stat().st_mtime
    except FileNotFoundError:
        return None
    cached = _cache.get(name)
    if cached and cached[0] == mtime:
        return cached[1]
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        logger.error("Could not load %s: %s", path, exc)
        return None
    _cache[name] = (mtime, data)
    return data


def available_years() -> List[int]:
    return sorted(int(p.stem) for p in DATA_DIR.glob("*.json") if p.stem.isdigit())


def year_info() -> List[dict]:
    """Year, status (official/projected) and number of entries per data file."""
    out = []
    for year in available_years():
        data = _load(str(year)) or {}
        out.append({
            "year": year,
            "status": data.get("status", "official"),
            "count": len(data.get("holidays", [])),
            "sources": data.get("sources", []),
        })
    return out


def get_events(years: Optional[List[int]] = None, include_historical: bool = False) -> List[dict]:
    """Events for the given years (all years when None), sorted by date."""
    events: List[dict] = []
    for year in (available_years() if years is None else years):
        data = _load(str(year))
        if data:
            events.extend(data.get("holidays", []))
    if include_historical:
        data = _load(HISTORICAL)
        if data:
            events.extend(data.get("holidays", []))
    return sorted(events, key=lambda e: e.get("date", ""))
