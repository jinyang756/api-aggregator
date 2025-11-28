"""
数据库抽象层 - 支持 SQLite 和 MySQL
"""

import os
import sqlite3
import pymysql
from datetime import datetime
from typing import List, Dict, Any, Optional


class Database:
    """数据库基类"""
    
    def __init__(self):
        self.db_type = os.environ.get('DB_TYPE', 'sqlite').lower()
        
    def execute(self, query: str, params: tuple = ()) -> Any:
        """执行查询"""
        raise NotImplementedError
    
    def execute_many(self, query: str, params: List[tuple]) -> int:
        """批量执行"""
        raise NotImplementedError
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """获取单条记录"""
        raise NotImplementedError
    
    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """获取所有记录"""
        raise NotImplementedError
    
    def init_tables(self):
        """初始化表结构"""
        raise NotImplementedError


class SQLiteDatabase(Database):
    """SQLite 数据库实现"""
    
    def __init__(self):
        super().__init__()
        self.db_path = os.environ.get('DB_PATH', 'data/api_database.db')
        os.makedirs(os.path.dirname(self.db_path) or '.', exist_ok=True)
    
    def _get_connection(self):
        """获取数据库连接"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def execute(self, query: str, params: tuple = ()) -> int:
        """执行增删改"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid
        finally:
            conn.close()
    
    def execute_many(self, query: str, params: List[tuple]) -> int:
        """批量执行"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.executemany(query, params)
            conn.commit()
            return cursor.rowcount
        finally:
            conn.close()
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """获取单条记录"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
        finally:
            conn.close()
    
    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """获取所有记录"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        finally:
            conn.close()
    
    def init_tables(self):
        """初始化表结构"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            
            # 创建分类表
            cursor.execute('''CREATE TABLE IF NOT EXISTS categories
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name TEXT NOT NULL UNIQUE,
                             description TEXT,
                             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            
            # 创建API表
            cursor.execute('''CREATE TABLE IF NOT EXISTS apis
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             name TEXT NOT NULL,
                             description TEXT,
                             category TEXT NOT NULL,
                             url TEXT,
                             auth_required BOOLEAN DEFAULT 0,
                             api_key_instructions TEXT,
                             documentation_url TEXT,
                             rate_limit TEXT,
                             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                             updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                             FOREIGN KEY(category) REFERENCES categories(name))''')
            
            # 创建收藏表
            cursor.execute('''CREATE TABLE IF NOT EXISTS favorites
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                             user_id TEXT NOT NULL,
                             api_id INTEGER NOT NULL,
                             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                             UNIQUE(user_id, api_id),
                             FOREIGN KEY(api_id) REFERENCES apis(id) ON DELETE CASCADE)''')
            
            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_apis_category ON apis(category)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_apis_name ON apis(name)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_favorites_user ON favorites(user_id)')
            
            conn.commit()
            print("✓ SQLite 表结构创建成功")
        finally:
            conn.close()


class MySQLDatabase(Database):
    """MySQL 数据库实现"""
    
    def __init__(self):
        super().__init__()
        self.host = os.environ.get('DB_HOST')
        self.port = int(os.environ.get('DB_PORT', 3306))
        self.user = os.environ.get('DB_USER')
        self.password = os.environ.get('DB_PASSWORD')
        self.database = os.environ.get('DB_NAME')
        
        if not all([self.host, self.user, self.password, self.database]):
            raise ValueError("MySQL 配置不完整，请检查环境变量")
    
    def _get_connection(self):
        """获取数据库连接"""
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    
    def execute(self, query: str, params: tuple = ()) -> int:
        """执行增删改"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()
    
    def execute_many(self, query: str, params: List[tuple]) -> int:
        """批量执行"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.executemany(query, params)
                conn.commit()
                return cursor.rowcount
        finally:
            conn.close()
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """获取单条记录"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchone()
        finally:
            conn.close()
    
    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """获取所有记录"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        finally:
            conn.close()
    
    def init_tables(self):
        """初始化表结构"""
        conn = self._get_connection()
        try:
            with conn.cursor() as cursor:
                
                # 创建分类表
                cursor.execute('''CREATE TABLE IF NOT EXISTS categories (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(100) NOT NULL UNIQUE,
                                description TEXT,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                INDEX idx_name (name)
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci''')
                
                # 创建API表
                cursor.execute('''CREATE TABLE IF NOT EXISTS apis (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(200) NOT NULL,
                                description TEXT,
                                category VARCHAR(100) NOT NULL,
                                url VARCHAR(500),
                                auth_required BOOLEAN DEFAULT 0,
                                api_key_instructions TEXT,
                                documentation_url VARCHAR(500),
                                rate_limit VARCHAR(100),
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                                FOREIGN KEY(category) REFERENCES categories(name),
                                INDEX idx_category (category),
                                INDEX idx_name (name)
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci''')
                
                # 创建收藏表
                cursor.execute('''CREATE TABLE IF NOT EXISTS favorites (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                user_id VARCHAR(100) NOT NULL,
                                api_id INT NOT NULL,
                                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                UNIQUE KEY unique_user_api (user_id, api_id),
                                FOREIGN KEY(api_id) REFERENCES apis(id) ON DELETE CASCADE,
                                INDEX idx_user (user_id)
                            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci''')
                
                conn.commit()
                print("✓ MySQL 表结构创建成功")
        finally:
            conn.close()


def get_database() -> Database:
    """获取数据库实例（工厂函数）"""
    db_type = os.environ.get('DB_TYPE', 'sqlite').lower()
    
    if db_type == 'mysql':
        return MySQLDatabase()
    else:
        return SQLiteDatabase()
