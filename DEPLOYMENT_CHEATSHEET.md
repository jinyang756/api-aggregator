# 📋 部署速记卡（打印版）

## 🎯 你的部署信息

```
GitHub: https://github.com/jinyang756/api-aggregator.git
PythonAnywhere 用户: jinyang756
应用地址: https://jinyang756.pythonanywhere.com
数据库: jinyang756$api-aggregator
MySQL 密码: Aa123456..
```

---

## ⚡ 5 步部署（复制粘贴）

### 第 1 步：Bash Console
```bash
cd /home/jinyang756
git clone https://github.com/jinyang756/api-aggregator.git
cd api-aggregator
```

### 第 2 步：Bash Console
```bash
mkvirtualenv --python=/usr/bin/python3.10 api-hub-mysql
workon api-hub-mysql
pip install -r requirements.txt
```

### 第 3 步：编辑 WSGI 文件
复制这段代码到 Web 应用配置中的 WSGI configuration file：

```python
import sys, os
path = '/home/jinyang756/api-aggregator'
if path not in sys.path:
    sys.path.append(path)
venv = '/home/jinyang756/.virtualenvs/api-hub-mysql'
activate_this = os.path.join(venv, 'bin', 'activate_this.py')
try:
    exec(open(activate_this).read(), {'__file__': activate_this})
except:
    pass
os.environ['FLASK_ENV'] = 'production'
os.environ['FLASK_APP'] = 'backend.app_mysql'
os.environ['SECRET_KEY'] = 'jinyang756-secret-key-2025'
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
添加到 Web 应用配置的 Static files 部分：
- URL: `/static/`
- Path: `/home/jinyang756/api-aggregator/frontend/static`

### 第 5 步：点击 Reload 🟢

---

## ✅ 部署后

### 初始化数据库
```
https://jinyang756.pythonanywhere.com/api/init_sample_data
```

### 访问应用
```
https://jinyang756.pythonanywhere.com
```

### 测试 API
```
https://jinyang756.pythonanywhere.com/api/apis
```

---

## 🐛 常见问题

| 问题 | 解决方案 |
|------|---------|
| 502 错误 | 查看 Log files，检查 WSGI 配置 |
| 无法连接数据库 | 验证数据库凭证 |
| 表不存在 | 访问 `/api/init_sample_data` |
| 静态文件 404 | 检查静态文件映射路径 |

---

## 💾 MySQL 命令

```bash
# 连接数据库
mysql -h jinyang756.mysql.pythonanywhere-services.com -u jinyang756 -p
# 密码：Aa123456..

# 备份数据库
mysqldump -h jinyang756.mysql.pythonanywhere-services.com \
          -u jinyang756 -p \
          jinyang756$api-aggregator > backup.sql
```

---

## 🔐 安全提示

- [ ] 修改 SECRET_KEY 为强密码
- [ ] 定期备份数据库
- [ ] 监控应用日志
- [ ] 关闭调试模式（已关闭）

---

**预计部署时间：15-20 分钟**

打印此卡片，跟着步骤走，5 分钟完成！🚀
