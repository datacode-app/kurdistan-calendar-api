# Kurdistan Calendar API

An open-source API providing access to Kurdish holidays, historical events, and cultural celebrations. This project aims to be a reliable, community-maintained resource for Kurdish calendar data.

![Kurdistan Calendar API](https://placeholder-for-kurdistan-calendar-logo.com/logo.png)

## 🌟 Key Features

- **Publicly accessible API** – Anyone can fetch Kurdish holidays & events
- **Fast & lightweight** – Built using Python (FastAPI)
- **Simple JSON-based data storage** – No database required
- **Multi-language support** – English, Kurdish, Arabic, and Persian
- **Community-maintained** – All updates must be submitted via pull requests
- **Standardized structure** – Ensures consistent, machine-readable data
- **Versioned API** – Supports future updates without breaking existing integrations

## 📋 Quick Start

### Using the API

The API is publicly available at `https://api.calendar.krd/api/v1/`

```bash
# Get all holidays
curl https://api.calendar.krd/api/v1/holidays

# Get holidays for a specific year
curl https://api.calendar.krd/api/v1/holidays?year=2025

# Get today's holiday (if any)
curl https://api.calendar.krd/api/v1/holidays/today

# Get holiday for a specific date
curl https://api.calendar.krd/api/v1/holidays/2025-03-21

# Get holidays in Kurdish language
curl https://api.calendar.krd/api/v1/holidays?lang=ku
```

### Setting Up Development Environment

1. Clone the repository
   ```bash
   git clone https://github.com/kurdistan-calendar-api/kurdistan-calendar-api.git
   cd kurdistan-calendar-api
   ```

2. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

4. Run the API locally
   ```bash
   uvicorn api.main:app --reload
   ```

The API will be available at `http://localhost:8000`.

For detailed setup instructions, see the [Development Setup Guide](docs/development_setup.md).

## 📚 Documentation

The project includes comprehensive documentation to help you use and contribute to the API:

- [Project Context](docs/context.md): Overview of the project goals and principles
- [API Documentation](docs/api_documentation.md): Detailed API endpoints and usage
- [Technical Architecture](docs/technical_architecture.md): System design and implementation details
- [Data Schema](docs/data_schema.md): Structure of the holiday data
- [Contribution Guide](docs/contribution_guide.md): How to contribute to the project
- [Development Setup](docs/development_setup.md): Setting up your development environment
- [Deployment Guide](docs/deployment_guide.md): Deploying the API to production

## 🤝 Contributing

We welcome contributions from the community! There are several ways to contribute:

- **Add or update holiday data**
- **Improve documentation**
- **Fix bugs in the API implementation**
- **Add new features to the API**
- **Translate content**

All contributions are made through GitHub Pull Requests. See the [Contribution Guide](docs/contribution_guide.md) for detailed instructions.

## 📊 Project Status

The project is in active development. The core dataset (holidays.json) has been established, and the API implementation is underway.

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

For questions or support, please open an issue on GitHub or contact the maintainers directly through the repository.

---

*Kurdistan Calendar API is a community-driven project to preserve and celebrate Kurdish culture through technology.*
