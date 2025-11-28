# 🚀 PythonAnywhere MySQL 快速部署卡片

## 📋 你的数据库信息

```
✓ 主机: jinyang756.mysql.pythonanywhere-services.com
✓ 用户名: jinyang756
✓ 密码: Aa123456..
✓ 数据库: jinyang756$api-aggregator
✓ 端口: 3306
```

---

## ⚡ 5 步快速部署

### 第 1 步：上传代码
```bash
cd /home/jinyang756
git clone <你的仓库> free-api-hub
cd free-api-hub/api-aggregator
```

### 第 2 步：安装依赖
```bash
mkvirtualenv --python=/usr/bin/python3.10 api-hub-mysql
workon api-hub-mysql
pip install -r requirements.txt
```

### 第 3 步：编辑 WSGI 文件

在 PythonAnywhere Web 应用配置中，复制以下内容到 WSGI configuration file：

```python
import sys
import os

path = '/home/jinyang756/free-api-hub/api-aggregator'
if path not in sys.path:
    sys.path.append(path)

venv = '/home/jinyang756/.virtualenvs/api-hub-mysql'
activate_this = os.path.join(venv, 'bin', 'activate_this.py')

try:
    exec(open(activate_this).read(), {'__file__': activate_this})
except FileNotFoundError:
    pass

os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_APP'] = 'backend.app_mysql'
os.environ['SECRET_KEY'] = 'your_secret_key'
os.environ['DB_TYPE'] = 'mysql'
os.environ['DB_HOST'] = 'jinyang756.mysql.pythonanywhere-services.com'
os.environ['DB_PORT'] = '3306'
os.environ['DB_USER'] = 'jinyang756'
os.environ['DB_PASSWORD'] = 'Aa123456..'
os.environ['DB_NAME'] = 'jinyang756$api-aggregator'
os.environ['DEBUG'] = 'False'

from backend.app_mysql import app as application
```

### 第 4 步：配置静态文件

在 Web 应用配置中添加：

| URL | 路径 |
|-----|------|
| `/static/` | `/home/jinyang756/free-api-hub/api-aggregator/frontend/static` |

### 第 5 步：重启应用

点击 **Reload** 按钮 🟢

---

## ✅ 初始化数据库

访问此 URL 创建表和示例数据：

```
https://jinyang756.pythonanywhere.com/api/init_sample_data
```

---

## 🌐 应用地址

```
🔗 https://jinyang756.pythonanywhere.com
```

---

## 📁 项目文件说明

| 文件 | 用途 |
|------|------|
| `backend/app_mysql.py` | MySQL 版本的主应用 |
| `backend/database.py` | 数据库抽象层（支持 SQLite 和 MySQL） |
| `.env` | 生产环境配置（已设置 MySQL 参数） |
| `MYSQL_DEPLOYMENT.md` | 详细部署指南 |

---

## 🔧 常用命令

### 测试 API

```bash
# 获取所有 API
curl https://jinyang756.pythonanywhere.com/api/apis

# 搜索特定 API
curl 'https://jinyang756.pythonanywhere.com/api/apis?search=weather'

# 按分类筛选
curl 'https://jinyang756.pythonanywhere.com/api/apis?category=Weather'

# 健康检查
curl https://jinyang756.pythonanywhere.com/api/health
```

### 数据库管理

```bash
# 连接数据库
mysql -h jinyang756.mysql.pythonanywhere-services.com -u jinyang756 -p
# 输入密码：Aa123456..

# 查看表
USE jinyang756$api-aggregator;
SHOW TABLES;

# 备份数据库
mysqldump -h jinyang756.mysql.pythonanywhere-services.com \
          -u jinyang756 -p \
          jinyang756$api-aggregator > backup.sql
```

---

## 🔐 重要！

✅ 生产环境需要更改的地方：

1. 在 WSGI 文件中修改 `SECRET_KEY` 为强密码
2. 定期备份数据库
3. 监控应用日志
4. 不要在代码中硬编码敏感信息

---

## 🆘 快速故障排查

| 问题 | 检查项 |
|------|--------|
| 502 错误 | WSGI 配置、虚拟环境路径、依赖安装 |
| 无法连接数据库 | 检查主机名、用户名、密码、数据库名 |
| 表不存在 | 访问 `/api/init_sample_data` 初始化 |
| 找不到静态文件 | 检查静态文件映射路径 |

查看完整日志：Web 应用配置 → Log files

---

**备忘单完成！** 现在按照 5 个步骤部署即可。有问题？查看 `MYSQL_DEPLOYMENT.md` 🚀
