import requests
import json
import sqlite3
import re
from datetime import datetime
import os

# Database connection
def get_db_connection():
    # Get absolute path to database
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/api_database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Fetch data from public-apis GitHub repository
def fetch_public_apis():
    url = "https://api.github.com/repos/public-apis/public-apis/contents/API.md"
    headers = {
        "Accept": "application/vnd.github.v3.raw"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        content = response.text
        
        # Parse the markdown content
        apis = parse_api_markdown(content)
        return apis
        
    except Exception as e:
        print(f"Error fetching public-apis: {e}")
        # Return sample data if GitHub API is unavailable
        return get_sample_apis()

# Get sample API data when GitHub API is unavailable
def get_sample_apis():
    print("Using sample API data...")
    return [
        {
            'name': 'OpenWeatherMap',
            'description': 'Weather data API',
            'category': 'Weather',
            'url': 'https://openweathermap.org/api',
            'auth_required': True,
            'api_key_instructions': 'Sign up at https://openweathermap.org/api to get an API key',
            'documentation_url': 'https://openweathermap.org/api',
            'rate_limit': '60 calls/minute',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        },
        {
            'name': 'NewsAPI',
            'description': 'News articles from around the world',
            'category': 'News',
            'url': 'https://newsapi.org/',
            'auth_required': True,
            'api_key_instructions': 'Register at https://newsapi.org/register to get an API key',
            'documentation_url': 'https://newsapi.org/docs',
            'rate_limit': '100 calls/day free tier',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        },
        {
            'name': 'IPGeolocation',
            'description': 'IP address geolocation',
            'category': 'Maps & Geocoding',
            'url': 'https://ipgeolocation.io/',
            'auth_required': True,
            'api_key_instructions': 'Create an account at https://ipgeolocation.io/ to get API key',
            'documentation_url': 'https://ipgeolocation.io/documentation',
            'rate_limit': '1000 calls/day free',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        },
        {
            'name': 'JSONPlaceholder',
            'description': 'Fake online REST API for testing',
            'category': 'Development Tools',
            'url': 'https://jsonplaceholder.typicode.com/',
            'auth_required': False,
            'api_key_instructions': 'No API key required',
            'documentation_url': 'https://jsonplaceholder.typicode.com/',
            'rate_limit': 'Unlimited',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        },
        {
            'name': 'NASA APIs',
            'description': 'NASA space data APIs',
            'category': 'Development Tools',
            'url': 'https://api.nasa.gov/',
            'auth_required': True,
            'api_key_instructions': 'Get API key at https://api.nasa.gov/',
            'documentation_url': 'https://api.nasa.gov/',
            'rate_limit': '1000 calls/hour',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        },
        {
            'name': 'GitHub API',
            'description': 'GitHub repository and user data',
            'category': 'Development Tools',
            'url': 'https://api.github.com/',
            'auth_required': True,
            'api_key_instructions': 'Create a personal access token at https://github.com/settings/tokens',
            'documentation_url': 'https://docs.github.com/en/rest',
            'rate_limit': '60 calls/hour unauthenticated',
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
    ]

# Parse API markdown content
def parse_api_markdown(content):
    apis = []
    current_category = None
    
    # Split content into lines
    lines = content.split('\n')
    
    for line in lines:
        # Check for category headers
        if line.startswith('### '):
            current_category = line[4:].strip()
            continue
            
        # Check for table rows
        if line.startswith('| ') and '|' in line:
            # Split the table row
            parts = [part.strip() for part in line.split('|')[1:-1]]
            
            if len(parts) >= 5 and parts[0] != 'API':  # Skip header row
                api_name = parts[0]
                api_description = parts[1]
                api_auth = parts[2]
                api_https = parts[3]
                api_cors = parts[4]
                api_link = parts[5] if len(parts) > 5 else ''
                
                # Clean up the data
                auth_required = api_auth.lower() != 'no'
                
                apis.append({
                    'name': api_name,
                    'description': api_description,
                    'category': current_category,
                    'url': api_link,
                    'auth_required': auth_required,
                    'api_key_instructions': f'Sign up at {api_link} to get an API key',
                    'documentation_url': api_link,
                    'rate_limit': 'Check documentation',
                    'created_at': datetime.now(),
                    'updated_at': datetime.now()
                })
    
    return apis

# Update database with new APIs
def update_database(apis):
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get existing API names
    c.execute("SELECT name FROM apis")
    existing_apis = {row['name'] for row in c.fetchall()}
    
    new_apis_count = 0
    updated_apis_count = 0
    
    for api in apis:
        if api['name'] in existing_apis:
            # Update existing API
            c.execute('''UPDATE apis SET 
                        description = ?,
                        category = ?,
                        url = ?,
                        auth_required = ?,
                        api_key_instructions = ?,
                        documentation_url = ?,
                        rate_limit = ?,
                        updated_at = ?
                        WHERE name = ?''',
                      (api['description'], api['category'], api['url'], 
                       api['auth_required'], api['api_key_instructions'],
                       api['documentation_url'], api['rate_limit'],
                       datetime.now(), api['name']))
            updated_apis_count += 1
        else:
            # Insert new API
            c.execute('''INSERT INTO apis 
                        (name, description, category, url, auth_required, 
                         api_key_instructions, documentation_url, rate_limit,
                         created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (api['name'], api['description'], api['category'], 
                       api['url'], api['auth_required'], api['api_key_instructions'],
                       api['documentation_url'], api['rate_limit'],
                       datetime.now(), datetime.now()))
            new_apis_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"Updated {updated_apis_count} APIs, added {new_apis_count} new APIs")
    return new_apis_count + updated_apis_count

# Update categories in database
def update_categories(apis):
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get existing categories
    c.execute("SELECT name FROM categories")
    existing_categories = {row['name'] for row in c.fetchall()}
    
    # Extract categories from APIs
    categories = set(api['category'] for api in apis if api['category'])
    
    new_categories_count = 0
    
    for category in categories:
        if category not in existing_categories:
            c.execute('''INSERT INTO categories (name, description) 
                        VALUES (?, ?)''',
                      (category, f'{category} related APIs'))
            new_categories_count += 1
    
    conn.commit()
    conn.close()
    
    print(f"Added {new_categories_count} new categories")
    return new_categories_count

# Main function
def main():
    print("Starting data collection...")
    
    # Fetch data from various sources
    public_apis = fetch_public_apis()
    
    if not public_apis:
        print("No APIs found. Exiting.")
        return
    
    # Update categories first
    update_categories(public_apis)
    
    # Update APIs
    updated_count = update_database(public_apis)
    
    print(f"Data collection completed. Total APIs processed: {updated_count}")

if __name__ == "__main__":
    main()