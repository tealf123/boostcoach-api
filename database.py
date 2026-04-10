"""
Database initialization and management
SQLite for MVP
"""

import sqlite3
import os
from contextlib import contextmanager

DATABASE = 'boostcoach.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_db_cursor():
    """Context manager for database operations"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def init_db():
    """Initialize database schema"""
    if os.path.exists(DATABASE):
        return  # Already initialized
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Analyses table (replay processing results)
    cursor.execute('''
        CREATE TABLE analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            replay_filename TEXT NOT NULL,
            replay_raw_path TEXT NOT NULL,
            parsed_data TEXT,
            coaching_report TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    
    # Conversations table (Q&A sessions)
    cursor.execute('''
        CREATE TABLE conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_id INTEGER NOT NULL,
            user_message TEXT NOT NULL,
            coach_response TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(analysis_id) REFERENCES analyses(id)
        )
    ''')
    
    conn.commit()
    conn.close()
