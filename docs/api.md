# Kurdistan Calendar API Documentation

## Overview

The Kurdistan Calendar API provides access to Kurdish holidays, historical events, and cultural celebrations. The API is rate-limited to ensure fair usage and system stability.

## Base URL

```
http://localhost:8000
```

## Rate Limits

- 10 requests per minute per IP address
- 1000 requests per day per IP address

## Authentication

Currently, the API is open and does not require authentication.

## Endpoints

### 1. Get All Holidays

```http
GET /api/v1/holidays
```

Retrieve all holidays with optional filters.

#### Query Parameters

| Parameter  | Type    | Description                                      | Example        |
|-----------|---------|--------------------------------------------------|----------------|
| year      | integer | Filter by year                                   | 2024          |
| month     | integer | Filter by month (1-12)                          | 3             |
| day       | integer | Filter by day of month (1-31)                   | 21            |
| lang      | string  | Language for responses (en, ku, ar, fa)         | en            |
| is_holiday| boolean | Filter by holiday status                        | true          |
| region    | string  | Filter by region (bashur, bakur, rojhelat, rojava, all) | bashur |

#### Response Format

```json
[
  {
    "date": "2024-03-21",
    "kurdish_date": {
      "year": 2324,
      "month": "Xakelew",
      "day": 1,
      "full_date": "١ی خاکەلێو ٢٣٢٤"
    },
    "isHoliday": true,
    "event": "Nawroz - Kurdish New Year",
    "note": "Traditional celebration of spring and new year",
    "region": "all",
    "image": "https://example.com/nawroz2024.jpg"
  }
]
```

### 2. Get Today's Holidays

```http
GET /api/v1/holidays/today
```

Retrieve holidays for the current date.

#### Query Parameters

| Parameter | Type   | Description                                      | Example        |
|-----------|--------|--------------------------------------------------|----------------|
| lang      | string | Language for responses (en, ku, ar, fa)         | en            |
| region    | string | Filter by region (bashur, bakur, rojhelat, rojava, all) | bashur |

#### Response Format

```json
[
  {
    "date": "2024-03-19",
    "kurdish_date": {
      "year": 2323,
      "month": "Reşeme",
      "day": 29,
      "full_date": "٢٩ی ڕەشەمە ٢٣٢٣"
    },
    "isHoliday": true,
    "event": "Example Holiday",
    "note": "Holiday description",
    "region": "bashur",
    "image": "https://example.com/holiday.jpg"
  }
]
```

### 3. Get Holidays by Date

```http
GET /api/v1/holidays/{date}
```

Retrieve holidays for a specific date.

#### Path Parameters

| Parameter | Type   | Description                | Example     |
|-----------|--------|----------------------------|-------------|
| date      | string | Date in YYYY-MM-DD format | 2024-03-21 |

#### Query Parameters

| Parameter | Type   | Description                                      | Example        |
|-----------|--------|--------------------------------------------------|----------------|
| lang      | string | Language for responses (en, ku, ar, fa)         | en            |
| region    | string | Filter by region (bashur, bakur, rojhelat, rojava, all) | bashur |

#### Response Format

```json
[
  {
    "date": "2024-03-21",
    "kurdish_date": {
      "year": 2324,
      "month": "Xakelew",
      "day": 1,
      "full_date": "١ی خاکەلێو ٢٣٢٤"
    },
    "isHoliday": true,
    "event": "Nawroz - Kurdish New Year",
    "note": "Traditional celebration of spring and new year",
    "region": "all",
    "image": "https://example.com/nawroz2024.jpg"
  }
]
```

## Response Fields

| Field        | Type    | Description                                    |
|-------------|---------|------------------------------------------------|
| date        | string  | Date in YYYY-MM-DD format                     |
| kurdish_date| object  | Date in Kurdish calendar format               |
| isHoliday   | boolean | Whether this is an official holiday           |
| event       | string  | Name of the event in the requested language   |
| note        | string  | Additional information (optional)             |
| region      | string  | Region where the holiday is celebrated        |
| image       | string  | URL or path to an image (optional)           |

### Kurdish Date Object

| Field     | Type   | Description                                    |
|-----------|--------|------------------------------------------------|
| year      | number | Kurdish year (Gregorian year - ~700)          |
| month     | string | Kurdish month name                            |
| day       | number | Day of the month                              |
| full_date | string | Full date in Kurdish format                   |

### Kurdish Month Names

| Month Number | Kurdish Name | Gregorian Months |
|-------------|--------------|------------------|
| 1 | Xakelew | March/April |
| 2 | Gullan | April/May |
| 3 | Cozerdan | May/June |
| 4 | Pûşper | June/July |
| 5 | Gelawêj | July/August |
| 6 | Xermanan | August/September |
| 7 | Rezber | September/October |
| 8 | Gelarêzan | October/November |
| 9 | Sermawez | November/December |
| 10 | Befranbar | December/January |
| 11 | Rêbendan | January/February |
| 12 | Reşeme | February/March |

## Languages

The API supports four languages:

| Code | Language |
|------|----------|
| en   | English  |
| ku   | Kurdish  |
| ar   | Arabic   |
| fa   | Persian  |

## Regions

The API supports five region values:

| Value    | Description                    |
|----------|--------------------------------|
| bashur   | South Kurdistan (Iraqi Kurdistan) |
| bakur    | North Kurdistan (Turkish Kurdistan) |
| rojhelat | East Kurdistan (Iranian Kurdistan) |
| rojava   | West Kurdistan (Syrian Kurdistan) |
| all      | All Kurdish regions            |

## Error Responses

### Rate Limit Exceeded

```json
{
  "status": "error",
  "message": "Rate limit exceeded. Try again in 60 seconds.",
  "code": "RATE_LIMIT_EXCEEDED"
}
```

### Invalid Date Format

```json
{
  "status": "error",
  "message": "Invalid date format. Use YYYY-MM-DD.",
  "code": "INVALID_DATE_FORMAT"
}
```

## CORS Support

The API supports Cross-Origin Resource Sharing (CORS) for all origins, allowing you to make requests directly from web browsers.

## Calendar Integration

The API supports exporting holiday data in iCalendar format:

```
GET /holidays/ical?year=2025
```

This will return an iCalendar (.ics) file that can be imported into calendar applications like Google Calendar, Apple Calendar, or Microsoft Outlook.

## SDK Support

We provide official client libraries for the following languages:

- JavaScript/TypeScript: [npm package](https://www.npmjs.com/package/kurdistan-calendar-api)
- Python: [PyPI package](https://pypi.org/project/kurdistan-calendar-api/)

## Support

If you have any questions or need help integrating with the Kurdistan Calendar API, please:

1. Check the [GitHub repository](https://github.com/kurdistan-calendar-api/kurdistan-calendar-api) for issues and discussions
2. Open a new issue if you encounter problems
3. Contact the maintainers via the repository 