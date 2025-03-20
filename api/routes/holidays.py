from fastapi import APIRouter, Request, Query
from typing import Optional, List, Union
import json
from datetime import datetime, date
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

class EventType(str, Enum):
    HISTORICAL = "historical"
    POLITICAL = "political"
    COMMEMORATION = "commemoration"
    CULTURAL = "cultural"
    RELIGIOUS = "religious"
    OFFICIAL = "official"

def load_holidays(year: Optional[int] = None, file_name: Optional[str] = None) -> List[dict]:
    """
    Load holidays from year-based JSON files.
    If year is specified, load only that year's file.
    If file_name is specified, load that specific file.
    Otherwise, load all available years.
    """
    # Use absolute path resolution
    base_dir = Path(__file__).resolve().parents[2]  # Go up two levels from routes
    data_dir = base_dir / "data" / "years"
    
    holidays = []

    try:
        if file_name:
            file_path = data_dir / file_name
            print(f"Loading from file: {file_path}, exists: {file_path.exists()}")
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    holidays.extend(data["holidays"])
                    print(f"Loaded {len(data['holidays'])} items from {file_name}")
        elif year:
            file_path = data_dir / f"{year}.json"
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    holidays.extend(data["holidays"])
            else:
                print(f"Warning: Year file {year}.json not found.")
        else:
            # When no year is specified, load all available year files
            found_files = False
            for file_path in data_dir.glob("*.json"):
                if file_path.name != "historical.json":  # Skip historical.json when loading all
                    found_files = True
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            holidays.extend(data["holidays"])
                    except json.JSONDecodeError:
                        print(f"Warning: Could not parse JSON in {file_path}")
                    except Exception as e:
                        print(f"Warning: Error loading {file_path}: {e}")
            
            if not found_files:
                print("Warning: No year files found in data directory.")
        
        return holidays
    except Exception as e:
        print(f"Error loading holidays: {e}")
        return []

@router.get("")
@limiter.limit("10/minute")
async def get_holidays(
    request: Request,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    lang: str = Query("en", regex="^(en|ku|ar|fa)$"),
    is_holiday: Optional[bool] = None,
    region: Optional[Region] = None,
    type: Optional[EventType] = None,
    include_historical: Optional[bool] = False,
):
    """
    Get holidays with optional filters.
    Rate limited to 10 requests per minute.
    
    Parameters:
    - year: Filter by year
    - month: Filter by month
    - day: Filter by day
    - from_date: Start date for range filter (YYYY-MM-DD)
    - to_date: End date for range filter (YYYY-MM-DD)
    - lang: Language for event and note fields (en, ku, ar, fa)
    - is_holiday: Filter by holiday status
    - region: Filter by region (bashur, bakur, rojhelat, rojava, all)
    - type: Filter by event type (historical, political, commemoration, cultural, religious, official)
    - include_historical: Include events from historical.json
    """
    try:
        # Track processed dates to avoid duplicates
        processed_dates = set()
        holidays = []
        
        # Load regular holidays based on year
        yearly_holidays = load_holidays(year)
        for h in yearly_holidays:
            try:
                # Create a unique key for each holiday
                unique_key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
                if unique_key not in processed_dates:
                    processed_dates.add(unique_key)
                    holidays.append(h)
            except KeyError:
                # Skip entries with missing required fields
                continue
        
        # Load historical events if requested
        if include_historical:
            historical_events = load_holidays(file_name="historical.json")
            for h in historical_events:
                try:
                    # Create a unique key for each historical event
                    unique_key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
                    if unique_key not in processed_dates:
                        processed_dates.add(unique_key)
                        holidays.append(h)
                except KeyError:
                    # Skip entries with missing required fields
                    continue
        
        # Apply date range filters if provided
        if from_date:
            try:
                from_date_obj = datetime.fromisoformat(from_date).date()
                holidays = [h for h in holidays if 'date' in h and datetime.fromisoformat(h["date"]).date() >= from_date_obj]
            except ValueError:
                return {"error": "Invalid from_date format. Use YYYY-MM-DD"}
        
        if to_date:
            try:
                to_date_obj = datetime.fromisoformat(to_date).date()
                holidays = [h for h in holidays if 'date' in h and datetime.fromisoformat(h["date"]).date() <= to_date_obj]
            except ValueError:
                return {"error": "Invalid to_date format. Use YYYY-MM-DD"}
        
        # Apply single date component filters
        if month:
            holidays = [h for h in holidays if 'date' in h and datetime.fromisoformat(h["date"]).month == month]
        if day:
            holidays = [h for h in holidays if 'date' in h and datetime.fromisoformat(h["date"]).day == day]
        
        # Apply other filters
        if is_holiday is not None:
            holidays = [h for h in holidays if 'isHoliday' in h and h["isHoliday"] == is_holiday]
        
        # Apply region filtering (ensure it's case-insensitive)
        if region:
            region_value = region.value.lower() if hasattr(region, 'value') else region.lower()
            holidays = [
                h for h in holidays if 
                'region' in h and (
                    h["region"].lower() == region_value or 
                    h["region"].lower() == "all"
                )
            ]
        
        # Apply type filtering
        if type:
            type_value = type.value if hasattr(type, 'value') else type
            holidays = [h for h in holidays if 'type' in h and h.get("type") == type_value]
        
        # Format response based on language
        result = []
        for h in holidays:
            try:
                entry = {
                    "date": h["date"],
                    "kurdish_date": h.get("kurdish_date", {}),
                    "isHoliday": h.get("isHoliday", False),
                    "event": h["event"].get(lang, h["event"].get("en", "Unknown")),
                    "note": h["note"].get(lang) if h.get("note", {}).get(lang) else None,
                    "region": h.get("region", "unknown"),
                    "type": h.get("type"),
                    "image": h.get("image")
                }
                result.append(entry)
            except (KeyError, AttributeError) as e:
                # Skip malformed entries
                print(f"Warning: Skipping malformed entry: {e}")
                continue
        
        return result
    except Exception as e:
        print(f"Error in get_holidays: {e}")
        return {"error": "An unexpected error occurred while processing your request."}

@router.get("/today")
@limiter.limit("10/minute")
async def get_today_holidays(
    request: Request,
    lang: str = Query("en", regex="^(en|ku|ar|fa)$"),
    region: Optional[Region] = None,
    type: Optional[EventType] = None,
    include_historical: Optional[bool] = False
):
    """
    Get today's holidays.
    Rate limited to 10 requests per minute.
    
    Parameters:
    - lang: Language for event and note fields (en, ku, ar, fa)
    - region: Filter by region (bashur, bakur, rojhelat, rojava, all)
    - type: Filter by event type (historical, political, commemoration, cultural, religious, official)
    - include_historical: Include events from historical.json
    """
    try:
        today = datetime.now()
        today_str = today.strftime("%Y-%m-%d")
        
        # Track processed dates to avoid duplicates
        processed_dates = set()
        holidays = []
        
        # Load regular holidays for current year
        yearly_holidays = load_holidays(today.year)
        for h in yearly_holidays:
            try:
                # Create a unique key for each holiday
                unique_key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
                if unique_key not in processed_dates:
                    processed_dates.add(unique_key)
                    holidays.append(h)
            except KeyError:
                # Skip entries with missing required fields
                continue
        
        # Load historical events if requested
        if include_historical:
            historical_events = load_holidays(file_name="historical.json")
            for h in historical_events:
                try:
                    # Create a unique key for each historical event
                    unique_key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
                    if unique_key not in processed_dates:
                        processed_dates.add(unique_key)
                        holidays.append(h)
                except KeyError:
                    # Skip entries with missing required fields
                    continue
        
        # Filter for today's date
        today_holidays = [h for h in holidays if 'date' in h and h["date"] == today_str]
        
        # Apply region filtering (ensure it's case-insensitive)
        if region:
            region_value = region.value.lower() if hasattr(region, 'value') else region.lower()
            today_holidays = [
                h for h in today_holidays if 
                'region' in h and (
                    h["region"].lower() == region_value or 
                    h["region"].lower() == "all"
                )
            ]
        
        # Apply type filtering
        if type:
            type_value = type.value if hasattr(type, 'value') else type
            today_holidays = [h for h in today_holidays if 'type' in h and h.get("type") == type_value]
        
        # Format response
        result = []
        for h in today_holidays:
            try:
                entry = {
                    "date": h["date"],
                    "kurdish_date": h.get("kurdish_date", {}),
                    "isHoliday": h.get("isHoliday", False),
                    "event": h["event"].get(lang, h["event"].get("en", "Unknown")),
                    "note": h["note"].get(lang) if h.get("note", {}).get(lang) else None,
                    "region": h.get("region", "unknown"),
                    "type": h.get("type"),
                    "image": h.get("image")
                }
                result.append(entry)
            except (KeyError, AttributeError) as e:
                # Skip malformed entries
                print(f"Warning: Skipping malformed entry: {e}")
                continue
        
        return result
    except Exception as e:
        print(f"Error in get_today_holidays: {e}")
        return {"error": "An unexpected error occurred while processing your request."}

@router.get("/{date}")
@limiter.limit("10/minute")
async def get_holidays_by_date(
    request: Request,
    date: str,
    lang: str = Query("en", regex="^(en|ku|ar|fa)$"),
    region: Optional[Region] = None,
    type: Optional[EventType] = None,
    include_historical: Optional[bool] = False
):
    """
    Get holidays for a specific date (YYYY-MM-DD).
    Rate limited to 10 requests per minute.
    
    Parameters:
    - date: Date in YYYY-MM-DD format
    - lang: Language for event and note fields (en, ku, ar, fa)
    - region: Filter by region (bashur, bakur, rojhelat, rojava, all)
    - type: Filter by event type (historical, political, commemoration, cultural, religious, official)
    - include_historical: Include events from historical.json
    """
    try:
        # Validate date format and get year
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            year = date_obj.year
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD"}
        
        # Track processed dates to avoid duplicates
        processed_dates = set()
        holidays = []
        
        # For historical dates, we need to load all files
        if date_obj.year < 2023:
            # For very old dates, only check historical file
            if include_historical:
                historical_events = load_holidays(file_name="historical.json")
                for h in historical_events:
                    try:
                        # Create a unique key for each historical event
                        unique_key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
                        if unique_key not in processed_dates:
                            processed_dates.add(unique_key)
                            holidays.append(h)
                    except KeyError:
                        # Skip entries with missing required fields
                        continue
        else:
            yearly_holidays = load_holidays(year)
            for h in yearly_holidays:
                try:
                    # Create a unique key for each holiday
                    unique_key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
                    if unique_key not in processed_dates:
                        processed_dates.add(unique_key)
                        holidays.append(h)
                except KeyError:
                    # Skip entries with missing required fields
                    continue
            
            # Load historical events if requested
            if include_historical:
                historical_events = load_holidays(file_name="historical.json")
                for h in historical_events:
                    try:
                        # Create a unique key for each historical event
                        unique_key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
                        if unique_key not in processed_dates:
                            processed_dates.add(unique_key)
                            holidays.append(h)
                    except KeyError:
                        # Skip entries with missing required fields
                        continue
        
        date_holidays = [h for h in holidays if 'date' in h and h["date"] == date]
        
        # Apply region filtering (ensure it's case-insensitive)
        if region:
            region_value = region.value.lower() if hasattr(region, 'value') else region.lower()
            date_holidays = [
                h for h in date_holidays if 
                'region' in h and (
                    h["region"].lower() == region_value or 
                    h["region"].lower() == "all"
                )
            ]
        
        # Apply type filtering
        if type:
            type_value = type.value if hasattr(type, 'value') else type
            date_holidays = [h for h in date_holidays if 'type' in h and h.get("type") == type_value]
        
        # Format response
        result = []
        for h in date_holidays:
            try:
                entry = {
                    "date": h["date"],
                    "kurdish_date": h.get("kurdish_date", {}),
                    "isHoliday": h.get("isHoliday", False),
                    "event": h["event"].get(lang, h["event"].get("en", "Unknown")),
                    "note": h["note"].get(lang) if h.get("note", {}).get(lang) else None,
                    "region": h.get("region", "unknown"),
                    "type": h.get("type"),
                    "image": h.get("image")
                }
                result.append(entry)
            except (KeyError, AttributeError) as e:
                # Skip malformed entries
                print(f"Warning: Skipping malformed entry: {e}")
                continue
                
        return result
    except Exception as e:
        print(f"Error in get_holidays_by_date: {e}")
        return {"error": "An unexpected error occurred while processing your request."}

@router.get("/range/{from_date}/{to_date}")
@limiter.limit("10/minute")
async def get_holidays_by_date_range(
    request: Request,
    from_date: str,
    to_date: str,
    lang: str = Query("en", regex="^(en|ku|ar|fa)$"),
    region: Optional[Region] = None,
    type: Optional[EventType] = None,
    is_holiday: Optional[bool] = None,
    include_historical: Optional[bool] = False
):
    """
    Get holidays within a specific date range.
    Rate limited to 10 requests per minute.
    
    Parameters:
    - from_date: Start date in YYYY-MM-DD format
    - to_date: End date in YYYY-MM-DD format
    - lang: Language for event and note fields (en, ku, ar, fa)
    - region: Filter by region (bashur, bakur, rojhelat, rojava, all)
    - type: Filter by event type (historical, political, commemoration, cultural, religious, official)
    - is_holiday: Filter by holiday status
    - include_historical: Include events from historical.json
    """
    try:
        # Validate date formats
        try:
            from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
            to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
        except ValueError:
            return {"error": "Invalid date format. Use YYYY-MM-DD"}
        
        if to_date_obj < from_date_obj:
            return {"error": "End date must be after start date"}
            
        # Determine which years to load based on date range
        start_year = from_date_obj.year
        end_year = to_date_obj.year
        
        # Track processed dates to avoid duplicates
        processed_dates = set()
        holidays = []
        
        # Load modern data (2023 onward)
        for year in range(max(2023, start_year), end_year + 1):
            yearly_holidays = load_holidays(year)
            for h in yearly_holidays:
                try:
                    # Create a unique key for each holiday
                    unique_key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
                    if unique_key not in processed_dates:
                        processed_dates.add(unique_key)
                        holidays.append(h)
                except KeyError:
                    # Skip entries with missing required fields
                    continue
        
        # Load historical events if requested or if range includes years before 2023
        if include_historical or start_year < 2023:
            historical_events = load_holidays(file_name="historical.json")
            for h in historical_events:
                try:
                    # Create a unique key for each historical event
                    unique_key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
                    if unique_key not in processed_dates:
                        processed_dates.add(unique_key)
                        holidays.append(h)
                except KeyError:
                    # Skip entries with missing required fields
                    continue
        
        # Filter by date range
        range_holidays = [
            h for h in holidays 
            if 'date' in h and from_date_obj <= datetime.fromisoformat(h["date"]).date() <= to_date_obj
        ]
        
        # Apply additional filters
        # Apply region filtering (ensure it's case-insensitive)
        if region:
            region_value = region.value.lower() if hasattr(region, 'value') else region.lower()
            range_holidays = [
                h for h in range_holidays if 
                'region' in h and (
                    h["region"].lower() == region_value or 
                    h["region"].lower() == "all"
                )
            ]
        
        # Apply type filtering
        if type:
            type_value = type.value if hasattr(type, 'value') else type
            range_holidays = [h for h in range_holidays if 'type' in h and h.get("type") == type_value]
            
        if is_holiday is not None:
            range_holidays = [h for h in range_holidays if 'isHoliday' in h and h["isHoliday"] == is_holiday]
        
        # Sort by date
        range_holidays.sort(key=lambda h: h["date"])
        
        # Additional duplicate check before forming the response
        processed_response_keys = set()
        unique_holidays = []
        
        for h in range_holidays:
            try:
                key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
                if key not in processed_response_keys:
                    processed_response_keys.add(key)
                    unique_holidays.append(h)
            except KeyError:
                # Skip entries with missing required fields
                continue
        
        # Form the response with the unique holidays
        result = []
        for h in unique_holidays:
            try:
                entry = {
                    "date": h["date"],
                    "kurdish_date": h.get("kurdish_date", {}),
                    "isHoliday": h.get("isHoliday", False),
                    "event": h["event"].get(lang, h["event"].get("en", "Unknown")),
                    "note": h["note"].get(lang) if h.get("note", {}).get(lang) else None,
                    "region": h.get("region", "unknown"),
                    "type": h.get("type"),
                    "image": h.get("image")
                }
                result.append(entry)
            except (KeyError, AttributeError) as e:
                # Skip malformed entries
                print(f"Warning: Skipping malformed entry: {e}")
                continue
                
        return result
        
    except Exception as e:
        print(f"Error in get_holidays_by_date_range: {e}")
        return {"error": "An unexpected error occurred while processing your request."}