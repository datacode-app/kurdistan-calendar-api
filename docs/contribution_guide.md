# Contribution Guide

## Introduction

Thank you for your interest in contributing to the Kurdistan Calendar API! This guide will walk you through the process of contributing to the project, whether you're fixing a bug, adding a new feature, or contributing new holiday data.

## How to Contribute

There are several ways to contribute to the Kurdistan Calendar API:

1. **Add or update holiday data**
2. **Improve documentation**
3. **Fix bugs in the API implementation**
4. **Add new features to the API**
5. **Translate content**

All contributions are made through GitHub Pull Requests (PRs). This ensures proper review and maintains the quality of the project.

## Getting Started

### Setting Up Your Development Environment

1. **Fork the repository**:
   - Go to the [Kurdistan Calendar API repository](https://github.com/kurdistan-calendar-api/kurdistan-calendar-api)
   - Click the "Fork" button to create your own copy of the repository

2. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR-USERNAME/kurdistan-calendar-api.git
   cd kurdistan-calendar-api
   ```

3. **Set up the development environment**:
   ```bash
   # Create a virtual environment
   python -m venv venv
   
   # Activate the virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Create a new branch**:
   ```bash
   # For holiday data updates
   git checkout -b add-holiday-data
   
   # For bug fixes
   git checkout -b fix-issue-123
   
   # For features
   git checkout -b feature-calendar-export
   ```

## Contributing Holiday Data

The holiday data is stored in the `holidays.json` file at the root of the repository. This is the most common type of contribution.

### Holiday Data Structure

Each holiday entry in the `holidays.json` file follows this structure:

```json
{
  "date": "YYYY-MM-DD",
  "isHoliday": true/false,
  "event": {
    "en": "Event name in English",
    "ku": "Event name in Kurdish",
    "ar": "Event name in Arabic",
    "fa": "Event name in Persian/Farsi"
  },
  "note": {
    "en": "Additional notes in English",
    "ku": "Additional notes in Kurdish",
    "ar": "Additional notes in Arabic",
    "fa": "Additional notes in Persian/Farsi"
  },
  "quote": {
    "celebrity": "Name of the person being quoted",
    "quote": {
      "en": "Quote in English",
      "ku": "Quote in Kurdish",
      "ar": "Quote in Arabic",
      "fa": "Quote in Persian/Farsi"
    }
  }
}
```

Optional fields that can be included:
- `country`: The country where the holiday is observed (e.g., "Iraq", "Iran")
- `region`: The region where the holiday is observed (e.g., "Erbil", "South Kurdistan")

### Adding a New Holiday

To add a new holiday:

1. Open the `holidays.json` file
2. Add a new entry to the `holidays` array
3. Ensure your entry follows the structure described above
4. Make sure the dates are in `YYYY-MM-DD` format
5. Provide translations for at least English and Kurdish
6. Add the holiday in chronological order by date

### Updating an Existing Holiday

To update an existing holiday:

1. Find the holiday entry in the `holidays.json` file
2. Update the relevant fields
3. Make sure to maintain the same structure
4. Provide a clear explanation of your changes in the PR description

### Data Validation

Before submitting your changes, run the validation script to ensure your data follows the correct format:

```bash
python scripts/validate_data.py
```

This will check for:
- Valid date formats
- Required fields
- Proper JSON structure
- Duplicate entries

## Making a Pull Request

Once you've made your changes:

1. **Commit your changes**:
   ```bash
   git add holidays.json
   git commit -m "Add holiday: Kurdish Clothing Day"
   ```

2. **Push to your fork**:
   ```bash
   git push origin add-holiday-data
   ```

3. **Create a Pull Request**:
   - Go to your fork on GitHub
   - Click "Pull Request"
   - Ensure the base repository is the original repository and the base branch is `main`
   - Fill out the PR template with details about your changes
   - Click "Create Pull Request"

## PR Review Process

All PRs go through a review process:

1. **Automated checks**:
   - The CI/CD pipeline will run automated tests on your PR
   - These check for formatting, data validity, and other issues

2. **Manual review**:
   - A project maintainer will review your PR
   - They may request changes or clarification
   - For holiday data, they may verify the accuracy of the information

3. **Approval and merge**:
   - Once approved, a maintainer will merge your PR
   - Your contribution will be included in the next release

## Code Contributions

If you're contributing code to the API implementation:

1. Follow the [PEP 8](https://pep8.org/) style guide
2. Add tests for your code
3. Ensure all tests pass by running:
   ```bash
   pytest
   ```
4. Document your code with docstrings
5. Update any relevant documentation

## Documentation Contributions

Documentation is crucial for the project. To contribute to documentation:

1. Look for existing documentation in the `/docs` directory
2. Make your changes or add new documentation files
3. Use clear, concise language
4. Follow Markdown formatting conventions
5. Include examples where appropriate

## Translation Contributions

For translation contributions:

1. Ensure translations are accurate and culturally appropriate
2. If you're unsure about a translation, indicate this in your PR
3. It's better to leave a field empty than to provide an incorrect translation

## Attribution

All contributors are listed in the [CONTRIBUTORS.md](../CONTRIBUTORS.md) file. By contributing, you agree to be added to this list.

## Code of Conduct

Please note that this project follows a [Code of Conduct](../CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Questions and Support

If you have questions about contributing:

1. Check the [GitHub Discussions](https://github.com/kurdistan-calendar-api/kurdistan-calendar-api/discussions)
2. Open an issue for specific problems
3. Contact the maintainers via GitHub

Thank you for contributing to the Kurdistan Calendar API! 