# Technical Architecture

## System Overview
The Kurdistan Calendar API is designed as a lightweight, read-only REST API that serves holiday and event data from a static JSON file. The system is built with simplicity and performance in mind, avoiding the need for a database by leveraging file-based storage.

## Architecture Components

### 1. Data Storage
- **holidays.json**: A structured JSON file containing all holiday and event data.
- **Format**: Each entry follows a strict schema ensuring consistency.
- **Updates**: Managed exclusively through GitHub pull requests to maintain data integrity.

### 2. API Layer
- **Framework**: FastAPI (Python)
- **Role**: Provides RESTful endpoints to query the holiday data.
- **Features**:
  - Automatic data loading and caching
  - Query filtering (date, year, region, etc.)
  - Language selection
  - Response formatting
  - Input validation

### 3. Validation Layer
- **Purpose**: Ensures data integrity and adherence to schema.
- **Implementation**: Pydantic models for strict type checking and validation.
- **Usage**: Applied during:
  - API runtime (for request validation)
  - CI/CD pipeline (for PR validation)

### 4. Documentation
- **API Documentation**: Auto-generated via FastAPI's built-in Swagger/OpenAPI support.
- **Project Documentation**: Markdown files in the `/docs` directory.

## Data Flow

1. **Data Loading**:
   - On application startup, the API loads the holidays.json file into memory.
   - Data is parsed and validated against the defined schema.
   - An in-memory index is created for efficient querying.

2. **Request Processing**:
   - Client sends HTTP request to API endpoint.
   - FastAPI parses and validates request parameters.
   - Query is executed against the in-memory data.
   - Results are filtered and formatted according to request parameters.
   - Response is returned in JSON format.

3. **Data Updates**:
   - Developer creates a fork of the repository.
   - Developer makes changes to holidays.json in their fork.
   - Developer submits a pull request with their changes.
   - Automated tests validate the changes against the schema.
   - Maintainers review the PR for accuracy and approve if valid.
   - Changes are merged into the main branch.
   - Upon deployment, the API reloads with the updated data.

## API Design

### Endpoints
- `GET /api/v1/holidays`: Retrieve all holidays (with optional filters)
- `GET /api/v1/holidays/today`: Get today's holiday (if any)
- `GET /api/v1/holidays/{date}`: Get holidays for a specific date

### Query Parameters
- `year`: Filter by year (e.g., `?year=2025`)
- `month`: Filter by month (e.g., `?month=3`)
- `day`: Filter by day (e.g., `?day=21`)
- `region`: Filter by region (e.g., `?region=Erbil`)
- `lang`: Specify response language (e.g., `?lang=ku`, defaults to English)
- `is_holiday`: Filter by holiday status (e.g., `?is_holiday=true`)

### Response Format
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

## Performance Considerations

1. **Memory Caching**:
   - The entire dataset is loaded into memory at startup.
   - In-memory indices are created for common query patterns.
   - This approach eliminates disk I/O during request processing.

2. **Response Size Optimization**:
   - Language filtering to reduce payload size.
   - Pagination for large result sets.
   - Optional fields to allow clients to request only needed data.

3. **Deployment Options**:
   - Containerized deployment (Docker) for consistent environments.
   - Static file serving for the holidays.json to reduce API load.
   - CDN integration for high-traffic scenarios.

## Security Considerations

1. **Read-Only API**:
   - No endpoints for modifying data, eliminating many attack vectors.
   - Data updates only through the GitHub PR process.

2. **Input Validation**:
   - Strict validation of all query parameters.
   - Path parameter sanitization.

3. **Rate Limiting**:
   - Implementation of rate limiting to prevent abuse.
   - Configurable limits based on deployment requirements.

4. **CORS Policy**:
   - Configurable CORS settings for different deployment scenarios.
   - Default to permissive policy to allow wide integration.

## Monitoring and Logging

1. **Request Logging**:
   - Log all API requests for monitoring and debugging.
   - Optional detailed logging for troubleshooting.

2. **Error Tracking**:
   - Comprehensive error handling and reporting.
   - Structured error responses for API consumers.

3. **Performance Metrics**:
   - Track response times and request counts.
   - Monitor memory usage and system health.

## Future Extensibility

1. **API Versioning**:
   - Path-based versioning strategy (`/api/v1/`, `/api/v2/`, etc.).
   - Backward compatibility guarantees for published versions.

2. **Data Schema Evolution**:
   - Forward-compatible schema design.
   - Clear documentation of schema changes between versions.

3. **Integration Options**:
   - Calendar export formats (iCal, Google Calendar).
   - Webhook notifications for specific dates.
   - SDK development for common programming languages. 