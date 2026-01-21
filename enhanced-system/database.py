"""
Simple Database Module
======================
Tracks all videos, ideas, and workflow runs
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
import os


class Database:
    def __init__(self, db_path="automation.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Videos table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                idea_data TEXT,
                script_data TEXT,
                sora_task_id TEXT,
                video_url TEXT,
                status TEXT,
                posted_tiktok BOOLEAN DEFAULT 0,
                posted_instagram BOOLEAN DEFAULT 0,
                posted_youtube BOOLEAN DEFAULT 0,
                error TEXT
            )
        ''')
        
        # Workflow runs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workflow_runs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                status TEXT,
                video_id INTEGER,
                error TEXT,
                FOREIGN KEY (video_id) REFERENCES videos(id)
            )
        ''')
        
        # Ideas bank table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ideas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slug TEXT UNIQUE,
                data TEXT,
                times_used INTEGER DEFAULT 0,
                last_used TIMESTAMP
            )
        ''')
        
        # System logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                level TEXT,
                message TEXT,
                details TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_video(self, idea_data: Dict, script_data: Dict = None, 
                  sora_task_id: str = None) -> int:
        """Add a new video to database"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO videos (idea_data, script_data, sora_task_id, status)
            VALUES (?, ?, ?, ?)
        ''', (json.dumps(idea_data), 
              json.dumps(script_data) if script_data else None,
              sora_task_id,
              'created'))
        
        video_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return video_id
    
    def update_video(self, video_id: int, **kwargs):
        """Update video fields"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Build update query dynamically
        fields = []
        values = []
        for key, value in kwargs.items():
            fields.append(f"{key} = ?")
            if isinstance(value, (dict, list)):
                values.append(json.dumps(value))
            else:
                values.append(value)
        
        values.append(video_id)
        
        query = f"UPDATE videos SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        
        conn.commit()
        conn.close()
    
    def get_video(self, video_id: int) -> Optional[Dict]:
        """Get video by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM videos WHERE id = ?', (video_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))
    
    def get_recent_videos(self, limit: int = 10) -> List[Dict]:
        """Get recent videos"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM videos 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        
        return [dict(zip(columns, row)) for row in rows]
    
    def add_workflow_run(self, status: str = 'started', 
                        video_id: int = None) -> int:
        """Start a new workflow run"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO workflow_runs (status, video_id)
            VALUES (?, ?)
        ''', (status, video_id))
        
        run_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return run_id
    
    def complete_workflow_run(self, run_id: int, status: str, 
                             video_id: int = None, error: str = None):
        """Complete a workflow run"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE workflow_runs 
            SET completed_at = CURRENT_TIMESTAMP, status = ?, 
                video_id = ?, error = ?
            WHERE id = ?
        ''', (status, video_id, error, run_id))
        
        conn.commit()
        conn.close()
    
    def log(self, level: str, message: str, details: Dict = None):
        """Add a log entry"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO logs (level, message, details)
            VALUES (?, ?, ?)
        ''', (level, message, json.dumps(details) if details else None))
        
        conn.commit()
        conn.close()
    
    def get_logs(self, limit: int = 100, level: str = None) -> List[Dict]:
        """Get recent logs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if level:
            cursor.execute('''
                SELECT * FROM logs 
                WHERE level = ?
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (level, limit))
        else:
            cursor.execute('''
                SELECT * FROM logs 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        
        return [dict(zip(columns, row)) for row in rows]
    
    def get_stats(self) -> Dict:
        """Get system statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        stats = {}
        
        # Total videos
        cursor.execute('SELECT COUNT(*) FROM videos')
        stats['total_videos'] = cursor.fetchone()[0]
        
        # Videos by status
        cursor.execute('SELECT status, COUNT(*) FROM videos GROUP BY status')
        stats['videos_by_status'] = dict(cursor.fetchall())
        
        # Total workflow runs
        cursor.execute('SELECT COUNT(*) FROM workflow_runs')
        stats['total_runs'] = cursor.fetchone()[0]
        
        # Successful runs
        cursor.execute("SELECT COUNT(*) FROM workflow_runs WHERE status = 'completed'")
        stats['successful_runs'] = cursor.fetchone()[0]
        
        # Failed runs
        cursor.execute("SELECT COUNT(*) FROM workflow_runs WHERE status = 'failed'")
        stats['failed_runs'] = cursor.fetchone()[0]
        
        conn.close()
        return stats
