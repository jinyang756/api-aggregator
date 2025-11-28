# ✅ PythonAnywhere Web 应用已创建 - 后续配置

## 🎉 Web 应用创建完成

你的 Web 应用地址：
```
https://jinyang756.pythonanywhere.com
```

---

## 📋 现在需要做的事（3 个步骤）

### 第 1 步：克隆代码并创建虚拟环境

**在 PythonAnywhere Bash Console 执行：**

```bash
cd /home/jinyang756
git clone https://github.com/jinyang756/api-aggregator.git
cd api-aggregator

# 创建虚拟环境
mkvirtualenv --python=/usr/bin/python3.10 api-hub-mysql
workon api-hub-mysql
pip install -r requirements.txt
```

### 第 2 步：配置 WSGI 文件

在当前页面（Web 应用配置）找到：
```
WSGI 配置文件: /var/www/jinyang756_pythonanywhere_com_wsgi.py
```

**点击这个文件路径** → 会打开编辑窗口

**全部删除**原有内容，复制粘贴以下代码：

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

**点击 "Save" 保存**

### 第 3 步：配置静态文件

在配置页面找到：
```
静态文件
URL          目录
输入 URL     输入路径
```

**点击 "输入 URL"** 输入：
```
/static/
```

**点击 "输入路径"** 输入：
```
/home/jinyang756/api-aggregator/frontend/static
```

**点击 "Save"**

---

## 🔄 重新加载应用

完成上面所有配置后，**返回配置页面顶部**，找到：

```
重新加载 jinyang756.pythonanywhere.com
```

**点击绿色的 Reload 按钮**

---

## ✅ 初始化数据库

等待 30 秒让应用重启，然后在浏览器中访问：

```
https://jinyang756.pythonanywhere.com/api/init_sample_data
```

应该看到：
```json
{"success": true, "message": "Sample data initialized"}
```

---

## 🌐 验证部署

### 1. 访问主页
```
https://jinyang756.pythonanywhere.com
```

应该看到 **Free API Hub** 首页

### 2. 测试 API
```
https://jinyang756.pythonanywhere.com/api/apis
https://jinyang756.pythonanywhere.com/api/categories
```

应该返回 JSON 数据

### 3. 搜索测试
```
https://jinyang756.pythonanywhere.com/api/apis?search=weather
```

---

## 🐛 如果看到 502 错误

### 快速诊断

1. **查看日志**
   - 在配置页面找到 **日志文件**
   - 点击 **错误日志** 查看错误信息

2. **常见错误和解决方案**

| 错误信息 | 原因 | 解决方案 |
|---------|------|---------|
| `ModuleNotFoundError: No module named 'backend'` | 虚拟环境未激活或路径错误 | 检查 WSGI 中的 venv 路径 |
| `Can't connect to MySQL server` | 数据库凭证错误 | 验证数据库主机、用户、密码 |
| `No such file or directory: activate_this.py` | 虚拟环境不存在 | 重新运行 `mkvirtualenv` 命令 |
| `ModuleNotFoundError: No module named 'pymysql'` | 依赖未安装 | 运行 `pip install -r requirements.txt` |

3. **重新部署**

```bash
cd /home/jinyang756/api-aggregator
workon api-hub-mysql
pip install -r requirements.txt --upgrade
# 然后在 Web 配置页面点击 Reload
```

---

## 📝 配置检查清单

Web 应用创建：
- [x] Web 应用已创建
- [x] 应用地址：https://jinyang756.pythonanywhere.com
- [x] Python 版本：3.10

代码部署：
- [ ] 代码已克隆到 `/home/jinyang756/api-aggregator`
- [ ] 虚拟环境已创建：`api-hub-mysql`
- [ ] 依赖已安装

配置阶段：
- [ ] WSGI 文件已编辑和保存
- [ ] 静态文件已映射（`/static/` → `/home/jinyang756/api-aggregator/frontend/static`）
- [ ] 应用已 Reload

验证阶段：
- [ ] 主页可访问
- [ ] `/api/init_sample_data` 可访问
- [ ] 数据库已初始化
- [ ] API 返回数据

---

## 🔐 安全设置

### 立即修改 SECRET_KEY

**不要** 使用默认的 `jinyang756-secret-key-2025`

1. 生成强密码（至少 32 个字符）
2. 编辑 WSGI 文件
3. 找到这行：
   ```python
   os.environ['SECRET_KEY'] = 'jinyang756-secret-key-2025'
   ```
4. 改为：
   ```python
   os.environ['SECRET_KEY'] = '你生成的强密码'
   ```
5. 保存并 Reload

### 强制 HTTPS（推荐）

在配置页面找到 **安全** 部分：
- ☑️ 选中 **强制 HTTPS**

---

## 📊 监控和维护

### 定期检查日志

访问配置页面：
- **访问日志**：`jinyang756.pythonanywhere.com.access.log`
- **错误日志**：`jinyang756.pythonanywhere.com.error.log`
- **服务器日志**：`jinyang756.pythonanywhere.com.server.log`

### 定期备份数据库

```bash
mysql -h jinyang756.mysql.pythonanywhere-services.com -u jinyang756 -p
# 输入密码：Aa123456..

# 然后备份
mysqldump -h jinyang756.mysql.pythonanywhere-services.com \
          -u jinyang756 -p \
          jinyang756$api-aggregator > backup-$(date +%Y%m%d).sql
```

### 每 3 个月登录一次

⚠️ **重要：** 免费账户需要每 3 个月登录一次并点击刷新按钮

```
本网站将于 2026年2月28日 关闭
```

在关闭前一周会收到邮件提醒。

---

## 💡 后续更新代码

当你在 GitHub 上更新代码时：

```bash
cd /home/jinyang756/api-aggregator
workon api-hub-mysql
git pull origin main
pip install -r requirements.txt
# 然后在 Web 配置页面点击 Reload
```

---

## 📞 常用命令速查

| 需求 | 命令 |
|------|------|
| 进入项目目录 | `cd /home/jinyang756/api-aggregator` |
| 激活虚拟环境 | `workon api-hub-mysql` |
| 安装/更新依赖 | `pip install -r requirements.txt --upgrade` |
| 连接数据库 | `mysql -h jinyang756.mysql.pythonanywhere-services.com -u jinyang756 -p` |
| 查看 Web 日志 | Web 配置 → 日志文件 |
| 重启应用 | Web 配置 → 点击 Reload 按钮 |

---

## 🎯 预期结果

完成所有配置后：

✅ **主页加载正常**
```
https://jinyang756.pythonanywhere.com
```

✅ **API 正常工作**
```
https://jinyang756.pythonanywhere.com/api/apis
```

✅ **数据库已初始化**
```
https://jinyang756.pythonanywhere.com/api/init_sample_data
```

✅ **HTTPS 已启用**
```
https://jinyang756.pythonanywhere.com
```

---

## 📚 相关文档

- `PYTHONANYWHERE_DEPLOYMENT_GUIDE.md` - 完整部署指南
- `MYSQL_QUICK_REFERENCE.md` - MySQL 快速参考
- `FINAL_DEPLOYMENT_GUIDE.md` - 详细故障排查

---

## 🚀 现在就开始！

**按照上面的 3 个配置步骤执行，你的应用将在 5-10 分钟内上线！**

有任何问题，查看 `PYTHONANYWHERE_DEPLOYMENT_GUIDE.md` 中的故障排查部分。

**祝部署顺利！** 🎉
