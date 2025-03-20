#!/usr/bin/env python3

import sys
from datetime import datetime
from pathlib import Path
import json
from typing import List, Optional, Dict, Any, Set

# Fix path
sys.path.append(str(Path(__file__).resolve().parent.parent))

def load_holidays(year: Optional[int] = None, file_name: Optional[str] = None) -> List[dict]:
    # Use absolute path resolution
    base_dir = Path(__file__).resolve().parents[1]  # Go up one level from api
    data_dir = base_dir / "data" / "years"
    
    holidays = []

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
        for file_path in data_dir.glob("*.json"):
            if file_path.name != "historical.json":  # Skip historical.json when loading all
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    holidays.extend(data["holidays"])
    
    return holidays

def get_holidays_by_date_range(from_date: str, to_date: str, include_historical: bool = False) -> List[Dict[str, Any]]:
    try:
        # Validate date formats
        from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
        to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
        
        if to_date_obj < from_date_obj:
            raise ValueError("End date must be after start date")
            
        # Determine which years to load based on date range
        start_year = from_date_obj.year
        end_year = to_date_obj.year
        
        # Track processed dates to avoid duplicates
        processed_dates: Set[str] = set()
        holidays = []
        
        # Load modern data (2023 onward)
        for year in range(max(2023, start_year), end_year + 1):
            yearly_holidays = load_holidays(year)
            for h in yearly_holidays:
                # Create a unique key for each holiday
                unique_key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
                if unique_key not in processed_dates:
                    processed_dates.add(unique_key)
                    holidays.append(h)
        
        # Load historical events if requested or if range includes years before 2023
        if include_historical or start_year < 2023:
            historical_events = load_holidays(file_name="historical.json")
            for h in historical_events:
                # Create a unique key for each historical event
                unique_key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
                if unique_key not in processed_dates:
                    processed_dates.add(unique_key)
                    holidays.append(h)
        
        # Filter by date range
        range_holidays = [
            h for h in holidays 
            if from_date_obj <= datetime.fromisoformat(h["date"]).date() <= to_date_obj
        ]
        
        # Sort by date
        range_holidays.sort(key=lambda h: h["date"])
        
        return range_holidays
        
    except ValueError as e:
        print(f"Error: {e}")
        return []

def main():
    from_date = "1946-01-01"
    to_date = "1946-12-31"
    
    print(f"\nTesting date range from {from_date} to {to_date} with historical data:")
    holidays = get_holidays_by_date_range(from_date, to_date, include_historical=True)
    
    print(f"Found {len(holidays)} holidays in range")
    
    # Check for duplicates
    date_keys = {}
    for h in holidays:
        key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
        if key in date_keys:
            print(f"⚠️ DUPLICATE DETECTED: {key}")
        else:
            date_keys[key] = True
    
    # Print results
    for h in holidays:
        print(f"{h['date']} - {h.get('type', 'unknown')} - {h['event']['en']}")
    
    print("\nTest complete!")

if __name__ == "__main__":
    main() 