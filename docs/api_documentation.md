# API Documentation

## Introduction

The Kurdistan Calendar API provides access to a comprehensive dataset of Kurdish holidays, cultural events, and historical dates. This documentation explains how to interact with the API endpoints, the available query parameters, and the expected response formats.

## Base URL

```
https://api.kurdistancalendar.org/api/v1
```

All endpoints described in this documentation are relative to this base URL.

## Authentication

The API is publicly accessible and does not require authentication.

## Rate Limiting

To ensure service availability for all users, the API implements rate limiting:

- 100 requests per minute per IP address
- 5,000 requests per day per IP address

If you exceed these limits, you will receive a `429 Too Many Requests` response.

## API Versioning

The API uses path-based versioning:

- `/api/v1/` - Current stable version

Future versions will use incrementing version numbers (`/api/v2/`, etc.) and will be announced with ample notice.

## Common HTTP Status Codes

| Status Code | Description |
|-------------|-------------|
| 200 | OK - The request was successful |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - The requested resource does not exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Something went wrong on our end |

## Response Format

All API responses are returned in JSON format with the following structure:

```json
{
  "status": "success",
  "count": 1,
  "data": [
    {
      // Holiday data
    }
  ]
}
```

- `status`: Indicates if the request was successful
- `count`: The number of holiday entries returned
- `data`: An array of holiday objects

## Endpoints

### Get All Holidays

```
GET /holidays
```

Returns all holidays in the dataset.

#### Query Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| year | integer | Filter by year | `?year=2025` |
| month | integer | Filter by month (1-12) | `?month=3` |
| day | integer | Filter by day (1-31) | `?day=21` |
| region | string | Filter by region | `?region=Erbil` |
| is_holiday | boolean | Filter by holiday status | `?is_holiday=true` |
| lang | string | Preferred language for response (en, ku, ar, fa) | `?lang=ku` |
| limit | integer | Number of results to return (default: 100, max: 500) | `?limit=50` |
| offset | integer | Number of results to skip (default: 0) | `?offset=50` |

#### Example Request

```
GET /holidays?year=2025&month=3&is_holiday=true
```

#### Example Response

```json
{
  "status": "success",
  "count": 2,
  "data": [
    {
      "date": "2025-03-21",
      "isHoliday": true,
      "event": {
        "en": "Nawroz Kurdish New Year",
        "ku": "نەورۆز، ساڵی نوێی کوردی",
        "ar": "نوروز، السنة الكردية الجديدة",
        "fa": "نوروز، سال نو کردی"
      },
      "note": {
        "en": "Traditional celebration of spring and new year",
        "ku": "جەژنی بەهار و ساڵی نوێ",
        "ar": "احتفال تقليدي بالربيع والسنة الجديدة",
        "fa": "جشن سنتی بهار و سال نو"
      },
      "quote": {
        "celebrity": "Sherko Bekas",
        "quote": {
          "en": "In every dawn, there is a promise of renewal.",
          "ku": "لە هەموو سپیدانێکدا، پێشوازی تازەبوون هەیە.",
          "ar": "في كل فجر، هناك وعد بالتجدد.",
          "fa": "در هر سپیده‌دم، وعده‌ای برای تجدید وجود دارد."
        }
      }
    },
    {
      "date": "2025-03-11",
      "isHoliday": true,
      "event": {
        "en": "Anniversary of 11 March Agreement (1970)",
        "ku": "ساڵیادی ڕێکەوتننامەی ١١ ی ئازار (١٩٧٠)",
        "ar": "ذكرى اتفاقية 11 آذار (1970)",
        "fa": "سالگرد توافقنامه ۱۱ مارس (۱۹۷۰)"
      },
      "note": {
        "en": "",
        "ku": "",
        "ar": "",
        "fa": ""
      },
      "quote": {
        "celebrity": "Jalal Talabani",
        "quote": {
          "en": "Dialogue and understanding build the bridges to our future.",
          "ku": "ڕێکەوت و تێگەیشتن پلەکانمان بۆ داهاتی ئێمە دروست دەکەن.",
          "ar": "الحوار والتفاهم يبنيان جسور مستقبلنا.",
          "fa": "گفتگو و تفاهم پل‌های آینده ما را می‌سازد."
        }
      }
    }
  ]
}
```

### Get Today's Holiday

```
GET /holidays/today
```

Returns any holidays occurring on the current date.

#### Query Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| lang | string | Preferred language for response (en, ku, ar, fa) | `?lang=ku` |

#### Example Response

```json
{
  "status": "success",
  "count": 1,
  "data": [
    {
      "date": "2025-03-21",
      "isHoliday": true,
      "event": {
        "en": "Nawroz Kurdish New Year",
        "ku": "نەورۆز، ساڵی نوێی کوردی",
        "ar": "نوروز، السنة الكردية الجديدة",
        "fa": "نوروز، سال نو کردی"
      },
      "note": {
        "en": "Traditional celebration of spring and new year",
        "ku": "جەژنی بەهار و ساڵی نوێ",
        "ar": "احتفال تقليدي بالربيع والسنة الجديدة",
        "fa": "جشن سنتی بهار و سال نو"
      },
      "quote": {
        "celebrity": "Sherko Bekas",
        "quote": {
          "en": "In every dawn, there is a promise of renewal.",
          "ku": "لە هەموو سپیدانێکدا، پێشوازی تازەبوون هەیە.",
          "ar": "في كل فجر، هناك وعد بالتجدد.",
          "fa": "در هر سپیده‌دم، وعده‌ای برای تجدید وجود دارد."
        }
      }
    }
  ]
}
```

If there are no holidays today, the response will include an empty data array:

```json
{
  "status": "success",
  "count": 0,
  "data": []
}
```

### Get Holiday by Date

```
GET /holidays/{date}
```

Returns any holidays occurring on the specified date.

#### Path Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| date | string | Date in YYYY-MM-DD format | `/holidays/2025-03-21` |

#### Query Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| lang | string | Preferred language for response (en, ku, ar, fa) | `?lang=ku` |

#### Example Request

```
GET /holidays/2025-03-21
```

#### Example Response

```json
{
  "status": "success",
  "count": 1,
  "data": [
    {
      "date": "2025-03-21",
      "isHoliday": true,
      "event": {
        "en": "Nawroz Kurdish New Year",
        "ku": "نەورۆز، ساڵی نوێی کوردی",
        "ar": "نوروز، السنة الكردية الجديدة",
        "fa": "نوروز، سال نو کردی"
      },
      "note": {
        "en": "Traditional celebration of spring and new year",
        "ku": "جەژنی بەهار و ساڵی نوێ",
        "ar": "احتفال تقليدي بالربيع والسنة الجديدة",
        "fa": "جشن سنتی بهار و سال نو"
      },
      "quote": {
        "celebrity": "Sherko Bekas",
        "quote": {
          "en": "In every dawn, there is a promise of renewal.",
          "ku": "لە هەموو سپیدانێکدا، پێشوازی تازەبوون هەیە.",
          "ar": "في كل فجر، هناك وعد بالتجدد.",
          "fa": "در هر سپیده‌دم، وعده‌ای برای تجدید وجود دارد."
        }
      }
    }
  ]
}
```

## Language Support

The API supports the following languages:

- English (`en`) - Default
- Kurdish (`ku`)
- Arabic (`ar`)
- Persian/Farsi (`fa`)

You can specify your preferred language using the `lang` query parameter. This affects two aspects of the response:

1. If a specific language is requested, only that language's content will be returned in the `event`, `note`, and `quote` objects.
2. If no language is specified, all available translations will be returned.

### Example with Language Filter

Request:
```
GET /holidays/2025-03-21?lang=ku
```

Response:
```json
{
  "status": "success",
  "count": 1,
  "data": [
    {
      "date": "2025-03-21",
      "isHoliday": true,
      "event": "نەورۆز، ساڵی نوێی کوردی",
      "note": "جەژنی بەهار و ساڵی نوێ",
      "quote": {
        "celebrity": "Sherko Bekas",
        "quote": "لە هەموو سپیدانێکدا، پێشوازی تازەبوون هەیە."
      }
    }
  ]
}
```

## Error Handling

In case of an error, the API will return a JSON response with details about the error:

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

## Webhook Notifications (Coming Soon)

In future versions, the API will support webhook notifications for upcoming holidays:

```
POST /webhooks/register
```

Stay tuned for updates on this feature.

## Support

If you have any questions or need help integrating with the Kurdistan Calendar API, please:

1. Check the [GitHub repository](https://github.com/kurdistan-calendar-api/kurdistan-calendar-api) for issues and discussions
2. Open a new issue if you encounter problems
3. Contact the maintainers via the repository 