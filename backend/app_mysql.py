"""
Free API Hub - MySQL 版本
支持 SQLite 本地开发和 MySQL 生产环境
"""

from flask import Flask, render_template, jsonify, request
import os
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from backend.database import get_database

app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend/templates')

# 应用配置
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['DEBUG'] = os.environ.get('FLASK_ENV') != 'production'
app.config['JSON_SORT_KEYS'] = False

# 初始化数据库
db = get_database()
db.init_tables()


# ============ 路由 ============

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')


@app.route('/api/apis')
def get_apis():
    """获取 API 列表（支持分类和搜索）"""
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = "SELECT * FROM apis WHERE 1=1"
    params = []
    
    if category:
        query += " AND category = %s"
        params.append(category)
    
    if search:
        query += " AND (name LIKE %s OR description LIKE %s)"
        params.append(f'%{search}%')
        params.append(f'%{search}%')
    
    query += " ORDER BY name"
    
    apis = db.fetch_all(query, tuple(params))
    return jsonify(apis)


@app.route('/api/categories')
def get_categories():
    """获取所有分类"""
    categories = db.fetch_all("SELECT * FROM categories ORDER BY name")
    return jsonify(categories)


@app.route('/api/apis/<int:api_id>')
def get_api_detail(api_id):
    """获取单个 API 详情"""
    api = db.fetch_one("SELECT * FROM apis WHERE id = %s", (api_id,))
    return jsonify(api) if api else jsonify({'error': 'API not found'}), 404


@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    """添加收藏"""
    data = request.json
    user_id = data.get('user_id')
    api_id = data.get('api_id')
    
    if not user_id or not api_id:
        return jsonify({'error': 'Missing user_id or api_id'}), 400
    
    try:
        favorite_id = db.execute(
            "INSERT INTO favorites (user_id, api_id) VALUES (%s, %s)",
            (user_id, api_id)
        )
        return jsonify({'success': True, 'favorite_id': favorite_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/favorites/<user_id>')
def get_favorites(user_id):
    """获取用户收藏"""
    query = '''SELECT a.* FROM apis a
              JOIN favorites f ON a.id = f.api_id
              WHERE f.user_id = %s'''
    favorites = db.fetch_all(query, (user_id,))
    return jsonify(favorites)


@app.route('/api/init_sample_data')
def init_sample_data():
    """初始化示例数据"""
    try:
        # 清空现有数据
        db.execute("DELETE FROM favorites")
        db.execute("DELETE FROM apis")
        db.execute("DELETE FROM categories")
        
        # 插入分类
        categories = [
            ('Weather', 'Weather and meteorological data APIs'),
            ('Maps & Geocoding', 'Map services and geolocation APIs'),
            ('News', 'News and media APIs'),
            ('AI & Machine Learning', 'Artificial intelligence and ML APIs'),
            ('Social Media', 'Social networking APIs'),
            ('Finance', 'Financial data and services APIs'),
            ('Development Tools', 'Developer tools and utilities APIs')
        ]
        
        db.execute_many(
            "INSERT INTO categories (name, description) VALUES (%s, %s)",
            categories
        )
        
        # 插入示例 API
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
            
            ('JSONPlaceholder', 'Fake online REST API for testing', 'Development Tools',
             'https://jsonplaceholder.typicode.com/', False,
             'No API key required', 'https://jsonplaceholder.typicode.com/', 'Unlimited',
             datetime.now(), datetime.now()),
            
            ('NASA APIs', 'NASA space data APIs', 'Development Tools', 'https://api.nasa.gov/', True,
             'Get API key at https://api.nasa.gov/', 'https://api.nasa.gov/', '1000 calls/hour',
             datetime.now(), datetime.now()),
            
            ('GitHub API', 'GitHub repository and user data', 'Development Tools',
             'https://api.github.com/', True,
             'Create a personal access token at https://github.com/settings/tokens',
             'https://docs.github.com/en/rest', '60 calls/hour unauthenticated',
             datetime.now(), datetime.now())
        ]
        
        db.execute_many(
            '''INSERT INTO apis
               (name, description, category, url, auth_required, api_key_instructions,
                documentation_url, rate_limit, created_at, updated_at)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
            sample_apis
        )
        
        return jsonify({'success': True, 'message': 'Sample data initialized'})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health')
def health_check():
    """健康检查"""
    return jsonify({
        'status': 'ok',
        'database': db.db_type,
        'timestamp': datetime.now().isoformat()
    })


@app.errorhandler(404)
def not_found(error):
    """404 错误处理"""
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    """500 错误处理"""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_ENV') != 'production', host='0.0.0.0', port=5000)
