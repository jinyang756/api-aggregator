# Free API Hub - Deployment Guide

## Overview
This guide provides instructions on how to deploy the Free API Hub application.

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional, for cloning the repository)

## Installation Options

### Option 1: Using the ZIP Package
1. Download the `free-api-hub.zip` file

2. Extract the contents:
   ```bash
   unzip free-api-hub.zip
   cd api-aggregator
   ```

3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Start the application:
   ```bash
   ./start.sh
   ```

### Option 2: Using Docker (Recommended)
1. Install Docker and Docker Compose

2. Extract the ZIP file and navigate to the project directory:
   ```bash
   unzip free-api-hub.zip
   cd api-aggregator
   ```

3. Build and start the containers:
   ```bash
   docker-compose up -d
   ```

## Accessing the Application
Once the application is running, you can access it at:
- Web Interface: http://localhost:5000
- API Endpoint: http://localhost:5000/api/apis

## Features
- **API Discovery**: Browse through a curated list of free APIs
- **API Details**: View detailed information about each API, including how to get API keys
- **Search & Filter**: Find APIs by name, description, or category
- **Favorites**: Save your favorite APIs for quick access
- **Automatic Updates**: The application automatically updates the API database daily

## Technical Details
- **Frontend**: HTML, CSS, JavaScript with Tailwind CSS
- **Backend**: Python Flask
- **Database**: SQLite
- **Scheduling**: APScheduler for daily data updates

## Troubleshooting
### Common Issues
1. **Port 5000 is already in use**
   - Change the port in `docker-compose.yml` or `start.sh`

2. **Database connection errors**
   - Ensure the `data` directory exists and has proper permissions

3. **GitHub API access issues**
   - The application will automatically fall back to sample data if GitHub API is unavailable

## Support
For issues or feature requests, please contact the development team.