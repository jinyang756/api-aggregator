#!/usr/bin/env python
"""
数据库备份脚本
在 PythonAnywhere 的 Scheduled tasks 中使用
"""

import os
import shutil
import sqlite3
from datetime import datetime

def backup_database():
    """备份数据库文件"""
    
    # 数据库文件路径
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'api_database.db')
    
    # 备份目录
    backup_dir = os.path.join(os.path.dirname(__file__), 'data', 'backups')
    
    # 创建备份目录（如果不存在）
    os.makedirs(backup_dir, exist_ok=True)
    
    # 生成备份文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f'api_database_backup_{timestamp}.db')
    
    try:
        # 备份数据库
        shutil.copy2(db_path, backup_path)
        print(f"✓ 数据库备份成功: {backup_path}")
        
        # 清理旧备份（保留最近 7 个）
        backups = sorted([f for f in os.listdir(backup_dir) if f.startswith('api_database_backup_')])
        if len(backups) > 7:
            for old_backup in backups[:-7]:
                old_path = os.path.join(backup_dir, old_backup)
                os.remove(old_path)
                print(f"✓ 删除旧备份: {old_backup}")
        
        return True
        
    except Exception as e:
        print(f"✗ 备份失败: {e}")
        return False

if __name__ == '__main__':
    backup_database()
