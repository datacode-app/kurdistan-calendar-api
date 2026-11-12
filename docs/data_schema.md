# Data Schema Documentation

This document describes the structure of the holiday data used in the Kurdistan Calendar API.

## Overview

The holiday data is organized by year in separate JSON files, each containing an array of holiday entries representing significant dates in Kurdish history, culture, or tradition.

## File Location

```
data/years/{YEAR}.json
```

Example: `data/years/2025.json`

For historical events, a special file is used:

```
data/years/historical.json
```

## Schema Structure

### Root Object

```json
{
  "year": 2026,
  "status": "official",
  "sources": ["https://gov.krd/calendar-2026/"],
  "holidays": [Holiday]
}
```

- `year` (year files only) must match the file name; every entry must fall in that year.
- `status` is `official` (published by the KRG) or `projected` (estimated ahead of the official calendar).
- `sources` is an optional list of URLs the data was taken from.
- Entries are sorted by date. Several entries may share the same date.

### Holiday Object

Each holiday entry has the following structure:

```json
{
  "date": "YYYY-MM-DD",
  "kurdish_date": {
    "year": number,
    "month": string,
    "month_number": number,
    "month_ku": string,
    "day": number,
    "full_date": string,
    "full_date_latin": string
  },
  "isHoliday": boolean,
  "event": {
    "en": "string",
    "ku": "string",
    "ar": "string",
    "fa": "string"
  },
  "note": {
    "en": "string",
    "ku": "string",
    "ar": "string",
    "fa": "string"
  },
  "region": "bashur | bakur | rojhelat | rojava | all",
  "type": "historical | political | commemoration | cultural | religious | official",
  "tentative": "boolean (optional)",
  "image": "string (optional)"
}
```

## Field Descriptions

### Required Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `date` | string | Date in YYYY-MM-DD format | "2025-03-21" |
| `kurdish_date` | object | Date in Kurdish calendar format | see below |
| `isHoliday` | boolean | Whether this is an official holiday | true |
| `event` | object | Event name in multiple languages | see below |
| `region` | string | Region where the holiday is celebrated | "bashur" |
| `type` | string | Category of the event | "religious" |

### Kurdish Date Object

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `year` | number | Kurdish year (Gregorian year + 700 from Newroz, + 699 before it) | 2726 |
| `month` | string | Kurdish month name (Latin) | "Xakelew" |
| `month_number` | number | Month number, 1-12 | 1 |
| `month_ku` | string | Kurdish month name (Sorani) | "خاکەلێوە" |
| `day` | number | Day of the month | 1 |
| `full_date` | string | Full date in Sorani | "١ی خاکەلێوە ٢٧٢٦" |
| `full_date_latin` | string | Full date in Latin script | "1 Xakelew 2726" |

`kurdish_date` is always derived from `date`. Do not write it by hand: run
`python scripts/validate_data.py --fix` and it is filled in for you.

The calendar convention is: the year starts on Newroz (21 March); months 1-6 have
31 days, months 7-11 have 30 days, and Reşeme has 29 days (30 when it contains
29 February).

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

### Optional Fields

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| `note` | object | Additional information in multiple languages | see below |
| `tentative` | boolean | `true` when the date is an estimate (for example Islamic holidays awaiting moon sighting) | true |
| `image` | string | URL or path to an image related to the event | "https://example.com/nawroz.jpg" |

### Language Support

Both `event` and `note` objects support four languages:

| Language Code | Description |
|--------------|-------------|
| `en` | English |
| `ku` | Kurdish |
| `ar` | Arabic |
| `fa` | Persian |

### Region Values

The `region` field accepts the following values:

| Value | Description |
|-------|-------------|
| `bashur` | South Kurdistan (Iraqi Kurdistan) |
| `bakur` | North Kurdistan (Turkish Kurdistan) |
| `rojhelat` | East Kurdistan (Iranian Kurdistan) |
| `rojava` | West Kurdistan (Syrian Kurdistan) |
| `all` | All Kurdish regions |

### Event Type Values

The `type` field accepts the following values:

| Value | Description |
|-------|-------------|
| `historical` | Historical events (e.g., Republic of Mahabad foundation) |
| `political` | Political events (e.g., elections, referendums) |
| `commemoration` | Commemorative events (e.g., Halabja Memorial) |
| `cultural` | Cultural celebrations (e.g., National Kurdish Clothing Day) |
| `religious` | Religious holidays |
| `official` | Official government holidays |

## Example Entry

```json
{
  "date": "2025-03-21",
  "kurdish_date": {
    "year": 2325,
    "month": "Xakelew",
    "day": 1,
    "full_date": "١ی خاکەلێو ٢٣٢٥"
  },
  "isHoliday": true,
  "event": {
    "en": "Nawroz - Kurdish New Year",
    "ku": "نەورۆز - سەری ساڵی کوردی",
    "ar": "نوروز - رأس السنة الكردية",
    "fa": "نوروز - سال نو کردی"
  },
  "note": {
    "en": "Traditional celebration of spring and new year",
    "ku": "جەژنی بەهار و ساڵی نوێ",
    "ar": "احتفال تقليدي بالربيع والسنة الجديدة",
    "fa": "جشن سنتی بهار و سال نو"
  },
  "region": "all",
  "type": "cultural",
  "image": "https://example.com/images/nawroz2025.jpg"
}
```

## Historical Event Example

```json
{
  "date": "1946-01-22",
  "kurdish_date": {
    "year": 2645,
    "month": "Rêbendan",
    "day": 2,
    "full_date": "٢ی Rêbendan ٢٦٤٥"
  },
  "isHoliday": true,
  "event": {
    "en": "Republic of Mahabad Foundation Day",
    "ku": "ڕۆژی دامەزراندنی کۆماری مەهاباد",
    "ar": "يوم تأسيس جمهورية مهاباد",
    "fa": "روز تأسیس جمهوری مهاباد"
  },
  "note": {
    "en": "Establishment of the first modern Kurdish state known as the Republic of Mahabad",
    "ku": "دامەزراندنی یەکەم دەوڵەتی مۆدێرنی کوردی کە بە کۆماری مەهاباد ناسراوە",
    "ar": "تأسيس أول دولة كردية حديثة معروفة باسم جمهورية مهاباد",
    "fa": "تأسیس اولین دولت مدرن کردی معروف به جمهوری مهاباد"
  },
  "region": "rojhelat",
  "type": "historical"
}
```

## Validation Rules

1. **Date Format**
   - Must be a valid date in YYYY-MM-DD format
   - Year should match the JSON file name

2. **Kurdish Date**
   - Year must be calculated correctly (Gregorian year - ~700)
   - Month must be a valid Kurdish month name
   - Day must be between 1 and 31
   - Full date must be properly formatted in Kurdish

3. **Event Translations**
   - All language fields (`en`, `ku`, `ar`, `fa`) are required
   - Values cannot be empty strings

4. **Note Translations**
   - All language fields are optional
   - If provided, values cannot be empty strings

5. **Region**
   - Must be one of: "bashur", "bakur", "rojhelat", "rojava", "all"
   - Cannot be empty or null

6. **Image URL**
   - Optional field
   - If provided, must be a valid URL or file path
   - Should point to an accessible image resource

## Best Practices

1. **File Organization**
   - Each year should have its own JSON file
   - File names should match the Gregorian year (e.g., "2025.json")
   - Entries within each file should be ordered by date

2. **Language Content**
   - Use proper grammar and spelling in all languages
   - Maintain consistent terminology across entries
   - Provide accurate translations

3. **Notes**
   - Keep notes concise and relevant
   - Include historical context when appropriate
   - Maintain cultural sensitivity

4. **Images**
   - Use high-quality, relevant images
   - Ensure proper licensing and attribution
   - Optimize image sizes for web use

## Contributing

When adding or modifying holiday entries:

1. Add entries to the correct year file
2. Follow the schema structure exactly
3. Provide accurate translations in all required languages
4. Verify the historical accuracy of dates and events
5. Test the JSON file for valid syntax
6. Submit changes through pull requests

## Schema Version

Current Version: 3.0.0
Last Updated: 2024-03-19 