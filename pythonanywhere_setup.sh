#!/bin/bash
# PythonAnywhere 自动部署脚本
# 在 PythonAnywhere Bash Console 中运行：bash pythonanywhere_setup.sh

set -e  # 出错时退出

echo "===== Free API Hub PythonAnywhere 部署脚本 ====="
echo ""

# 变量配置
read -p "请输入你的 PythonAnywhere 用户名: " USERNAME
read -p "请输入项目目录名称 (默认: free-api-hub): " PROJECT_DIR
PROJECT_DIR=${PROJECT_DIR:-free-api-hub}

PROJECT_PATH="/home/$USERNAME/$PROJECT_DIR/api-aggregator"
VENV_NAME="api-hub"

echo ""
echo "📋 配置信息："
echo "  用户名: $USERNAME"
echo "  项目路径: $PROJECT_PATH"
echo "  虚拟环境: $VENV_NAME"
echo ""

# 检查项目是否存在
if [ ! -d "$PROJECT_PATH" ]; then
    echo "❌ 项目目录不存在: $PROJECT_PATH"
    echo ""
    echo "请先上传项目文件到 $PROJECT_DIR 目录"
    exit 1
fi

echo "✓ 项目目录已找到"

# 创建虚拟环境
echo ""
echo "🔧 创建虚拟环境..."
mkvirtualenv --python=/usr/bin/python3.10 $VENV_NAME || workon $VENV_NAME

# 激活虚拟环境
workon $VENV_NAME

# 进入项目目录
cd "$PROJECT_PATH"

# 安装依赖
echo ""
echo "📦 安装依赖包..."
pip install --upgrade pip
pip install -r requirements.txt

# 初始化数据库
echo ""
echo "🗄️  初始化数据库..."
python -c "from backend.app import init_db; init_db(); print('✓ 数据库初始化成功')"

# 显示下一步指示
echo ""
echo "✅ 部署准备完成！"
echo ""
echo "🔗 下一步操作："
echo "  1. 登录 PythonAnywhere 网页控制台"
echo "  2. 转到 Web 应用配置"
echo "  3. 编辑 WSGI 配置文件，使用 pythonanywhere_wsgi.py 的内容"
echo "  4. 在配置中设置静态文件映射："
echo "     URL: /static"
echo "     目录: $PROJECT_PATH/frontend/static"
echo "  5. 点击 Reload 重启应用"
echo ""
echo "🌐 应用地址: https://$USERNAME.pythonanywhere.com"
echo ""
echo "💾 初始化数据库 URL: https://$USERNAME.pythonanywhere.com/api/init_sample_data"
echo ""
