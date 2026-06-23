"""
数据库工具模块 - 用于存储用户生成的文案和PPT历史记录
使用SQLite，Streamlit Cloud上数据存储在用户目录
"""

import sqlite3
import os
import json
from datetime import datetime

# 数据库路径 - 放在用户home目录下，Streamlit Cloud也能持久化
DB_PATH = os.path.join(os.path.expanduser("~"), "ai_tools_history.db")


def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库表"""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tool_type TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            extra_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def save_record(tool_type, title, content, extra_data=None):
    """保存一条生成记录"""
    conn = get_connection()
    conn.execute(
        "INSERT INTO history (tool_type, title, content, extra_data) VALUES (?, ?, ?, ?)",
        (tool_type, title, content, json.dumps(extra_data, ensure_ascii=False) if extra_data else None)
    )
    conn.commit()
    conn.close()


def get_records(tool_type=None, limit=50):
    """查询历史记录"""
    conn = get_connection()
    if tool_type:
        rows = conn.execute(
            "SELECT * FROM history WHERE tool_type = ? ORDER BY created_at DESC LIMIT ?",
            (tool_type, limit)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM history ORDER BY created_at DESC LIMIT ?",
            (limit,)
        ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_record(record_id):
    """删除一条记录"""
    conn = get_connection()
    conn.execute("DELETE FROM history WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()


def get_stats():
    """获取统计信息"""
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM history").fetchone()[0]
    copy_count = conn.execute("SELECT COUNT(*) FROM history WHERE tool_type = 'copywriting'").fetchone()[0]
    ppt_count = conn.execute("SELECT COUNT(*) FROM history WHERE tool_type = 'ppt'").fetchone()[0]
    conn.close()
    return {"total": total, "copywriting": copy_count, "ppt": ppt_count}


# 模块加载时自动初始化
init_db()
