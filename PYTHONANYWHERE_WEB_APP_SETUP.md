# 🚀 PythonAnywhere Web 应用创建指南（详细步骤）

## 📍 当前步骤

你已经进入了 PythonAnywhere **"Add a new web app"** 页面。

这是你应该看到的选项：
```
» Django
» web2py
» Flask
» Bottle
» Manual configuration (including virtualenvs)
```

---

## ✅ 选择方式

### 🎯 你应该选择：**Manual configuration (including virtualenvs)**

**原因：**
- ✅ 完全控制虚拟环境路径
- ✅ 可以自定义 WSGI 配置
- ✅ 支持 MySQL 数据库连接
- ✅ 灵活配置 Flask 应用

**不要选择 "Flask" 选项，因为：**
- ❌ 会自动创建虚拟环境（我们需要自定义）
- ❌ 无法指定 Python 版本（我们需要 3.10）
- ❌ 配置会被限制

---

## 🔄 Web 应用创建流程

### 第 1 步：选择 Manual configuration

在选项列表中点击：
```
» Manual configuration (including virtualenvs)
```

### 第 2 步：选择 Python 版本

**选择：Python 3.10**

```
» Python 3.9 (Flask 3.0.3)
» Python 3.10 (Flask 3.0.3)  ← 选这个
» Python 3.11 (Flask 3.0.3)
» Python 3.12 (Flask 3.0.3)
» Python 3.13 (Flask 3.0.3)
```

### 第 3 步：确认创建

- 点击 **"Next"** 或 **"Create"** 按钮
- 等待 Web 应用创建完成

---

## 📋 创建完成后（重要！）

创建完成后，你会看到 Web 应用配置页面。你需要：

### 1️⃣ 注意你的应用地址

```
https://jinyang756.pythonanywhere.com
```

### 2️⃣ 记下虚拟环境路径

通常是：
```
/home/jinyang756/.virtualenvs/
```

### 3️⃣ 找到 WSGI configuration file

在配置页面中找到这一行：
```
WSGI configuration file: /var/www/jinyang756_pythonanywhere_com_wsgi.py
```

点击这个文件路径，会打开编辑窗口。

---

## 🚀 创建后立即执行

Web 应用创建后，立即在 **Bash Console** 中执行：

### 第 1 步：克隆代码

```bash
cd /home/jinyang756
git clone https://github.com/jinyang756/api-aggregator.git
cd api-aggregator
```

### 第 2 步：创建虚拟环境

```bash
mkvirtualenv --python=/usr/bin/python3.10 api-hub-mysql
workon api-hub-mysql
pip install -r requirements.txt
```

### 第 3 步：编辑 WSGI 文件

1. 回到 Web 应用配置页面
2. 找到 **WSGI configuration file**
3. 点击文件路径进入编辑
4. **全部删除**，替换为以下代码：

```python
import sys
import os

# 添加项目路径
path = '/home/jinyang756/api-aggregator'
if path not in sys.path:
    sys.path.append(path)

# 激活虚拟环境
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

# 导入应用
from backend.app_mysql import app as application
```

5. 点击 **"Save"** 保存

### 第 4 步：配置静态文件

在同一个配置页面，找到 **Static files** 部分。

点击 **"Add a new static file mapping"**，输入：

| 项目 | 值 |
|------|-----|
| URL | `/static/` |
| Directory | `/home/jinyang756/api-aggregator/frontend/static` |

点击 **"Save"**

### 第 5 步：重启应用

在配置页面顶部，点击绿色的 **"Reload jinyang756.pythonanywhere.com"** 按钮

---

## ✅ 验证部署成功

### 访问应用

```
https://jinyang756.pythonanywhere.com
```

应该看到 Free API Hub 首页。

### 初始化数据库

访问：
```
https://jinyang756.pythonanywhere.com/api/init_sample_data
```

应该返回：
```json
{"success": true, "message": "Sample data initialized"}
```

### 测试 API

```
https://jinyang756.pythonanywhere.com/api/apis
https://jinyang756.pythonanywhere.com/api/categories
```

---

## 🎯 完整检查清单

Web 应用创建阶段：
- [ ] 选择了 "Manual configuration (including virtualenvs)"
- [ ] 选择了 Python 3.10
- [ ] Web 应用已创建

部署阶段：
- [ ] 克隆代码到 `/home/jinyang756/api-aggregator`
- [ ] 创建虚拟环境 `api-hub-mysql`
- [ ] 安装依赖包 `pip install -r requirements.txt`
- [ ] WSGI 文件已编辑并保存
- [ ] 静态文件已映射
- [ ] 应用已 Reload

验证阶段：
- [ ] 主页可访问
- [ ] `/api/init_sample_data` 可访问
- [ ] 数据库已初始化
- [ ] API 端点正常工作

---

## 🐛 常见问题

### Q: 我不小心选了 Flask 怎么办？

A: 不用重新创建。完成后你仍然可以：
1. 进入 Web 应用配置
2. 编辑 WSGI 文件
3. 更改虚拟环境路径
4. 点击 Reload

### Q: 虚拟环境路径不对怎么办？

A: 在 Bash Console 中确认：
```bash
ls /home/jinyang756/.virtualenvs/api-hub-mysql/
```

如果存在，确保 WSGI 文件中的路径正确。

### Q: 502 错误？

A: 查看日志：
1. Web 应用配置 → "Log files"
2. 查看 "Error log" 和 "Server error log"
3. 确认错误信息

---

## 📞 你的信息速查

```
PythonAnywhere 账户: jinyang756
应用地址: https://jinyang756.pythonanywhere.com
项目目录: /home/jinyang756/api-aggregator
虚拟环境: /home/jinyang756/.virtualenvs/api-hub-mysql
Python 版本: 3.10

数据库:
  主机: jinyang756.mysql.pythonanywhere-services.com
  用户: jinyang756
  密码: Aa123456..
  数据库: jinyang756$api-aggregator
```

---

## 🚀 立即开始！

1. ✅ 选择 **"Manual configuration (including virtualenvs)"**
2. ✅ 选择 **Python 3.10**
3. ✅ 点击创建
4. ✅ 然后按照本指南的 "创建后立即执行" 部分操作

**预计总耗时：20 分钟**

---

**下一步？** 创建完 Web 应用后，回到 Bash Console 执行克隆和部署命令。

祝部署顺利！🎉
