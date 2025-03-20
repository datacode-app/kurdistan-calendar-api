# Kurdistan Calendar API Roadmap and Tasks

This document outlines the planned development path and specific tasks for the Kurdistan Calendar API project. It serves as a roadmap for development and helps contributors identify areas where they can help.

## Recently Completed Tasks

- [x] **Data Schema Restructuring**
  - [x] Added Kurdish date field to holiday entries (year, month, day, full_date)
  - [x] Reorganized data into year-based JSON files
  - [x] Updated schema documentation with Kurdish calendar information

- [x] **API Implementation Updates**
  - [x] Modified API routes to handle the new year-based file structure
  - [x] Added region filtering capability to all endpoints 
  - [x] Added support for Kurdish date in API responses

- [x] **Documentation Updates**
  - [x] Updated API documentation with Kurdish date examples
  - [x] Documented Kurdish month names and corresponding Gregorian months
  - [x] Standardized error response formats
  
- [x] **Conversion Utility**
  - [x] Developed Gregorian to Kurdish date conversion function
  - [x] Created Kurdish to Gregorian date conversion function
  - [x] Added conversion endpoints to the API

- [x] **Data Validation and Integrity**
  - [x] Created automated validation script for Kurdish dates
  - [x] Implemented schema validation for all year-based JSON files
  - [x] Added GitHub Action to validate PRs containing data changes

- [x] **Data Expansion**
  - [x] Created 2023.json and 2024.json with full holiday data
  - [x] Create 2026.json with projected holidays
  - [x] Add significant historical dates (pre-2023)

- [x] **Enhanced Filtering Options**
  - [x] Implemented date range queries (from/to dates)
  - [x] Added holiday type filtering (historical, political, etc.)
  - [x] Added support for combined filters (region + type + date range)
  - [x] Created dedicated endpoint for date range queries

## Current High-Priority Tasks

### Phase 1: Core System Enhancements (Next 2 Weeks)

- [x] **Additional Data Expansion**
  - [x] Create 2026.json with projected holidays
  - [x] Add significant historical dates (pre-2023)
  - [ ] Add more regional-specific holidays

### Phase 2: API Improvements (3-4 Weeks)

- [x] **Enhanced Filtering Options**
  - [x] Implement date range queries (from/to dates)
  - [x] Add holiday type filtering (official, cultural, historical, religious)
  - [x] Support combined filters (region + type + date range)

- [ ] **Performance Optimization**
  - [ ] Implement caching layer (Redis or in-memory)
  - [ ] Add data preloading for common queries
  - [ ] Optimize response size with field selection

- [ ] **Calendar Integration**
  - [ ] Add iCalendar (.ics) export endpoint
  - [ ] Create Google Calendar integration option
  - [ ] Support for calendar subscription links

## Medium-Priority Tasks (Next 2-3 Months)

### Developer Experience

- [ ] **Client Libraries**
  - [ ] Create JavaScript/TypeScript client library
  - [ ] Develop Python client package
  - [ ] Create documentation for client library usage

- [ ] **Example Applications**
  - [ ] Build simple web calendar demo
  - [ ] Create mobile app example (React Native)
  - [ ] Develop widget examples for websites

- [ ] **Testing and Quality**
  - [ ] Increase unit test coverage to >80%
  - [ ] Add integration tests for all endpoints
  - [ ] Implement load testing strategy

### User Experience Improvements

- [ ] **Localization Enhancements**
  - [ ] Support Kurdish dialects (Sorani, Kurmanji)
  - [ ] Add Azeri language support
  - [ ] Improve multilingual documentation

- [ ] **Cultural Context**
  - [ ] Add brief historical context to significant events
  - [ ] Include links to reliable sources for each event
  - [ ] Add cultural significance indicators

## Long-Term Goals (3-6 Months)

### System Expansion

- [ ] **Advanced Features**
  - [ ] Implement webhook notifications for upcoming holidays
  - [ ] Create public API for community contributions
  - [ ] Develop visualization tools for historical timelines

- [ ] **Infrastructure**
  - [ ] Set up comprehensive monitoring
  - [ ] Implement analytics for API usage
  - [ ] Create deployment options (Docker, serverless)

### Community Growth

- [ ] **Outreach**
  - [ ] Create promotional materials for Kurdish developers
  - [ ] Develop documentation in Kurdish language
  - [ ] Establish contributor recognition system

- [ ] **Educational**
  - [ ] Create tutorials for API integration
  - [ ] Develop educational content about Kurdish calendar
  - [ ] Host webinars or workshops for integration

## Specific Technical Tasks

### Backend Development

1. **~~Date Conversion Utility (High Priority)~~** ✅
   - ~~Create utility functions in Python for converting between Gregorian and Kurdish dates~~
   - ~~Implement data validation for Kurdish date format~~
   - ~~Add unit tests for conversion edge cases~~

2. **API Expansion**
   - ~~Add new endpoint for date conversion (/api/v1/convert)~~ ✅
   - Create endpoint for calendar exports (/api/v1/calendar/export)
   - Implement search functionality for events (/api/v1/search)

3. **Performance Improvements**
   - Implement middleware for response caching
   - Optimize data loading for large date ranges
   - Add database option for larger datasets (MongoDB)

### Data Management

1. **Historical Data Collection**
   - Research and compile significant historical dates in Kurdish history
   - Validate dates with multiple sources
   - Add proper multilingual descriptions for each event

2. **Regional Variations**
   - Document regional differences in holiday celebrations
   - Add region-specific notes to major holidays
   - Include custom imagery for regional celebrations

3. **Calendar Structure**
   - ~~Research variations in Kurdish calendar systems~~ ✅
   - ~~Document differences between regions~~ ✅
   - ~~Implement support for alternative calendar systems~~ ✅

### Documentation and Resources

1. **Developer Guides**
   - Create step-by-step integration guide for web applications
   - Develop mobile application integration tutorials
   - Add code examples in multiple programming languages

2. **Cultural Context Documentation**
   - Create reference material about Kurdish calendar history
   - Document regional naming conventions for months
   - Add cultural significance explanations for holidays

## How to Contribute

If you'd like to work on any of these tasks:

1. Check if there's an existing GitHub issue for the task
2. If not, create a new issue describing what you plan to work on
3. Comment on the issue to express your interest
4. Follow the [contribution guide](contribution_guide.md) to submit your work

## Task Prioritization Criteria

Tasks are prioritized based on:

1. **Impact**: How much value the task adds for users
2. **Dependency**: Whether other features depend on it
3. **Complexity**: How difficult the implementation is
4. **Community Interest**: Level of community demand 