# PythonAnywhere WSGI 配置文件
# 复制这个文件的内容到 PythonAnywhere 的 WSGI configuration file

import sys
import os

# 添加项目路径（根据你的用户名修改）
# 例如：path = '/home/username/free-api-hub/api-aggregator'
path = '/home/your_username/free-api-hub/api-aggregator'
if path not in sys.path:
    sys.path.append(path)

# 设置虚拟环境（根据你的用户名修改）
# 例如：venv = '/home/username/.virtualenvs/api-hub'
venv = '/home/your_username/.virtualenvs/api-hub'
activate_this = os.path.join(venv, 'bin', 'activate_this.py')

try:
    exec(open(activate_this).read(), {'__file__': activate_this})
except FileNotFoundError:
    print("Warning: Virtual environment activation file not found")
    pass

# 设置环境变量
os.environ['FLASK_ENV'] = 'production'
os.environ['PYTHONPATH'] = path

# 导入 Flask 应用
try:
    from backend.app import app as application
except ImportError as e:
    print(f"Error importing app: {e}")
    
    # 创建一个简单的应用用于调试
    from flask import Flask
    application = Flask(__name__)
    
    @application.route('/')
    def error():
        return f"Error loading application: {e}", 500
