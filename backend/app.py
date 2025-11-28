from flask import Flask, render_template, jsonify, request
import sqlite3
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

# 生产环境配置
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.environ.get('FLASK_ENV') != 'production'
app.config['JSON_SORT_KEYS'] = False

# 数据库初始化
def init_db():
    # Get absolute path to database
    import os
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/api_database.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # 创建API表
    c.execute('''CREATE TABLE IF NOT EXISTS apis
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 description TEXT,
                 category TEXT,
                 url TEXT,
                 auth_required BOOLEAN,
                 api_key_instructions TEXT,
                 documentation_url TEXT,
                 rate_limit TEXT,
                 created_at TIMESTAMP,
                 updated_at TIMESTAMP)''')
    
    # 创建分类表
    c.execute('''CREATE TABLE IF NOT EXISTS categories
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT NOT NULL,
                 description TEXT)''')
    
    # 创建用户收藏表
    c.execute('''CREATE TABLE IF NOT EXISTS favorites
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 user_id TEXT,
                 api_id INTEGER,
                 FOREIGN KEY(api_id) REFERENCES apis(id))''')
    
    conn.commit()
    conn.close()

# 初始化数据库
init_db()

# 首页
@app.route('/')
def index():
    return render_template('index.html')

# API列表API
@app.route('/api/apis')
def get_apis():
    category = request.args.get('category')
    search = request.args.get('search')
    
    import os
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/api_database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    query = "SELECT * FROM apis WHERE 1=1"
    params = []
    
    if category:
        query += " AND category = ?"
        params.append(category)
    
    if search:
        query += " AND (name LIKE ? OR description LIKE ?)"
        params.append(f'%{search}%')
        params.append(f'%{search}%')
    
    query += " ORDER BY name"
    
    c.execute(query, params)
    apis = [dict(row) for row in c.fetchall()]
    
    conn.close()
    return jsonify(apis)

# API分类列表
@app.route('/api/categories')
def get_categories():
    import os
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/api_database.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM categories ORDER BY name")
    categories = [dict(row) for row in c.fetchall()]
    
    conn.close()
    return jsonify(categories)

# API详情
@app.route('/api/apis/<int:api_id>')
def get_api_detail(api_id):
    conn = sqlite3.connect('../data/api_database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM apis WHERE id = ?", (api_id,))
    api = dict(c.fetchone()) if c.fetchone() else None
    
    conn.close()
    return jsonify(api)

# 添加收藏
@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    data = request.json
    user_id = data.get('user_id')
    api_id = data.get('api_id')
    
    import os
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/api_database.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute("INSERT INTO favorites (user_id, api_id) VALUES (?, ?)", (user_id, api_id))
    conn.commit()
    
    favorite_id = c.lastrowid
    conn.close()
    
    return jsonify({'success': True, 'favorite_id': favorite_id})

# 获取用户收藏
@app.route('/api/favorites/<user_id>')
def get_favorites(user_id):
    conn = sqlite3.connect('../data/api_database.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute('''SELECT a.* FROM apis a
                 JOIN favorites f ON a.id = f.api_id
                 WHERE f.user_id = ?''', (user_id,))
    
    favorites = [dict(row) for row in c.fetchall()]
    conn.close()
    
    return jsonify(favorites)

# 数据库初始化脚本
@app.route('/api/init_sample_data')
def init_sample_data():
    import os
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data/api_database.db')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # 清空现有数据
    c.execute("DELETE FROM apis")
    c.execute("DELETE FROM categories")
    c.execute("DELETE FROM favorites")
    
    # 插入分类数据
    categories = [
        ('Weather', 'Weather and meteorological data APIs'),
        ('Maps & Geocoding', 'Map services and geolocation APIs'),
        ('News', 'News and media APIs'),
        ('AI & Machine Learning', 'Artificial intelligence and ML APIs'),
        ('Social Media', 'Social networking APIs'),
        ('Finance', 'Financial data and services APIs'),
        ('Development Tools', 'Developer tools and utilities APIs')
    ]
    
    c.executemany("INSERT INTO categories (name, description) VALUES (?, ?)", categories)
    
    # 插入示例API数据
    sample_apis = [
        ('OpenWeatherMap', 'Weather data API', 'Weather', 'https://openweathermap.org/api', True, 
         'Sign up at https://openweathermap.org/api to get an API key', 
         'https://openweathermap.org/api', '60 calls/minute', datetime.now(), datetime.now()),
        
        ('NewsAPI', 'News articles from around the world', 'News', 'https://newsapi.org/', True,
         'Register at https://newsapi.org/register to get an API key',
         'https://newsapi.org/docs', '100 calls/day free tier', datetime.now(), datetime.now()),
        
        ('IPGeolocation', 'IP address geolocation', 'Maps & Geocoding', 'https://ipgeolocation.io/', True,
         'Create an account at https://ipgeolocation.io/ to get API key',
         'https://ipgeolocation.io/documentation', '1000 calls/day free', datetime.now(), datetime.now()),
        
        ('JSONPlaceholder', 'Fake online REST API for testing', 'Development Tools', 'https://jsonplaceholder.typicode.com/', False,
         'No API key required', 'https://jsonplaceholder.typicode.com/', 'Unlimited', datetime.now(), datetime.now()),
        
        ('NASA APIs', 'NASA space data APIs', 'Development Tools', 'https://api.nasa.gov/', True,
         'Get API key at https://api.nasa.gov/', 'https://api.nasa.gov/', '1000 calls/hour', datetime.now(), datetime.now()),
        
        ('GitHub API', 'GitHub repository and user data', 'Development Tools', 'https://api.github.com/', True,
         'Create a personal access token at https://github.com/settings/tokens',
         'https://docs.github.com/en/rest', '60 calls/hour unauthenticated', datetime.now(), datetime.now())
    ]
    
    c.executemany('''INSERT INTO apis (name, description, category, url, auth_required, 
                     api_key_instructions, documentation_url, rate_limit, created_at, updated_at)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', sample_apis)
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Sample data initialized'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)