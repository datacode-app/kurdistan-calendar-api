# Development Setup Guide

## Introduction

This guide will help you set up your development environment for the Kurdistan Calendar API project. Follow these steps to get the project running locally.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+**: Required for the FastAPI backend
- **Git**: For version control
- **A text editor or IDE**: VS Code, PyCharm, or any editor of your choice

## Setting Up the Development Environment

### 1. Clone the Repository

```bash
# Clone the repository
git clone https://github.com/kurdistan-calendar-api/kurdistan-calendar-api.git

# Navigate to the project directory
cd kurdistan-calendar-api
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to isolate the project dependencies:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install the project dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt
```

The `requirements.txt` file includes:

- FastAPI: Web framework for building APIs
- Uvicorn: ASGI server for FastAPI
- Pydantic: Data validation and settings management
- python-dateutil: For working with dates and times
- python-multipart: For handling form data
- pytest: For testing

The `requirements-dev.txt` file includes additional tools for development:

- Black: Code formatter
- isort: Import optimizer
- flake8: Style guide enforcer
- mypy: Static type checker
- pytest-cov: Test coverage reporter

### 4. Setup Pre-commit Hooks (Optional but Recommended)

Pre-commit hooks help ensure code quality before committing changes:

```bash
# Install pre-commit
pip install pre-commit

# Set up the git hooks
pre-commit install
```

## Project Structure

The project is organized as follows:

```
kurdistan-calendar-api/
│
├── api/                 # API implementation
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── models.py        # Pydantic models for data validation
│   ├── routes/          # API route handlers
│   └── utils/           # Utility functions
│
├── docs/                # Project documentation
│
├── scripts/             # Utility scripts
│   ├── validate_data.py # Script to validate holiday data
│   └── generate_ical.py # Script to generate iCalendar files
│
├── tests/               # Test suite
│   ├── __init__.py
│   ├── test_api.py      # API tests
│   └── test_data.py     # Data validation tests
│
├── holidays.json        # Core data file
├── requirements.txt     # Production dependencies
├── requirements-dev.txt # Development dependencies
├── .pre-commit-config.yaml # Pre-commit hooks configuration
└── README.md            # Project overview
```

## Running the API Locally

To start the API server locally:

```bash
# Make sure your virtual environment is activated
# Then run:
uvicorn api.main:app --reload
```

This will start the development server with hot reloading at `http://localhost:8000`.

## API Documentation

Once the server is running, you can access the automatically generated API documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Running Tests

To run the test suite:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=api tests/
```

## Data Validation

To validate the `holidays.json` file:

```bash
python scripts/validate_data.py
```

This will check the data against the schema and report any issues.

## Code Formatting

To format your code according to the project's style guidelines:

```bash
# Format with Black
black .

# Sort imports
isort .

# Run linting
flake8
```

## Common Development Tasks

### Adding a New Endpoint

1. Define the route in the appropriate file in `api/routes/`
2. If needed, add new models in `api/models.py`
3. Add tests in the `tests/` directory

### Modifying the Data Schema

1. Update the schema definition in `api/models.py`
2. Update the validation script in `scripts/validate_data.py`
3. Update the documentation in `docs/data_schema.md`

### Adding New Features

1. Discuss the feature in a GitHub issue first
2. Implement the feature in a new branch
3. Add tests for the new functionality
4. Update documentation as needed
5. Submit a pull request

## Debugging Tips

### FastAPI Debug Mode

FastAPI includes detailed error information when running in debug mode:

```bash
uvicorn api.main:app --reload --debug
```

### Logging

The API uses Python's standard logging module. You can adjust the log level in `api/main.py`.

## Deployment Considerations

While developing locally, keep in mind these considerations for deployment:

- Set proper CORS settings in `api/main.py`
- Configure rate limiting
- Set up proper error handling and monitoring
- Consider environment-specific configuration

## Need Help?

If you encounter any issues during setup:

1. Check the [GitHub issues](https://github.com/kurdistan-calendar-api/kurdistan-calendar-api/issues) to see if it's a known problem
2. Open a new issue if needed
3. Reach out to the maintainers

Happy coding! 