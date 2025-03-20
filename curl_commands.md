# Kurdistan Calendar API Test Curl Commands

## Basic Endpoints

# Get all holidays
```bash
curl -X GET "http://localhost:8000/api/v1/holidays" | jq
```

# Get holidays for specific year
```bash
curl -X GET "http://localhost:8000/api/v1/holidays?year=2025" | jq
```

# Get holidays for specific month and year
```bash
curl -X GET "http://localhost:8000/api/v1/holidays?year=2025&month=3" | jq
```

# Get today's holidays
```bash
curl -X GET "http://localhost:8000/api/v1/holidays/today" | jq
```

# Get holidays for specific date
```bash
curl -X GET "http://localhost:8000/api/v1/holidays/2025-03-21" | jq
```

## Filtering Options

# Filter by language
```bash
curl -X GET "http://localhost:8000/api/v1/holidays?lang=ku" | jq
```

# Filter by region
```bash
curl -X GET "http://localhost:8000/api/v1/holidays?region=bashur" | jq
```

# Filter by holiday status
```bash
curl -X GET "http://localhost:8000/api/v1/holidays?is_holiday=true" | jq
```

# Filter by type
```bash
curl -X GET "http://localhost:8000/api/v1/holidays?type=historical&include_historical=true" | jq
```

# Date range filtering
```bash
curl -X GET "http://localhost:8000/api/v1/holidays/range/2025-01-01/2025-12-31" | jq
```

## Combined Filters

# Multiple filters combined
```bash
curl -X GET "http://localhost:8000/api/v1/holidays?year=2025&region=bashur&is_holiday=true&lang=en" | jq
```

# Range endpoint with multiple filters
```bash
curl -X GET "http://localhost:8000/api/v1/holidays/range/2025-01-01/2025-12-31?region=bashur&type=historical&include_historical=true" | jq
```

## Error Cases

# Invalid date format
```bash
curl -X GET "http://localhost:8000/api/v1/holidays/invalid-date" | jq
```

# Invalid language code
```bash
curl -X GET "http://localhost:8000/api/v1/holidays?lang=invalid" | jq
```

# Invalid date range (end before start)
```bash
curl -X GET "http://localhost:8000/api/v1/holidays/range/2025-12-31/2025-01-01" | jq
```

## Calendar API

# Convert Gregorian to Kurdish date
```bash
curl -X GET "http://localhost:8000/api/v1/calendar/convert/gregorian-to-kurdish?date=2025-03-21" | jq
```

# Convert Kurdish to Gregorian date
```bash
curl -X GET "http://localhost:8000/api/v1/calendar/convert/kurdish-to-gregorian?year=2725&month=Xakelew&day=1" | jq
```
