# Free API Hub

A comprehensive platform for discovering and using free APIs with detailed instructions on how to get API keys and start using them.

## Features

- **Curated API List**: Browse through a collection of free APIs across various categories
- **API Key Instructions**: Detailed guides on how to obtain API keys for each service
- **Search & Filter**: Find APIs by name, description, or category
- **Favorites**: Save your favorite APIs for quick access
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.9+ (for development)

### Installation

#### Using Docker (Recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/free-api-hub.git
cd free-api-hub

# Build and start the containers
docker-compose up -d

# The application will be available at http://localhost:5000
```

#### Local Development
```bash
# Clone the repository
git clone https://github.com/yourusername/free-api-hub.git
cd free-api-hub

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python -c "from backend.app import init_db; init_db()"

# Run the application
python backend/app.py

# The application will be available at http://localhost:5000
```

## API Categories

The platform includes APIs from the following categories:
- Weather
- Maps & Geocoding
- News
- AI & Machine Learning
- Social Media
- Finance
- Development Tools

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.