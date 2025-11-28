# 📋 部署检查清单

## ✅ 已完成的配置

- [x] 创建 MySQL 支持的应用文件 (`backend/app_mysql.py`)
- [x] 创建数据库抽象层 (`backend/database.py`)
- [x] 支持 SQLite 和 MySQL 双数据库
- [x] 创建 `.env` 配置文件（包含 MySQL 凭证）
- [x] 安装 PyMySQL 和依赖包
- [x] 创建详细的部署指南
- [x] 创建快速参考卡片

---

## 🚀 PythonAnywhere 部署步骤

### 步骤 1️⃣ - 准备工作（✓ 已完成）

**文件列表 - 上传到 PythonAnywhere：**

```
free-api-hub/
├── api-aggregator/
│   ├── backend/
│   │   ├── app_mysql.py          ← MySQL 版本应用 ✓
│   │   ├── database.py           ← 数据库抽象层 ✓
│   │   ├── __pycache__/
│   │   └── app.py                ← 原始 SQLite 版本
│   ├── frontend/
│   │   ├── static/
│   │   │   └── js/
│   │   │       └── app.js
│   │   └── templates/
│   │       └── index.html
│   ├── data/                     ← 本地 SQLite 存储（可选）
│   ├── scripts/
│   ├── .env                      ← 环境配置 ✓
│   ├── .env.example              ← 配置模板 ✓
│   ├── requirements.txt           ← 依赖包 ✓（已更新）
│   ├── MYSQL_DEPLOYMENT.md       ← 详细指南 ✓
│   ├── MYSQL_QUICK_REFERENCE.md  ← 快速参考 ✓
│   └── ... 其他文件
```

### 步骤 2️⃣ - 上传代码到 PythonAnywhere

```bash
# 在 PythonAnywhere Bash Console
cd /home/jinyang756
git clone <你的仓库 URL> free-api-hub

# 或者通过文件管理上传 ZIP，然后解压
cd free-api-hub/api-aggregator
```

### 步骤 3️⃣ - 创建虚拟环境

```bash
mkvirtualenv --python=/usr/bin/python3.10 api-hub-mysql
workon api-hub-mysql
pip install -r requirements.txt
```

### 步骤 4️⃣ - 配置 WSGI 文件

在 Web 应用配置中编辑 WSGI configuration file，替换为：

[查看 MYSQL_QUICK_REFERENCE.md 中的 WSGI 代码]

### 步骤 5️⃣ - 配置静态文件

| URL | 路径 |
|-----|------|
| `/static/` | `/home/jinyang756/free-api-hub/api-aggregator/frontend/static` |

### 步骤 6️⃣ - 重启应用

点击 Web 应用配置中的绿色 **"Reload"** 按钮

### 步骤 7️⃣ - 初始化数据库

访问：
```
https://jinyang756.pythonanywhere.com/api/init_sample_data
```

---

## 🔑 数据库信息总结

```
主机: jinyang756.mysql.pythonanywhere-services.com
用户: jinyang756
密码: Aa123456..
数据库: jinyang756$api-aggregator
端口: 3306
```

---

## 📝 文件说明

### 新创建的文件

| 文件 | 用途 |
|------|------|
| `backend/app_mysql.py` | Flask 应用，支持 MySQL 数据库 |
| `backend/database.py` | 数据库抽象层，支持 SQLite/MySQL 切换 |
| `.env` | 生产环境配置（已配置 MySQL 参数） |
| `.env.example` | 配置模板 |
| `MYSQL_DEPLOYMENT.md` | 详细部署指南 |
| `MYSQL_QUICK_REFERENCE.md` | 快速参考卡片 |
| `requirements.txt` | 已更新，包含 PyMySQL |

### 修改的文件

| 文件 | 变更 |
|------|------|
| `requirements.txt` | 添加了 `PyMySQL==1.1.0` 和 `cryptography==41.0.0` |

---

## 🧪 本地测试

### 使用 SQLite（本地开发）

```bash
# 保持原 .env 配置或创建新的
DB_TYPE=sqlite
DB_PATH=data/api_database.db

# 运行
python backend/app.py
```

### 使用 MySQL（仅在 PythonAnywhere 上）

```bash
# WSGI 自动加载 MySQL 配置
# 本地无法测试（网络限制）
```

---

## 🔗 访问地址

部署完成后：

- **主应用**：https://jinyang756.pythonanywhere.com
- **Web 界面**：https://jinyang756.pythonanywhere.com/
- **API 端点**：https://jinyang756.pythonanywhere.com/api/apis
- **分类列表**：https://jinyang756.pythonanywhere.com/api/categories
- **健康检查**：https://jinyang756.pythonanywhere.com/api/health

---

## 📦 依赖包清单

```
Flask==2.3.3
Flask-SQLAlchemy==3.1.1
gunicorn==21.2.0
python-dotenv==1.0.1
requests==2.32.3
APScheduler==3.10.4
Werkzeug==2.3.8
PyMySQL==1.1.0          ← 新增
cryptography==41.0.0    ← 新增
```

---

## ⚠️ 注意事项

1. **本地连接 MySQL 限制**
   - 由于网络限制，本地无法连接到 PythonAnywhere MySQL
   - 这是正常的，部署到 PythonAnywhere 后会自动工作

2. **环境变量配置**
   - 在 PythonAnywhere WSGI 文件中已配置所有必要的环境变量
   - 确保 `SECRET_KEY` 已更改为强密码

3. **数据库初始化**
   - 部署后第一次必须访问 `/api/init_sample_data` 创建表
   - 之后才能正常使用应用

4. **备份建议**
   - 定期备份 MySQL 数据库
   - 使用 `mysqldump` 命令导出备份

---

## 🆘 常见问题

**Q: 为什么本地无法连接 MySQL？**
A: 这是正常的。PythonAnywhere MySQL 只能从 PythonAnywhere 服务器访问。

**Q: 部署后看到 502 错误？**
A: 检查 WSGI 配置文件、虚拟环境路径、依赖安装。查看 Web 应用日志。

**Q: 如何切换回 SQLite？**
A: 修改 .env 中的 `DB_TYPE=sqlite`，或运行原来的 `app.py`。

**Q: 数据库表没有创建？**
A: 访问 `/api/init_sample_data` URL 自动创建表。

---

## 📞 下一步行动

1. ☐ 将代码推送到 GitHub（如果使用 Git 部署）
2. ☐ 在 PythonAnywhere 中创建新 Web 应用
3. ☐ 按照上述 7 个步骤部署
4. ☐ 访问 `/api/init_sample_data` 初始化数据库
5. ☐ 测试应用是否正常运行

---

**所有准备工作已完成！** 🎉

现在可以按照部署步骤部署到 PythonAnywhere 了。

详细说明：`MYSQL_DEPLOYMENT.md`
快速参考：`MYSQL_QUICK_REFERENCE.md`
