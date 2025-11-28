# 🚀 Free API Hub - 免费 API 聚合平台

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![MySQL](https://img.shields.io/badge/MySQL-Production-orange)
![License](https://img.shields.io/badge/License-MIT-blue)

## 📋 项目介绍

**Free API Hub** 是一个免费的 API 聚合平台，帮助开发者**快速发现、查找和集成**全球主流的公开 API 接口，无需逐个查阅文档就能了解每个 API 的功能、认证方式和使用限制。

![Free API Hub 主页](https://via.placeholder.com/800x400?text=Free+API+Hub+Dashboard)

### ✨ 核心特性

- ✅ **精心编辑的 API 列表** - 涵盖天气、新闻、地理、金融等多个分类
- ✅ **API 密钥获取指南** - 每个 API 都有详细的认证方式说明
- ✅ **智能搜索与分类** - 快速按名称、描述或分类查找 API
- ✅ **收藏夹功能** - 保存常用 API 方便快速访问
- ✅ **响应式设计** - 完美适配桌面、平板和手机
- ✅ **实时 API 数据** - 基于 MySQL 数据库的持久化存储

![API 列表展示](https://via.placeholder.com/800x400?text=API+List+Display)

---

## 🌐 在线访问

### 演示环境

| 项目 | 地址 |
|------|------|
| **前端应用** | https://jinyang756.pythonanywhere.com |
| **API 接口** | https://jinyang756.pythonanywhere.com/api/apis |
| **GitHub 仓库** | https://github.com/jinyang756/api-aggregator |

### 测试账号

```
用户名: Jiuzhougroup
密码: Aa123456
```

---

## 🚀 快速开始

### 前置要求
- Python 3.10+
- MySQL 5.7+ (生产环境)
- Docker & Docker Compose (可选)

### 本地开发

```bash
# 克隆仓库
git clone https://github.com/jinyang756/api-aggregator.git
cd api-aggregator

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动应用（SQLite 本地开发）
python backend/app.py
```

应用将在 **http://localhost:5000** 运行

### Docker 部署

```bash
# 构建并启动容器
docker-compose up -d

# 查看日志
docker-compose logs -f
```

### 生产环境部署（PythonAnywhere）

参考 [`DEPLOY_NOW.md`](./DEPLOY_NOW.md) 获取详细的部署步骤

---

## 📊 项目结构

```
api-aggregator/
├── backend/
│   ├── app.py                 # SQLite 版 Flask 应用
│   ├── app_mysql.py           # MySQL 版 Flask 应用
│   ├── database.py            # 数据库抽象层
│   └── __pycache__/
├── frontend/
│   ├── static/                # CSS、JavaScript 资源
│   │   └── js/
│   │       └── app.js
│   └── templates/             # HTML 模板
│       └── index.html
├── scripts/
│   ├── data_collector.py      # 数据收集脚本
│   └── scheduler.py           # 定时任务调度
├── data/
│   └── api_database.db        # SQLite 数据库（本地开发）
├── requirements.txt           # Python 依赖
├── docker-compose.yml         # Docker 配置
├── Dockerfile                 # Docker 镜像配置
└── README.md                  # 项目文档
```

---

## 🔌 API 分类

平台涵盖以下主要 API 分类：

| 分类 | 示例 API | 用途 |
|------|---------|------|
| **天气** | OpenWeatherMap | 实时天气数据 |
| **新闻** | NewsAPI | 全球新闻源 |
| **地理** | IPGeolocation | IP 地址定位 |
| **开发工具** | GitHub API | 代码仓库管理 |
| **金融** | Alpha Vantage | 股票行情数据 |
| **太空** | NASA APIs | 空间站数据 |

---

## 🛠️ 技术栈

### 后端
- **Flask 2.3.3** - Web 框架
- **PyMySQL 1.1.0** - MySQL 驱动
- **SQLite** - 本地开发数据库
- **Python-dotenv** - 环境变量管理

### 前端
- **HTML5** - 标准页面结构
- **CSS3** - 响应式设计（Tailwind CSS）
- **JavaScript** - 交互功能
- **Fetch API** - HTTP 请求

### 部署
- **PythonAnywhere** - 云托管（生产环境）
- **Docker** - 容器化
- **GitHub** - 代码仓库

---

## 📝 API 端点

### 获取 API 列表
```
GET /api/apis
```

**响应示例：**
```json
[
  {
    "id": 1,
    "name": "OpenWeatherMap",
    "category": "Weather",
    "description": "Weather data API",
    "url": "https://openweathermap.org/api",
    "auth_required": 1,
    "rate_limit": "60 calls/minute"
  }
]
```

### 按分类获取 API
```
GET /api/categories
```

### 获取最爱的 API
```
GET /api/favorites
```

---

## 🔐 环境配置

创建 `.env` 文件配置生产环境：

```env
# Flask 配置
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# 数据库配置
DB_TYPE=mysql
DB_HOST=your-mysql-host
DB_PORT=3306
DB_USER=your-username
DB_PASSWORD=your-password
DB_NAME=your-database
```

---

## 📖 文档

- [`START_HERE.md`](./START_HERE.md) - 项目启动指南
- [`DEPLOY_NOW.md`](./DEPLOY_NOW.md) - 快速部署步骤
- [`PYTHONANYWHERE_DEPLOYMENT.md`](./PYTHONANYWHERE_DEPLOYMENT.md) - PythonAnywhere 详细部署
- [`MYSQL_SETUP_COMPLETE.md`](./MYSQL_SETUP_COMPLETE.md) - MySQL 配置

---

## 🤝 贡献指南

欢迎提交 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [`LICENSE`](LICENSE) 文件

---

## 📧 联系方式

有问题或建议？欢迎提交 Issue 或联系维护者。

**GitHub**: https://github.com/jinyang756/api-aggregator

**Patreon**: https://www.patreon.com/cw/darkoarea

---

**⭐ 如果你觉得这个项目有帮助，请给个 Star！**

**💪 想要支持项目开发？欢迎在 Patreon 上成为赞助者！**