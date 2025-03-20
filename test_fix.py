#!/usr/bin/env python3

import json
from datetime import datetime
from pathlib import Path
from pprint import pprint
from typing import List, Optional, Dict, Any

def load_holidays(year: Optional[int] = None, file_name: Optional[str] = None) -> List[dict]:
    """
    Load holidays from year-based JSON files.
    If year is specified, load only that year's file.
    If file_name is specified, load that specific file.
    Otherwise, load all available years.
    """
    # Use absolute path resolution
    base_dir = Path(__file__).resolve().parent  # Current directory
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

def test_date_range_duplicates(from_date: str, to_date: str, include_historical: bool = True):
    """
    Test the date range functionality with and without duplicate prevention
    """
    try:
        # Validate date formats
        from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").date()
        to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").date()
        
        if to_date_obj < from_date_obj:
            print("Error: End date must be after start date")
            return
            
        # Determine which years to load based on date range
        start_year = from_date_obj.year
        end_year = to_date_obj.year
        
        # First approach: No duplicate prevention during loading
        holidays_without_prevention = []
        
        # Load modern data (2023 onward)
        for year in range(max(2023, start_year), end_year + 1):
            yearly_holidays = load_holidays(year)
            holidays_without_prevention.extend(yearly_holidays)
        
        # Load historical events if requested or if range includes years before 2023
        if include_historical or start_year < 2023:
            historical_events = load_holidays(file_name="historical.json")
            holidays_without_prevention.extend(historical_events)
        
        # Filter by date range
        range_holidays_no_prevention = [
            h for h in holidays_without_prevention 
            if from_date_obj <= datetime.fromisoformat(h["date"]).date() <= to_date_obj
        ]
        
        # Second approach: With duplicate prevention during loading
        processed_dates = set()
        holidays_with_prevention = []
        
        # Load modern data (2023 onward)
        for year in range(max(2023, start_year), end_year + 1):
            yearly_holidays = load_holidays(year)
            for h in yearly_holidays:
                # Create a unique key for each holiday
                unique_key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
                if unique_key not in processed_dates:
                    processed_dates.add(unique_key)
                    holidays_with_prevention.append(h)
        
        # Load historical events if requested or if range includes years before 2023
        if include_historical or start_year < 2023:
            historical_events = load_holidays(file_name="historical.json")
            for h in historical_events:
                # Create a unique key for each historical event
                unique_key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
                if unique_key not in processed_dates:
                    processed_dates.add(unique_key)
                    holidays_with_prevention.append(h)
        
        # Filter by date range
        range_holidays_with_prevention = [
            h for h in holidays_with_prevention 
            if from_date_obj <= datetime.fromisoformat(h["date"]).date() <= to_date_obj
        ]
        
        # Third approach: With additional duplicate check before forming response
        additional_check_holidays = list(range_holidays_with_prevention)
        processed_response_keys = set()
        unique_holidays = []
        
        for h in additional_check_holidays:
            key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
            if key not in processed_response_keys:
                processed_response_keys.add(key)
                unique_holidays.append(h)
        
        # Print results
        print(f"\nResults for date range: {from_date} to {to_date}\n")
        print(f"Without duplicate prevention: {len(range_holidays_no_prevention)} holidays")
        print(f"With duplicate prevention during loading: {len(range_holidays_with_prevention)} holidays")
        print(f"With additional check before response: {len(unique_holidays)} holidays")
        
        # Check for any duplicates in the final unique holidays list
        keys_in_unique = {}
        has_duplicates = False
        
        for h in unique_holidays:
            key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
            if key in keys_in_unique:
                print(f"\nDuplicate found in 'unique' holidays: {key}")
                has_duplicates = True
            else:
                keys_in_unique[key] = True
                
        if not has_duplicates:
            print("\nVerification successful: No duplicates in the final response")
            
        # Print the actual holidays
        print("\nHolidays found in date range:")
        for h in unique_holidays:
            print(f"{h['date']} - {h.get('type', 'unknown')} - {h['event']['en']}")
        
    except Exception as e:
        print(f"Error during testing: {e}")

if __name__ == "__main__":
    # Test with the Republic of Mahabad date range
    test_date_range_duplicates("1946-01-01", "1946-12-31") 