from fastapi import APIRouter, Request, Query
from typing import Optional, List
import json
from datetime import datetime
from enum import Enum
import os
from pathlib import Path

from api.core.rate_limiter import limiter

router = APIRouter(
    prefix="/api/v1/holidays",
    tags=["holidays"],
)

class Region(str, Enum):
    BASHUR = "bashur"
    BAKUR = "bakur"
    ROJHELAT = "rojhelat"
    ROJAVA = "rojava"
    ALL = "all"

def load_holidays(year: Optional[int] = None) -> List[dict]:
    """
    Load holidays from year-based JSON files.
    If year is specified, load only that year's file.
    Otherwise, load all available years.
    """
    data_dir = Path("data/years")
    holidays = []

    if year:
        file_path = data_dir / f"{year}.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                holidays.extend(data["holidays"])
    else:
        for file_path in data_dir.glob("*.json"):
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                holidays.extend(data["holidays"])
    
    return holidays

@router.get("")
@limiter.limit("10/minute")
async def get_holidays(
    request: Request,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    lang: str = Query("en", regex="^(en|ku|ar|fa)$"),
    is_holiday: Optional[bool] = None,
    region: Optional[Region] = None,
):
    """
    Get holidays with optional filters.
    Rate limited to 10 requests per minute.
    """
    holidays = load_holidays(year)
    
    # Apply filters
    if month:
        holidays = [h for h in holidays if datetime.fromisoformat(h["date"]).month == month]
    if day:
        holidays = [h for h in holidays if datetime.fromisoformat(h["date"]).day == day]
    if is_holiday is not None:
        holidays = [h for h in holidays if h["isHoliday"] == is_holiday]
    if region:
        holidays = [h for h in holidays if h["region"] == region or h["region"] == "all"]
    
    # Format response based on language
    return [{
        "date": h["date"],
        "kurdish_date": h["kurdish_date"],
        "isHoliday": h["isHoliday"],
        "event": h["event"][lang],
        "note": h["note"][lang] if h["note"].get(lang) else None,
        "region": h["region"],
        "image": h.get("image")
    } for h in holidays]

@router.get("/today")
@limiter.limit("10/minute")
async def get_today_holidays(
    request: Request,
    lang: str = Query("en", regex="^(en|ku|ar|fa)$"),
    region: Optional[Region] = None
):
    """
    Get today's holidays.
    Rate limited to 10 requests per minute.
    """
    today = datetime.now()
    holidays = load_holidays(today.year)
    today_str = today.strftime("%Y-%m-%d")
    today_holidays = [h for h in holidays if h["date"] == today_str]
    
    if region:
        today_holidays = [h for h in today_holidays if h["region"] == region or h["region"] == "all"]
    
    return [{
        "date": h["date"],
        "kurdish_date": h["kurdish_date"],
        "isHoliday": h["isHoliday"],
        "event": h["event"][lang],
        "note": h["note"][lang] if h["note"].get(lang) else None,
        "region": h["region"],
        "image": h.get("image")
    } for h in today_holidays]

@router.get("/{date}")
@limiter.limit("10/minute")
async def get_holidays_by_date(
    request: Request,
    date: str,
    lang: str = Query("en", regex="^(en|ku|ar|fa)$"),
    region: Optional[Region] = None
):
    """
    Get holidays for a specific date (YYYY-MM-DD).
    Rate limited to 10 requests per minute.
    """
    try:
        # Validate date format and get year
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        year = date_obj.year
    except ValueError:
        return {"error": "Invalid date format. Use YYYY-MM-DD"}
    
    holidays = load_holidays(year)
    date_holidays = [h for h in holidays if h["date"] == date]
    
    if region:
        date_holidays = [h for h in date_holidays if h["region"] == region or h["region"] == "all"]
    
    return [{
        "date": h["date"],
        "kurdish_date": h["kurdish_date"],
        "isHoliday": h["isHoliday"],
        "event": h["event"][lang],
        "note": h["note"][lang] if h["note"].get(lang) else None,
        "region": h["region"],
        "image": h.get("image")
    } for h in date_holidays]