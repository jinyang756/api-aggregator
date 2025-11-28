# PythonAnywhere MySQL 数据库部署指南

## 📋 数据库信息

```
主机: jinyang756.mysql.pythonanywhere-services.com
用户名: jinyang756
MySQL 密码: Aa123456..
数据库名: jinyang756$api-aggregator
端口: 3306
```

---

## 🚀 快速部署（5 步）

### 1️⃣ 上传代码到 PythonAnywhere

在 PythonAnywhere Bash Console 中：

```bash
cd /home/jinyang756
git clone <your-repo> free-api-hub
cd free-api-hub/api-aggregator
```

### 2️⃣ 创建虚拟环境

```bash
mkvirtualenv --python=/usr/bin/python3.10 api-hub-mysql
workon api-hub-mysql
pip install -r requirements.txt
```

### 3️⃣ 配置 WSGI 文件

在 PythonAnywhere Web 应用配置中，编辑 WSGI configuration file，替换为：

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

# 设置环境变量
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_APP'] = 'backend.app_mysql'
os.environ['SECRET_KEY'] = 'your_strong_secret_key_here'
os.environ['DB_TYPE'] = 'mysql'
os.environ['DB_HOST'] = 'jinyang756.mysql.pythonanywhere-services.com'
os.environ['DB_PORT'] = '3306'
os.environ['DB_USER'] = 'jinyang756'
os.environ['DB_PASSWORD'] = 'Aa123456..'
os.environ['DB_NAME'] = 'jinyang756$api-aggregator'
os.environ['DEBUG'] = 'False'

from backend.app_mysql import app as application
```

### 4️⃣ 配置静态文件

在 Web 应用配置中，添加静态文件映射：

| URL | 目录 |
|-----|------|
| `/static/` | `/home/jinyang756/free-api-hub/api-aggregator/frontend/static` |

### 5️⃣ 重启应用

点击 Web 应用配置中的绿色 **"Reload"** 按钮

---

## ✅ 初始化数据库

部署完成后，访问以下 URL 创建数据表并导入示例数据：

```
https://jinyang756.pythonanywhere.com/api/init_sample_data
```

应该看到响应：
```json
{"success": true, "message": "Sample data initialized"}
```

---

## 🔍 验证部署

### 检查应用状态

```bash
# 访问健康检查端点
curl https://jinyang756.pythonanywhere.com/api/health

# 响应示例：
# {"status": "ok", "database": "mysql", "timestamp": "2025-11-29T..."}
```

### 测试 API 端点

```bash
# 获取所有分类
curl https://jinyang756.pythonanywhere.com/api/categories

# 获取所有 API
curl https://jinyang756.pythonanywhere.com/api/apis

# 搜索特定 API
curl 'https://jinyang756.pythonanywhere.com/api/apis?search=weather'

# 按分类筛选
curl 'https://jinyang756.pythonanywhere.com/api/apis?category=Weather'
```

---

## 🗄️ 数据库管理

### 连接到 MySQL 数据库

```bash
# 在 PythonAnywhere Bash 中
mysql -h jinyang756.mysql.pythonanywhere-services.com \
      -u jinyang756 -p

# 输入密码: Aa123456..
```

### 查看表结构

```sql
USE jinyang756$api-aggregator;
SHOW TABLES;
DESC categories;
DESC apis;
DESC favorites;
```

### 查看数据

```sql
-- 查看所有分类
SELECT * FROM categories;

-- 查看所有 API
SELECT * FROM apis;

-- 查看收藏
SELECT * FROM favorites;

-- 统计数据
SELECT COUNT(*) as api_count FROM apis;
SELECT COUNT(*) as category_count FROM categories;
```

---

## 💾 备份数据库

### 导出备份

```bash
# 完整备份
mysqldump -h jinyang756.mysql.pythonanywhere-services.com \
          -u jinyang756 -p \
          jinyang756$api-aggregator > api-aggregator-backup.sql

# 输入密码: Aa123456..
```

### 恢复备份

```bash
# 恢复数据库
mysql -h jinyang756.mysql.pythonanywhere-services.com \
      -u jinyang756 -p \
      jinyang756$api-aggregator < api-aggregator-backup.sql
```

---

## 🛠️ 本地开发配置

如需在本地使用 SQLite 开发：

### 修改 .env

```
DB_TYPE=sqlite
DB_PATH=data/api_database.db
FLASK_ENV=development
DEBUG=True
```

### 运行应用

```bash
cd api-aggregator
python backend/app.py
```

---

## 🐛 故障排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 502 Bad Gateway | WSGI 配置错误 | 检查 WSGI 文件路径和数据库凭证 |
| Can't connect to MySQL | 连接信息错误 | 验证主机、用户名、密码、数据库名 |
| Table doesn't exist | 表未创建 | 访问 `/api/init_sample_data` |
| Static files 404 | 路径错误 | 检查静态文件映射路径 |
| ModuleNotFoundError | 依赖未安装 | 运行 `pip install -r requirements.txt` |

---

## 📊 应用访问地址

- **主应用**：https://jinyang756.pythonanywhere.com
- **API 列表**：https://jinyang756.pythonanywhere.com/api/apis
- **分类列表**：https://jinyang756.pythonanywhere.com/api/categories
- **健康检查**：https://jinyang756.pythonanywhere.com/api/health

---

## 🔐 安全建议

1. ✅ 定期更改数据库密码
2. ✅ 使用强密码的 SECRET_KEY
3. ✅ 不要在代码中硬编码敏感信息
4. ✅ 生产环境中禁用调试模式 (DEBUG=False)
5. ✅ 定期备份数据库
6. ✅ 监控应用日志

---

## 📞 需要帮助？

- PythonAnywhere 支持：https://www.pythonanywhere.com/support/
- 官方文档：https://help.pythonanywhere.com/
- MySQL 官方文档：https://dev.mysql.com/doc/

---

**部署完成！** 🎉

现在你可以访问 https://jinyang756.pythonanywhere.com 使用你的应用了。
