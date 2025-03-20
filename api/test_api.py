#!/usr/bin/env python3
"""
Test script for Kurdistan Calendar API
This script checks if the API endpoints are functioning correctly
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000/api/v1"

def test_endpoint(endpoint, description):
    """Test an API endpoint and print results"""
    print(f"\nTesting: {description}")
    print(f"Endpoint: {endpoint}")
    
    try:
        response = requests.get(endpoint)
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                print(f"Success: Received {len(data)} items")
            else:
                print(f"Success: Received response")
                
            return data
        else:
            print(f"Error: Status code {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print(f"Exception: {e}")
        return None

def check_for_duplicates(data, key_func):
    """Check for duplicates in the response data"""
    if not data or not isinstance(data, list):
        return False
        
    unique_keys = set()
    duplicates = []
    
    for item in data:
        key = key_func(item)
        if key in unique_keys:
            duplicates.append(key)
        else:
            unique_keys.add(key)
    
    if duplicates:
        print(f"Found {len(duplicates)} duplicate items")
        for dup in duplicates:
            print(f"  - Duplicate key: {dup}")
        return True
    else:
        print("No duplicates found")
        return False

def run_all_tests():
    """Run all API tests"""
    print("=== Kurdistan Calendar API Test ===")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test endpoints
    test_endpoint(f"{BASE_URL}/holidays", "All holidays")
    test_endpoint(f"{BASE_URL}/holidays/today", "Today's holidays")
    
    # Test date endpoint
    date_data = test_endpoint(f"{BASE_URL}/holidays/2023-03-21", "Specific date (Newroz)")
    if date_data:
        check_for_duplicates(date_data, lambda x: f"{x['date']}_{x.get('type')}_{x.get('region')}")
    
    # Test date range endpoint - historical data (Republic of Mahabad)
    range_data = test_endpoint(
        f"{BASE_URL}/holidays/range/1946-01-01/1946-12-31?include_historical=true", 
        "Date range (1946) with historical data"
    )
    if range_data:
        check_for_duplicates(range_data, lambda x: f"{x['date']}_{x.get('type')}_{x.get('region')}")
        
    # Test filtering
    test_endpoint(f"{BASE_URL}/holidays?type=historical", "Holidays filtered by type")
    test_endpoint(f"{BASE_URL}/holidays?region=bashur", "Holidays filtered by region")
    
    print("\n=== Test completed ===")

if __name__ == "__main__":
    run_all_tests() 