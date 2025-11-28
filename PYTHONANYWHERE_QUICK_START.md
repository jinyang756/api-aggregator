# PythonAnywhere 快速部署指南

## 🚀 5 分钟快速部署

### 1️⃣ 注册账户
- 访问 https://www.pythonanywhere.com
- 免费注册（Beginner 计划）

### 2️⃣ 上传代码
在 PythonAnywhere Bash Console 中：
```bash
cd /home/your_username
git clone https://github.com/your_username/free-api-hub.git
# 或者上传 ZIP 并解压
```

### 3️⃣ 一键部署
```bash
bash free-api-hub/api-aggregator/pythonanywhere_setup.sh
```

### 4️⃣ 配置 WSGI
在 Web 应用配置中，将 WSGI 文件内容替换为 `pythonanywhere_wsgi.py` 的内容

### 5️⃣ 重启应用
点击 Web 应用配置中的绿色 "Reload" 按钮

---

## 📊 部署前检查清单

- [ ] 已注册 PythonAnywhere 账户
- [ ] 已上传项目代码
- [ ] 已创建虚拟环境
- [ ] 已安装 requirements.txt 依赖
- [ ] 已初始化数据库
- [ ] WSGI 配置已设置
- [ ] 静态文件映射已配置
- [ ] 应用已重启

---

## 🔐 生产环境配置

### 环境变量设置
在 PythonAnywhere 账户设置中添加：
```
SECRET_KEY=your_random_secret_key_here
FLASK_ENV=production
```

### 静态文件映射
| URL | 路径 |
|-----|------|
| `/static/` | `/home/username/free-api-hub/api-aggregator/frontend/static` |

---

## 📍 应用访问地址

- **主站点**: `https://your_username.pythonanywhere.com`
- **API 端点**: `https://your_username.pythonanywhere.com/api/apis`
- **初始化数据**: `https://your_username.pythonanywhere.com/api/init_sample_data`

---

## 🆘 常见问题

**Q: 502 Bad Gateway?**
- A: 检查 WSGI 配置和虚拟环境路径

**Q: 静态文件加载失败?**
- A: 验证静态文件映射路径正确且有读权限

**Q: 数据库不存在?**
- A: 运行 `python -c "from backend.app import init_db; init_db()"`

**Q: 需要自定义域名?**
- A: 升级到付费计划（Hacker Plan $5/月）

---

## 📞 获取帮助

- PythonAnywhere 文档: https://help.pythonanywhere.com/
- 官方论坛: https://www.pythonanywhere.com/forums/
- 中文社区: https://www.v2ex.com/ (搜索 PythonAnywhere)

---

**部署完成后别忘记：**
1. ✅ 访问 `/api/init_sample_data` 初始化示例数据
2. ✅ 测试搜索功能和 API 端点
3. ✅ 设置定期数据备份任务
