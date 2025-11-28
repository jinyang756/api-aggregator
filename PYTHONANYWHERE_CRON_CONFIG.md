# ⏰ PythonAnywhere + Cron-Job.org 配置指南

## 🎯 目标

让你的 Free API Hub 应用每天自动更新数据，无需升级付费版。

---

## 📋 配置步骤

### 第 1 步：更新 PythonAnywhere 上的代码

在 PythonAnywhere Bash Console 执行：

```bash
cd /home/jinyang756/api-aggregator
workon api-hub-mysql
git pull origin main
pip install -r requirements.txt
```

### 第 2 步：更新 WSGI 文件

在 PythonAnywhere 配置页面，编辑 WSGI 文件 `/var/www/jinyang756_pythonanywhere_com_wsgi.py`

在所有环境变量下方添加：

```python
os.environ['UPDATE_API_KEY'] = 'your-secure-update-key-12345-change-this'
```

**完整示例：**

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
os.environ['UPDATE_API_KEY'] = 'your-secure-update-key-12345-change-this'  # ← 新增此行
from backend.app_mysql import app as application
```

点击 **Save**

### 第 3 步：重新加载应用

在 PythonAnywhere 配置页面，点击绿色的 **Reload** 按钮

### 第 4 步：测试新端点

访问（需要用正确的 API 密钥）：

```bash
# 使用 curl 测试
curl -X POST https://jinyang756.pythonanywhere.com/api/update_data \
  -H "X-API-Key: your-secure-update-key-12345-change-this"
```

或在浏览器中用 Python 脚本测试：

```python
import requests

response = requests.post(
    'https://jinyang756.pythonanywhere.com/api/update_data',
    headers={'X-API-Key': 'your-secure-update-key-12345-change-this'}
)
print(response.json())
```

**预期响应：**
```json
{
  "message": "Data updated successfully",
  "success": true,
  "timestamp": "2025-11-29T14:30:45.123456",
  "database_type": "mysql"
}
```

---

## 🌍 注册 Cron-Job.org

### 步骤 1：访问网站

打开浏览器访问：https://cron-job.org/

### 步骤 2：创建账户

1. 点击 **Sign Up**
2. 输入邮箱地址
3. 设置密码
4. 检查邮箱进行验证
5. 登录账户

---

## ⚙️ 在 Cron-Job.org 创建任务

### 步骤 1：进入后台

登录后，点击菜单中的 **Cronjobs** 或 **My cronjobs**

### 步骤 2：创建新任务

点击 **+ Create cronjob** 或类似的按钮

### 步骤 3：填写任务详情

| 字段 | 值 |
|------|---|
| **Title** | `Free API Hub - Update Data` |
| **Enabled** | ✅ 勾选 |
| **URL** | `https://jinyang756.pythonanywhere.com/api/update_data` |
| **HTTP Method** | `POST` |
| **Execution time** | 每天凌晨 2:00 AM |

### 步骤 4：添加认证头

在 **HTTP Headers** 或 **Custom Headers** 部分，添加：

```
X-API-Key: your-secure-update-key-12345-change-this
```

**注意：** 必须与 WSGI 文件中的密钥完全一致！

### 步骤 5：保存任务

点击 **Create** 或 **Save** 按钮

---

## 🧪 测试定时任务

### 方式 1：立即执行测试

1. 在 cron-job.org 找到你创建的任务
2. 点击 **Execute** 或 **Run Now** 按钮
3. 等待 10-30 秒
4. 查看 **Execution result**，应该看到 `200 OK` 或类似的成功信息

### 方式 2：查看执行日志

1. 点击任务名称
2. 查看 **Execution history**
3. 应该看到类似的记录：
   ```
   ✓ 2025-11-29 14:30:45 - HTTP 200 - Success
   ```

### 方式 3：查看 PythonAnywhere 日志

1. 进入 PythonAnywhere 配置页面
2. 点击 **Log files** 部分
3. 查看 **Access log** - 应该有 POST 请求记录
4. 查看 **Error log** - 应该没有错误

---

## ⏰ 自定义执行时间

### 常见的执行时间设置

| 需求 | 配置 |
|------|------|
| **每天早上 8 点** | 08:00 |
| **每天中午 12 点** | 12:00 |
| **每天晚上 6 点** | 18:00 |
| **每天凌晨 2 点** | 02:00 |
| **每 12 小时** | 多个 cron job (02:00 和 14:00) |
| **每 6 小时** | 多个 cron job (02:00, 08:00, 14:00, 20:00) |

---

## 🔐 安全最佳实践

### 1. 使用强密钥

```python
# ❌ 弱密钥
UPDATE_API_KEY = '123456'
UPDATE_API_KEY = 'password'

# ✅ 强密钥
UPDATE_API_KEY = 'abc123def456ghi789jkl012mno345pqr'
UPDATE_API_KEY = 'X9kL2mN4pQ7rS1tU5vW3xY6zAbCd9EfGhIj'
```

### 2. 定期更换密钥

- 建议每 3 个月更换一次
- 更换时需要同时更新 WSGI 文件和 cron-job.org 任务

### 3. 监控执行日志

- 定期检查 cron-job.org 的执行历史
- 查看 PythonAnywhere 的错误日志
- 如果发现异常，立即调查

### 4. 添加请求验证

当前代码已经有基础验证，可以进一步增强：

```python
# 检查请求来源
# 检查请求频率（防止重复调用）
# 添加请求签名（HMAC）
```

---

## 📊 监控和维护

### 每周检查清单

- [ ] 查看 cron-job.org 执行历史（是否有失败）
- [ ] 查看 PythonAnywhere 日志（是否有错误）
- [ ] 测试 `/api/update_data` 端点是否正常
- [ ] 验证数据是否有更新

### 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 收到 401 错误 | API 密钥不匹配 | 检查 WSGI 和 cron-job.org 的密钥是否一致 |
| 收到 404 错误 | URL 不正确 | 确认 URL 是 `https://jinyang756.pythonanywhere.com/api/update_data` |
| 收到 500 错误 | 应用错误 | 查看 PythonAnywhere 错误日志 |
| 从未执行过 | 任务被禁用 | 检查 cron-job.org 任务是否启用 |
| 执行但无响应 | 超时 | 检查应用是否在运行，查看日志 |

---

## 🎯 完成检查清单

### 代码部分
- [x] 已在 `backend/app_mysql.py` 添加 `/api/update_data` 端点
- [x] 已创建 `CRON_JOB_SETUP.md` 文档

### PythonAnywhere 部分
- [ ] 已执行 `git pull` 更新代码
- [ ] 已在 WSGI 文件中设置 `UPDATE_API_KEY`
- [ ] 已点击 **Reload** 重新加载应用
- [ ] 已测试 `/api/update_data` 端点成功返回 200

### Cron-Job.org 部分
- [ ] 已创建 cron-job.org 账户
- [ ] 已创建新的 cronjob
- [ ] 已设置 URL 为 `https://jinyang756.pythonanywhere.com/api/update_data`
- [ ] 已在 Headers 中添加 `X-API-Key`
- [ ] 已点击 **Execute** 进行测试
- [ ] 执行结果显示 HTTP 200 成功

---

## 📞 需要帮助？

如果配置过程中遇到问题，检查：

1. **PythonAnywhere 错误日志**
   - https://www.pythonanywhere.com/user/jinyang756/webapps/
   - 点击 Web app
   - 查看 Error log

2. **Cron-Job.org 执行历史**
   - 登录 cron-job.org
   - 点击你的 cronjob
   - 查看最近的执行记录

3. **本地测试**
   - 使用 curl 或 Python requests 测试端点
   - 确保 API 密钥正确

---

**配置完成后，你的应用会每天自动更新数据！** 🎉
