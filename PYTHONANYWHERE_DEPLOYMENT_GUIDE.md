# 🚀 PythonAnywhere 一键部署指南

## 📌 你的信息

```
GitHub 仓库: https://github.com/jinyang756/api-aggregator.git
PythonAnywhere 账户: jinyang756
数据库: jinyang756$api-aggregator
MySQL 密码: Aa123456..
```

---

## ⚡ 5 分钟快速部署

### 步骤 1️⃣：在 PythonAnywhere Bash Console 执行

```bash
cd /home/jinyang756
git clone https://github.com/jinyang756/api-aggregator.git
cd api-aggregator
```

### 步骤 2️⃣：创建虚拟环境和安装依赖

```bash
mkvirtualenv --python=/usr/bin/python3.10 api-hub-mysql
workon api-hub-mysql
pip install -r requirements.txt
```

### 步骤 3️⃣：配置 WSGI 文件

1. 登录 PythonAnywhere Web 控制台
2. 点击 **Web** → 选择你的应用
3. 向下滚动找到 **WSGI configuration file**
4. 点击编辑，**完全替换**为下面的代码：

```python
import sys
import os

path = '/home/jinyang756/api-aggregator'
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

### 步骤 4️⃣：配置静态文件

在同一个 Web 应用配置页面中，找到 **Static files** 部分，添加：

| URL path | Directory |
|----------|-----------|
| `/static/` | `/home/jinyang756/api-aggregator/frontend/static` |

### 步骤 5️⃣：重启应用

点击页面顶部的绿色 **"Reload"** 按钮

---

## ✅ 验证部署

### 应用地址
```
https://jinyang756.pythonanywhere.com
```

### 初始化数据库（访问此 URL）
```
https://jinyang756.pythonanywhere.com/api/init_sample_data
```

### 测试 API 端点
```
https://jinyang756.pythonanywhere.com/api/apis
https://jinyang756.pythonanywhere.com/api/categories
```

---

## 🐛 如果看到 502 错误

### 快速排查：

1. **查看日志**
   - Web 应用配置 → **Log files**
   - 查看 **Server error log** 和 **error log**

2. **常见问题和解决方案**

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| ModuleNotFoundError | 依赖未安装 | `workon api-hub-mysql && pip install -r requirements.txt` |
| Can't connect MySQL | 数据库配置错误 | 检查 WSGI 中的数据库凭证 |
| Import error (app_mysql) | 虚拟环境路径错误 | 验证 venv 路径和 activate_this 文件 |
| Table doesn't exist | 未初始化数据库 | 访问 `/api/init_sample_data` |

3. **重新部署**
   ```bash
   workon api-hub-mysql
   cd /home/jinyang756/api-aggregator
   git pull origin main
   pip install -r requirements.txt
   ```

4. **重启应用**
   - 点击 Web 应用配置中的 **Reload** 按钮

---

## 📊 数据库管理

### 连接数据库（在 Bash Console 中）

```bash
mysql -h jinyang756.mysql.pythonanywhere-services.com -u jinyang756 -p
# 输入密码：Aa123456..
```

### 查看表

```sql
USE jinyang756$api-aggregator;
SHOW TABLES;
```

### 备份数据库

```bash
mysqldump -h jinyang756.mysql.pythonanywhere-services.com \
          -u jinyang756 -p \
          jinyang756$api-aggregator > backup.sql
# 输入密码：Aa123456..
```

---

## 🔄 更新代码

当你在 GitHub 上更新代码时：

```bash
cd /home/jinyang756/api-aggregator
workon api-hub-mysql
git pull origin main
pip install -r requirements.txt
# 然后在 Web 控制台点击 Reload
```

---

## 💾 项目文件说明

```
api-aggregator/
├── backend/
│   ├── app_mysql.py          ← MySQL 版本应用
│   ├── database.py           ← 数据库抽象层
│   └── app.py                ← SQLite 版本（不用）
├── frontend/
│   ├── static/               ← JavaScript、CSS
│   └── templates/            ← HTML 模板
├── .env                      ← 配置文件（本地）
├── requirements.txt          ← 依赖包
├── MYSQL_QUICK_REFERENCE.md  ← 这个文件
└── MYSQL_DEPLOYMENT.md       ← 详细指南
```

---

## 🔐 重要安全提醒

✅ **必做项目：**

1. 修改 WSGI 文件中的 `SECRET_KEY`：
   ```python
   os.environ['SECRET_KEY'] = '你自己的复杂密钥'
   ```

2. 不要在代码中暴露敏感信息

3. 定期备份数据库

4. 监控应用日志

---

## 📞 快速参考

| 需求 | 命令 |
|------|------|
| 激活虚拟环境 | `workon api-hub-mysql` |
| 安装依赖 | `pip install -r requirements.txt` |
| 查看 Python 版本 | `python --version` |
| 连接数据库 | `mysql -h jinyang756.mysql.pythonanywhere-services.com -u jinyang756 -p` |
| 备份数据库 | `mysqldump ... > backup.sql` |
| 查看日志 | Web 应用配置 → Log files |
| 重启应用 | 点击绿色 Reload 按钮 |

---

## 🎯 完整检查清单

- [ ] 克隆代码到 `/home/jinyang756/api-aggregator`
- [ ] 创建虚拟环境 `api-hub-mysql`
- [ ] 安装依赖包
- [ ] 编辑 WSGI 文件（复制上面的代码）
- [ ] 配置静态文件映射
- [ ] 点击 Reload 重启应用
- [ ] 访问应用地址验证部署
- [ ] 访问 `/api/init_sample_data` 初始化数据库
- [ ] 修改 SECRET_KEY 为强密码
- [ ] 备份数据库配置

---

## 💡 常用命令速查

```bash
# 进入项目目录
cd /home/jinyang756/api-aggregator

# 激活虚拟环境
workon api-hub-mysql

# 更新代码
git pull origin main

# 重新安装依赖
pip install -r requirements.txt --upgrade

# 连接数据库
mysql -h jinyang756.mysql.pythonanywhere-services.com -u jinyang756 -p

# 备份数据库
mysqldump -h jinyang756.mysql.pythonanywhere-services.com \
          -u jinyang756 -p \
          jinyang756$api-aggregator > backup-$(date +%Y%m%d).sql
```

---

## 🚀 你已准备好了！

按照上面的 5 个步骤，你的应用将在 PythonAnywhere 上成功运行。

**预计部署时间：5 分钟** ⏱️

**祝部署顺利！** 🎉

---

*需要帮助？查看 `MYSQL_DEPLOYMENT.md` 获取详细说明*
