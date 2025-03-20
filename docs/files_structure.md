# Files Structure Documentation

This document outlines the organization and purpose of files and directories in the Kurdistan Calendar API project.

## Project Root

```
kurdistan-calendar-api/
├── .git/                       # Git repository data
├── .github/                    # GitHub configuration files
│   ├── workflows/              # GitHub Actions workflows
│   │   ├── validate-data.yml   # Workflow to validate holiday data in PRs
│   │   └── deploy.yml          # Deployment workflow
│   └── ISSUE_TEMPLATE/         # Templates for GitHub issues
├── api/                        # API implementation
├── data/                       # Data storage directory
│   └── holidays.json           # Core data file containing all holidays
├── docs/                       # Project documentation
├── scripts/                    # Utility scripts
├── tests/                      # Test suite
├── .gitignore                  # Git ignore patterns
├── LICENSE                     # Project license (MIT)
├── README.md                   # Project overview
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
└── Dockerfile                  # Docker configuration
```

## API Directory

```
api/
├── __init__.py                 # Package initialization
├── main.py                     # FastAPI application entry point
├── models.py                   # Pydantic models for data validation
├── config.py                   # Configuration settings
├── routes/                     # API route handlers
│   ├── __init__.py             # Package initialization
│   ├── holidays.py             # Holiday routes
│   └── calendar.py             # Calendar export routes
└── utils/                      # Utility functions
    ├── __init__.py             # Package initialization
    ├── data_loader.py          # Functions to load and process holiday data
    ├── filters.py              # Query filtering functions
    └── date_utils.py           # Date manipulation utilities
```

## Documentation Directory

```
docs/
├── context.md                  # Project context and overview
├── technical_architecture.md   # System design and implementation details
├── api_documentation.md        # Detailed API documentation
├── data_schema.md              # Schema for holiday data
├── contribution_guide.md       # How to contribute to the project
├── development_setup.md        # Setting up development environment
├── deployment_guide.md         # Deploying to production
├── files_structure.md          # This file - project organization
├── tasks.md                    # Planned tasks and improvements
└── changes.log                 # Record of significant changes
```

## Scripts Directory

```
scripts/
├── validate_data.py            # Script to validate holidays.json
├── generate_ical.py            # Script to generate iCalendar files
└── data_migration.py           # Script for data format migrations
```

## Tests Directory

```
tests/
├── __init__.py                 # Package initialization
├── conftest.py                 # Pytest configuration
├── test_api.py                 # API endpoint tests
├── test_models.py              # Data model tests
├── test_data.py                # Data validation tests
└── test_utils.py               # Utility function tests
```

## File Descriptions

### Core Files

- **data/holidays.json**: The primary data file containing all holiday information. This is the only file that most contributors will need to modify. It follows a strict schema defined in the data schema documentation.

- **main.py**: The entry point for the FastAPI application. It initializes the API, loads the holiday data, and registers routes.

- **models.py**: Contains Pydantic models that define the data schema and provide validation. These models ensure that the API responses conform to the expected format.

### Configuration Files

- **config.py**: Contains configuration settings for the API, including environment variables for deployment settings, rate limits, and CORS configuration.

- **requirements.txt**: Lists the production dependencies required to run the API.

- **requirements-dev.txt**: Lists additional dependencies needed for development and testing.

- **Dockerfile**: Defines the Docker container configuration for deployment.

### Documentation Files

See the Documentation Directory section above for details on documentation files.

## File Relationships

1. **Data Flow**:
   - `data/holidays.json` → `data_loader.py` → `models.py` → API routes

2. **Request Processing**:
   - Client Request → `main.py` → Route handlers → `filters.py` → Response

3. **Validation Flow**:
   - PR with data changes → GitHub Actions → `validate_data.py` → Validation results

## Best Practices for File Organization

1. **Adding New Routes**:
   - Create new route handlers in the `api/routes/` directory
   - Register the routes in `main.py`

2. **Adding Utility Functions**:
   - Add related functions to existing utility modules or create new ones in `api/utils/`
   - Import these utilities in the appropriate route handlers

3. **Documentation Updates**:
   - When adding new features, update the relevant documentation files
   - Keep the API documentation in sync with the implementation

4. **Test Coverage**:
   - Add tests for new functionality in the appropriate test files
   - Ensure all routes and utility functions have corresponding tests 