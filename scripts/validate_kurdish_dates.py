#!/usr/bin/env python3
"""
Script to validate Kurdish dates in the holiday data files.

This script checks:
1. All holidays have proper Kurdish date fields
2. Kurdish dates are valid and correctly calculated
3. Kurdish date formatting follows conventions
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Add the project root to path so we can import the API modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.utils.date_utils import (
    gregorian_to_kurdish,
    is_valid_kurdish_date,
    format_kurdish_date
)

def validate_file(file_path: Path) -> Tuple[bool, List[str]]:
    """
    Validate Kurdish dates in a single year file.
    
    Args:
        file_path: Path to the year JSON file
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    success = True
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if not isinstance(data, dict) or "holidays" not in data:
            errors.append(f"ERROR: Invalid file format in {file_path.name}, missing 'holidays' key")
            return False, errors
            
        holidays = data["holidays"]
        
        if not isinstance(holidays, list):
            errors.append(f"ERROR: 'holidays' is not a list in {file_path.name}")
            return False, errors
            
        for idx, holiday in enumerate(holidays):
            # Check if holiday has required fields
            if "date" not in holiday:
                errors.append(f"ERROR: Holiday at index {idx} missing 'date' field in {file_path.name}")
                success = False
                continue
                
            gregorian_date = holiday["date"]
            
            # Check kurdish_date exists
            if "kurdish_date" not in holiday:
                errors.append(f"ERROR: Holiday at index {idx} missing 'kurdish_date' field in {file_path.name}")
                success = False
                continue
                
            kurdish_date = holiday["kurdish_date"]
            
            # Check kurdish_date has all required fields
            required_fields = ["year", "month", "day", "full_date"]
            for field in required_fields:
                if field not in kurdish_date:
                    errors.append(f"ERROR: Holiday at index {idx} missing '{field}' in kurdish_date in {file_path.name}")
                    success = False
                    continue
            
            # Check if the Kurdish date is valid
            kurdish_year = kurdish_date["year"]
            kurdish_month = kurdish_date["month"]
            kurdish_day = kurdish_date["day"]
            
            if not is_valid_kurdish_date(kurdish_year, kurdish_month, kurdish_day):
                errors.append(
                    f"ERROR: Invalid Kurdish date {kurdish_year}-{kurdish_month}-{kurdish_day} "
                    f"in holiday at index {idx} in {file_path.name}"
                )
                success = False
            
            # Check if the Kurdish date calculation is correct
            calculated_kurdish_date = gregorian_to_kurdish(gregorian_date)
            
            if (calculated_kurdish_date["year"] != kurdish_date["year"] or
                calculated_kurdish_date["month"] != kurdish_date["month"] or 
                calculated_kurdish_date["day"] != kurdish_date["day"]):
                errors.append(
                    f"ERROR: Incorrect Kurdish date calculation in holiday at index {idx} in {file_path.name}. "
                    f"Got {kurdish_date['year']}-{kurdish_date['month']}-{kurdish_date['day']}, "
                    f"expected {calculated_kurdish_date['year']}-{calculated_kurdish_date['month']}-{calculated_kurdish_date['day']}"
                )
                success = False
            
            # Check if the full_date formatting is correct
            expected_full_date = format_kurdish_date(kurdish_day, kurdish_month, kurdish_year)
            
            if kurdish_date["full_date"] != expected_full_date:
                errors.append(
                    f"ERROR: Incorrect Kurdish date formatting in holiday at index {idx} in {file_path.name}. "
                    f"Got '{kurdish_date['full_date']}', expected '{expected_full_date}'"
                )
                success = False
                
        return success, errors
            
    except json.JSONDecodeError:
        errors.append(f"ERROR: Invalid JSON in {file_path.name}")
        return False, errors
    except Exception as e:
        errors.append(f"ERROR: Unexpected error processing {file_path.name}: {str(e)}")
        return False, errors

def validate_all_files() -> Tuple[bool, Dict[str, List[str]]]:
    """
    Validate Kurdish dates in all year files.
    
    Returns:
        Tuple of (all_valid, {file_name: [error_messages]})
    """
    data_dir = Path("data/years")
    all_valid = True
    all_errors = {}
    
    if not data_dir.exists() or not data_dir.is_dir():
        return False, {"global": [f"ERROR: Data directory not found at {data_dir}"]}
    
    year_files = list(data_dir.glob("*.json"))
    
    if not year_files:
        return False, {"global": [f"ERROR: No year files found in {data_dir}"]}
    
    for file_path in year_files:
        file_valid, file_errors = validate_file(file_path)
        if not file_valid:
            all_valid = False
            all_errors[file_path.name] = file_errors
    
    return all_valid, all_errors

def update_kurdish_dates(file_path: Path, dry_run: bool = False) -> Tuple[bool, List[str]]:
    """
    Update Kurdish dates in a data file.
    
    Args:
        file_path: Path to the year JSON file
        dry_run: If True, only show what would be changed without writing
        
    Returns:
        Tuple of (success, messages)
    """
    messages = []
    success = True
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if not isinstance(data, dict) or "holidays" not in data:
            messages.append(f"ERROR: Invalid file format in {file_path.name}, missing 'holidays' key")
            return False, messages
            
        holidays = data["holidays"]
        
        if not isinstance(holidays, list):
            messages.append(f"ERROR: 'holidays' is not a list in {file_path.name}")
            return False, messages
        
        changes_count = 0
        for idx, holiday in enumerate(holidays):
            if "date" not in holiday:
                messages.append(f"ERROR: Holiday at index {idx} missing 'date' field in {file_path.name}")
                success = False
                continue
                
            gregorian_date = holiday["date"]
            calculated_kurdish_date = gregorian_to_kurdish(gregorian_date)
            
            # If holiday doesn't have kurdish_date, add it
            if "kurdish_date" not in holiday:
                holiday["kurdish_date"] = calculated_kurdish_date
                changes_count += 1
                messages.append(f"Added Kurdish date for holiday at index {idx} in {file_path.name}")
                continue
            
            # Check if existing kurdish_date needs updating
            kurdish_date = holiday["kurdish_date"]
            needs_update = False
            
            required_fields = ["year", "month", "day", "full_date"]
            for field in required_fields:
                if field not in kurdish_date:
                    kurdish_date[field] = calculated_kurdish_date[field]
                    needs_update = True
            
            if (kurdish_date["year"] != calculated_kurdish_date["year"] or
                kurdish_date["month"] != calculated_kurdish_date["month"] or
                kurdish_date["day"] != calculated_kurdish_date["day"] or
                kurdish_date["full_date"] != calculated_kurdish_date["full_date"]):
                
                messages.append(
                    f"Updated Kurdish date for holiday at index {idx} in {file_path.name} from "
                    f"{kurdish_date['year']}-{kurdish_date['month']}-{kurdish_date['day']} to "
                    f"{calculated_kurdish_date['year']}-{calculated_kurdish_date['month']}-{calculated_kurdish_date['day']}"
                )
                
                # Update the Kurdish date
                holiday["kurdish_date"] = calculated_kurdish_date
                needs_update = True
            
            if needs_update:
                changes_count += 1
        
        if changes_count > 0 and not dry_run:
            # Write the updated data back to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            messages.append(f"Updated {changes_count} Kurdish dates in {file_path.name}")
        elif changes_count > 0:
            messages.append(f"Would update {changes_count} Kurdish dates in {file_path.name} (dry run)")
        else:
            messages.append(f"No Kurdish date updates needed in {file_path.name}")
        
        return success, messages
            
    except json.JSONDecodeError:
        messages.append(f"ERROR: Invalid JSON in {file_path.name}")
        return False, messages
    except Exception as e:
        messages.append(f"ERROR: Unexpected error processing {file_path.name}: {str(e)}")
        return False, messages

def main():
    parser = argparse.ArgumentParser(description="Validate and update Kurdish dates in holiday data files")
    parser.add_argument('--update', action='store_true', help="Update Kurdish dates in files")
    parser.add_argument('--dry-run', action='store_true', help="Show what would be updated without making changes")
    parser.add_argument('--file', type=str, help="Only validate/update a specific file (e.g., 2025.json)")
    
    args = parser.parse_args()
    
    if args.file:
        file_path = Path(f"data/years/{args.file}")
        
        if not file_path.exists():
            print(f"ERROR: File not found: {file_path}")
            sys.exit(1)
            
        if args.update:
            success, messages = update_kurdish_dates(file_path, args.dry_run)
            for msg in messages:
                print(msg)
            if not success:
                sys.exit(1)
        else:
            success, errors = validate_file(file_path)
            if not success:
                for error in errors:
                    print(error)
                sys.exit(1)
            else:
                print(f"✅ {file_path.name} - All Kurdish dates are valid")
    else:
        if args.update:
            data_dir = Path("data/years")
            if not data_dir.exists() or not data_dir.is_dir():
                print(f"ERROR: Data directory not found at {data_dir}")
                sys.exit(1)
                
            year_files = list(data_dir.glob("*.json"))
            any_failure = False
            
            for file_path in year_files:
                success, messages = update_kurdish_dates(file_path, args.dry_run)
                for msg in messages:
                    print(msg)
                if not success:
                    any_failure = True
            
            if any_failure:
                sys.exit(1)
        else:
            all_valid, all_errors = validate_all_files()
            
            if not all_valid:
                for file_name, errors in all_errors.items():
                    for error in errors:
                        print(error)
                print("\n❌ Validation failed. Some files have errors.")
                sys.exit(1)
            else:
                print("✅ All Kurdish dates in all files are valid")

if __name__ == "__main__":
    main() 