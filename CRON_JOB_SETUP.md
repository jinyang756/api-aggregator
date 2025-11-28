# ⏰ 使用 Cron-Job.org 实现自动定时更新

## 📋 概述

使用免费的 **cron-job.org** 服务，可以让你的 PythonAnywhere 应用每天自动更新 API 数据，无需升级付费版。

---

## 🚀 配置步骤

### 第 1 步：创建更新端点

在你的 Flask 应用中添加一个更新端点，编辑 `backend/app_mysql.py`：

```python
# 在现有路由下方添加以下代码

@app.route('/api/update_data', methods=['POST'])
def update_data():
    """
    更新 API 数据的端点
    需要正确的 API 密钥验证
    """
    # 验证 API 密钥（防止未授权访问）
    api_key = request.headers.get('X-API-Key')
    if api_key != os.environ.get('UPDATE_API_KEY', 'your-secret-update-key'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    try:
        # 这里可以添加数据更新逻辑
        # 例如：调用数据收集脚本或重新初始化数据
        
        # 简单示例：重新初始化示例数据
        db.init_tables()
        
        return jsonify({
            'message': 'Data updated successfully',
            'success': True,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500
```

### 第 2 步：设置环境变量

在 PythonAnywhere 的 WSGI 文件中添加更新密钥：

```python
os.environ['UPDATE_API_KEY'] = 'your-secure-update-key-12345'
```

或在 `.env` 文件中添加：

```env
UPDATE_API_KEY=your-secure-update-key-12345
```

然后重新加载 Web 应用。

### 第 3 步：注册 Cron-Job.org 账户

1. 访问 https://cron-job.org/
2. 点击 **Sign Up** 注册免费账户
3. 用邮箱验证账户

### 第 4 步：创建定时任务

1. 登录 cron-job.org 后台
2. 点击 **Create cronjob**
3. 填写以下信息：

| 字段 | 值 |
|------|---|
| **Title** | `Update Free API Hub Data` |
| **URL** | `https://jinyang756.pythonanywhere.com/api/update_data` |
| **Execution timing** | 每天凌晨 2:00 AM (推荐) |
| **HTTP Method** | `POST` |

### 第 5 步：添加身份验证

在 cron-job.org 的 **HTTP Headers** 部分添加：

```
X-API-Key: your-secure-update-key-12345
```

确保与 WSGI 文件中设置的密钥一致。

### 第 6 步：保存并测试

1. 点击 **Create** 保存
2. 立即点击 **Execute** 测试一次
3. 检查响应状态（应该是 200 OK）

---

## 📊 验证设置

### 方式 1：直接测试端点

使用 curl 命令测试（在本地或 PythonAnywhere Bash Console）：

```bash
curl -X POST https://jinyang756.pythonanywhere.com/api/update_data \
  -H "X-API-Key: your-secure-update-key-12345"
```

### 方式 2：查看 cron-job.org 执行日志

1. 登录 cron-job.org
2. 点击你创建的任务
3. 查看 **Execution history** 和 **HTTP response**

### 方式 3：查看 PythonAnywhere 错误日志

在 PythonAnywhere 配置页面查看：
- 访问日志：`jinyang756.pythonanywhere.com.access.log`
- 错误日志：`jinyang756.pythonanywhere.com.error.log`

---

## ⏰ 推荐的更新计划

| 时间 | 频率 | 优势 |
|------|------|------|
| **每天凌晨 2:00 AM** | 1 次/天 | 用户活跃度低，服务器压力小 |
| **每天上午 10:00 AM** | 1 次/天 | 白天更新，数据更新 |
| **每 12 小时** | 2 次/天 | 数据更新更频繁 |
| **每 6 小时** | 4 次/天 | 适合高频更新需求 |

---

## 🔐 安全建议

1. **使用强密钥**
   ```python
   # ❌ 不好
   UPDATE_API_KEY = '123456'
   
   # ✅ 好
   UPDATE_API_KEY = 'abc123def456ghi789jkl012mno345pqr'
   ```

2. **不要在代码中硬编码**
   - 使用环境变量或 .env 文件
   - 定期更换密钥

3. **限制请求来源**
   - 只允许 cron-job.org 的 IP 地址
   - 在 PythonAnywhere 防火墙设置中配置

4. **添加请求日志**
   ```python
   @app.route('/api/update_data', methods=['POST'])
   def update_data():
       # 记录谁调用了这个端点
       print(f"Update request from {request.remote_addr}")
       # ... 其他代码
   ```

---

## 📝 高级配置

### 添加重试机制

```python
@app.route('/api/update_data', methods=['POST'])
def update_data():
    """带重试的更新端点"""
    api_key = request.headers.get('X-API-Key')
    if api_key != os.environ.get('UPDATE_API_KEY'):
        return jsonify({'error': 'Unauthorized'}), 401
    
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            # 尝试更新数据
            db.init_tables()
            
            return jsonify({
                'message': 'Data updated successfully',
                'success': True,
                'retries': retry_count
            }), 200
        except Exception as e:
            retry_count += 1
            if retry_count >= max_retries:
                return jsonify({
                    'error': str(e),
                    'success': False,
                    'retries': retry_count
                }), 500
```

### 添加邮件通知

```python
import smtplib
from email.mime.text import MIMEText

@app.route('/api/update_data', methods=['POST'])
def update_data():
    """带邮件通知的更新端点"""
    # ... 验证代码 ...
    
    try:
        db.init_tables()
        
        # 发送成功邮件
        send_notification_email("Data update completed successfully")
        
        return jsonify({'success': True}), 200
    except Exception as e:
        # 发送失败邮件
        send_notification_email(f"Data update failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

def send_notification_email(message):
    # 使用你的邮箱服务发送通知
    pass
```

---

## 🐛 常见问题

### Q: 任务执行失败？

**A:** 检查以下几点：
1. ✅ URL 是否正确（包括 HTTPS）
2. ✅ API 密钥是否匹配
3. ✅ PythonAnywhere 应用是否正在运行
4. ✅ 查看错误日志获取详细信息

### Q: 如何改变执行时间？

**A:** 在 cron-job.org 后台编辑任务，修改 **Execution timing** 字段。

### Q: 能否同时执行多个任务？

**A:** 可以！创建多个 cron job，分别在不同时间执行。

### Q: 如何禁用任务？

**A:** 在 cron-job.org 后台找到任务，点击 **Disable** 按钮。

---

## ✅ 完成检查清单

- [ ] 在 `backend/app_mysql.py` 添加 `/api/update_data` 端点
- [ ] 在 WSGI 文件中设置 `UPDATE_API_KEY` 环境变量
- [ ] PythonAnywhere 应用已重新加载
- [ ] 在 cron-job.org 创建账户
- [ ] 创建定时任务
- [ ] 添加 API 密钥到 HTTP Headers
- [ ] 测试端点（cron-job.org Execute）
- [ ] 验证执行日志

---

**现在你的应用可以自动定时更新数据了！** 🎉
