#!/usr/bin/env python3

import requests
import json
from datetime import datetime
import sys
import time

# Base URL for the API
BASE_URL = "http://localhost:8000/api/v1"

def test_endpoint(url, expected_status=200, description="", method="GET", json_data=None):
    """Test an endpoint and print the result"""
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=json_data)
        else:
            raise ValueError(f"Unsupported method: {method}")
            
        status = "✅ PASS" if response.status_code == expected_status else f"❌ FAIL (Status: {response.status_code})"
        
        if response.status_code == 200 and isinstance(response.json(), list):
            data_count = len(response.json())
        elif response.status_code == 200:
            data_count = "Object"
        else:
            data_count = "N/A"
        
        print(f"{status} | {description} | Items: {data_count}")
        return response.json() if response.status_code == expected_status else None
    except Exception as e:
        print(f"❌ ERROR | {description} | {str(e)}")
        return None

def main():
    print("\n🧪 Testing Kurdistan Calendar API - Enhanced Filtering Options 🧪")
    print("=" * 80)
    print("Testing base endpoints...")
    
    # Test basic endpoints
    test_endpoint(f"{BASE_URL}/holidays", description="Get all holidays")
    test_endpoint(f"{BASE_URL}/holidays/today", description="Get today's holidays")
    
    # Test date endpoint
    nawroz_date = "2024-03-21"
    test_endpoint(f"{BASE_URL}/holidays/{nawroz_date}", description=f"Get holidays for {nawroz_date}")
    
    print("\n" + "=" * 80)
    print("Testing new filtering options...")
    
    # Test type filtering
    historical_data = test_endpoint(
        f"{BASE_URL}/holidays?type=historical", 
        description="Filter by historical type"
    )
    
    # Test date range filtering
    date_range_data = test_endpoint(
        f"{BASE_URL}/holidays/range/2024-03-01/2024-04-30",
        description="Date range from Mar 1 to Apr 30, 2024"
    )
    
    # Test combined filters
    combined_filters_data = test_endpoint(
        f"{BASE_URL}/holidays?from_date=2024-01-01&to_date=2024-12-31&region=bashur&lang=ku",
        description="Combined filters: 2024, bashur region, Kurdish language"
    )
    
    # Test historical inclusion
    historical_included = test_endpoint(
        f"{BASE_URL}/holidays?include_historical=true&year=2023",
        description="Include historical events with 2023 holidays"
    )
    
    print("\n" + "=" * 80)
    print("Testing invalid inputs...")
    
    # Test invalid date format
    test_endpoint(
        f"{BASE_URL}/holidays/range/2024-03-32/2024-04-30",
        expected_status=422,  # FastAPI validation error
        description="Invalid date format in range"
    )
    
    # Test invalid type
    test_endpoint(
        f"{BASE_URL}/holidays?type=invalid_type",
        expected_status=422,  # FastAPI validation error
        description="Invalid event type"
    )
    
    # Additional tests for calendar conversion
    print("\n" + "=" * 80)
    print("Testing calendar conversion endpoints...")
    
    test_endpoint(
        f"{BASE_URL}/calendar/convert/gregorian-to-kurdish/2024-03-21",
        description="Convert Gregorian to Kurdish date (GET)"
    )
    
    test_endpoint(
        f"{BASE_URL}/calendar/convert/gregorian-to-kurdish",
        method="POST",
        json_data={"date": "2024-03-21"},
        description="Convert Gregorian to Kurdish date (POST)"
    )
    
    test_endpoint(
        f"{BASE_URL}/calendar/convert/kurdish-to-gregorian",
        method="POST",
        json_data={"year": 2724, "month": "Xakelew", "day": 1},
        description="Convert Kurdish to Gregorian date (POST)"
    )
    
    test_endpoint(
        f"{BASE_URL}/calendar/validate/kurdish-date?year=2724&month=Xakelew&day=1",
        description="Validate Kurdish date"
    )
    
    print("\n" + "=" * 80)
    print("🏁 Testing complete!")

if __name__ == "__main__":
    # Wait a moment for the server to start
    time.sleep(1)
    main() 