# PythonAnywhere 部署指南

PythonAnywhere 是一个完全托管的 Python 云平台，非常适合部署 Flask 应用。

## 📋 前置要求

1. PythonAnywhere 账户（免费账户足够）
2. GitHub 账户（用于 Git 部署，可选）
3. 本地 Git 或 ZIP 文件

## 🚀 部署步骤

### 第一步：注册 PythonAnywhere

1. 访问 https://www.pythonanywhere.com
2. 点击 "Sign up for free account"
3. 选择免费计划（Beginner）
4. 完成注册和邮箱验证

### 第二步：创建 Web 应用

1. 登录 PythonAnywhere 仪表盘
2. 点击 "Web" → "Add a new web app"
3. 选择 "Manual configuration"
4. 选择 Python 3.10+

### 第三步：上传代码

#### 方式 A：使用 Git（推荐）

```bash
# 在 PythonAnywhere Bash Console 中执行
cd /home/your_username
git clone https://github.com/your_username/free-api-hub.git
cd free-api-hub/api-aggregator
```

#### 方式 B：使用 ZIP 上传

1. 在 PythonAnywhere 文件管理中上传 ZIP
2. 在 Bash 中解压：
```bash
cd /home/your_username
unzip free-api-hub.zip
cd api-aggregator
```

### 第四步：配置虚拟环境

在 PythonAnywhere Bash Console 中：

```bash
# 创建虚拟环境
mkvirtualenv --python=/usr/bin/python3.10 api-hub

# 进入虚拟环境
workon api-hub

# 安装依赖
pip install -r requirements.txt
```

### 第五步：配置 WSGI 文件

1. 在 Web 应用配置中，找到 WSGI configuration file
2. 点击编辑该文件，替换内容为：

```python
import sys
import os

# 添加项目路径
path = '/home/your_username/free-api-hub/api-aggregator'
if path not in sys.path:
    sys.path.append(path)

# 设置虚拟环境
venv = '/home/your_username/.virtualenvs/api-hub'
activate_this = os.path.join(venv, 'bin', 'activate_this.py')
exec(open(activate_this).read(), {'__file__': activate_this})

# 导入 Flask 应用
from backend.app import app as application
```

3. 保存文件

### 第六步：配置静态文件

在 Web 应用配置中，配置静态文件映射：

| URL | 目录 |
|-----|------|
| `/static` | `/home/your_username/free-api-hub/api-aggregator/frontend/static` |

### 第七步：重启应用

1. 在 Web 应用配置页面，点击绿色的 "Reload" 按钮
2. 应用应该在几秒内启动

### 第八步：访问应用

你的应用将在以下地址可访问：
- `https://your_username.pythonanywhere.com`

## 🔧 初始化数据库

访问以下 URL 初始化示例数据：
```
https://your_username.pythonanywhere.com/api/init_sample_data
```

## 📊 免费计划限制

| 功能 | 限制 |
|------|------|
| CPU 时间 | 每天 100 秒 |
| 内存 | 512 MB |
| 域名 | username.pythonanywhere.com |
| SSL 支持 | ✓ 免费 HTTPS |
| 数据库大小 | 无限 |

## 🔐 安全配置

### 1. 更新 Flask 配置

修改 `backend/app.py`：

```python
import os

# 生产环境配置
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['DEBUG'] = False  # 关闭调试模式
app.config['PROPAGATE_EXCEPTIONS'] = True
```

### 2. 在 PythonAnywhere 中设置环境变量

在 Web 应用配置的 "Environment variables" 中添加：
```
SECRET_KEY=your_random_secret_key_here
```

## 📅 自动任务

PythonAnywhere 的 Scheduled tasks 可以运行定期更新：

1. 转到 Account → Scheduled tasks
2. 创建新任务
3. 时间：每天 03:00
4. 命令：
```bash
/home/your_username/.virtualenvs/api-hub/bin/python /home/your_username/free-api-hub/api-aggregator/scripts/scheduler.py
```

## 🐛 故障排查

### 问题 1：502 Bad Gateway

**解决方案：**
- 检查 WSGI 文件路径是否正确
- 查看日志：Web 应用配置 → Log files
- 重新加载应用

### 问题 2：静态文件 404

**解决方案：**
- 确保静态文件映射路径正确
- 检查文件夹权限（`chmod 755`）

### 问题 3：数据库文件不存在

**解决方案：**
```bash
# 在 Bash 中手动初始化
cd /home/your_username/free-api-hub/api-aggregator
python -c "from backend.app import init_db; init_db()"
```

## 📈 升级到付费计划

需要更多资源时：

1. 登录 PythonAnywhere
2. 转到 Account → Upgrade
3. 选择合适的计划
   - **Hacker Plan**：$5/月，2GB 磁盘，更多 CPU 时间
   - **Noob Plan**：$9/月，5GB 磁盘，自定义域名

## 🔗 有用的链接

- [PythonAnywhere 文档](https://help.pythonanywhere.com/)
- [Flask 部署指南](https://flask.palletsprojects.com/en/2.3.x/deploying/)
- [WSGI 参考](https://peps.python.org/pep-3333/)

## 💡 最佳实践

1. ✅ 定期备份数据库文件
2. ✅ 监控应用日志
3. ✅ 设置错误告警
4. ✅ 使用环境变量存储敏感信息
5. ✅ 定期更新依赖包

---

**需要帮助？** 访问 PythonAnywhere 官方论坛或社区支持
