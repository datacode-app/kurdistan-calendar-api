#!/usr/bin/env python3

import subprocess
import json
import sys

def run_curl(url):
    """Run curl command and parse JSON response"""
    try:
        result = subprocess.run(
            ["curl", "-s", url],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error running curl: {e}")
        return None

def test_date_range():
    print("Testing date range API endpoint:")
    url = "http://localhost:8000/api/v1/holidays/range/1946-01-01/1946-12-31?include_historical=true"
    data = run_curl(url)
    
    if not data:
        print("Failed to get data from API")
        return
    
    print(f"API returned {len(data)} holidays")
    
    # Check for duplicates
    date_keys = {}
    for h in data:
        key = f"{h['date']}_{h.get('type', 'unknown')}_{h.get('region', 'unknown')}"
        if key in date_keys:
            print(f"⚠️ DUPLICATE DETECTED: {key}")
        else:
            date_keys[key] = True
    
    # Print results
    for h in data:
        print(f"{h['date']} - {h.get('type', 'unknown')} - {h['event']}")

def main():
    test_date_range()

if __name__ == "__main__":
    main() 