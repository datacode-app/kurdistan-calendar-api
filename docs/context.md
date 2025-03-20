# Kurdistan Calendar API - Project Context

## Overview
Kurdistan Calendar API is an open-source project providing a structured dataset of holidays, historical events, and cultural celebrations in Kurdistan. The project aims to offer developers easy access to these dates through a RESTful API, with multi-language support (English, Kurdish, Arabic, and Persian) and region-specific filtering capabilities.

## Core Principles
1. **Community-Maintained**: All data updates happen through GitHub pull requests, ensuring transparency and peer review.
2. **Data Accuracy**: Historical and cultural events in Kurdistan should be accurately represented.
3. **Fast & Lightweight**: The API is built to be performant and have minimal dependencies.
4. **Multi-language Support**: All content is available in multiple languages relevant to the region.
5. **Cultural Authenticity**: The API includes both Gregorian and Kurdish calendar dates.
6. **Regional Awareness**: Events are tagged by region (Bashur, Bakur, Rojhelat, Rojava).
7. **Open Source**: The project is freely available for use, modification, and distribution.

## Project Goals
1. Create a reliable source of data for Kurdish holidays and significant dates.
2. Provide an easy-to-use API for developers to integrate this data into applications.
3. Foster community participation in maintaining and expanding the dataset.
4. Preserve and promote Kurdish culture and history through technology.
5. Support both Gregorian and Kurdish calendar systems.
6. Facilitate region-specific calendar applications.

## Technical Approach
1. **Data Storage**: Year-based JSON files in the `data/years/` directory for improved organization and querying.
2. **API Implementation**: FastAPI for high performance and modern Python features.
3. **Contribution Workflow**: GitHub pull requests as the exclusive method for data updates.
4. **Validation**: Strict schema validation to maintain data integrity.
5. **Date Conversion**: Support for Kurdish date representation alongside Gregorian dates.
6. **Regional Filtering**: Ability to filter holidays by specific Kurdish regions.

## Current Status
The project has evolved from its initial phase to include:
1. A restructured data schema with year-based organization
2. Kurdish date fields in all holiday entries
3. Region-specific tagging for all events
4. API endpoints with filtering capabilities
5. Rate limiting for API stability
6. Comprehensive documentation

## Project Structure
- **/data/years/**: Directory containing year-based JSON files (e.g., 2025.json)
- **/api/**: FastAPI implementation with routes, core functionality, and utilities
- **/docs/**: Project documentation including API references and schema definitions
- **/tests/**: Test suite for data validation and API functionality

## Data Schema
Each holiday entry in our dataset now includes:
- Gregorian date information
- Kurdish date (year, month, day, full date in Kurdish)
- Event names in multiple languages
- Notes and descriptions
- Region specification
- Optional image URL

## Maintainers
This project is maintained by the Kurdish developer community. All contributors are acknowledged in the CONTRIBUTORS.md file. 