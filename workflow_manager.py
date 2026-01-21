"""
Workflow Manager
================
Manages unlimited dynamic workflows
"""

import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Optional
import schedule


class WorkflowManager:
    """Manages multiple workflows dynamically"""
    
    def __init__(self, db_path="automation.db"):
        self.db_path = db_path
        self._init_workflows_table()
    
    def _init_workflows_table(self):
        """Initialize workflows table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workflows (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                type TEXT NOT NULL,
                config TEXT NOT NULL,
                schedule TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_run TIMESTAMP,
                total_runs INTEGER DEFAULT 0,
                successful_runs INTEGER DEFAULT 0,
                failed_runs INTEGER DEFAULT 0
            )
        ''')
        
        # Workflow execution history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workflow_executions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                workflow_id INTEGER,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                status TEXT,
                result TEXT,
                error TEXT,
                FOREIGN KEY (workflow_id) REFERENCES workflows(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_workflow(self, name: str, description: str, workflow_type: str,
                       config: Dict, schedule_config: Dict = None) -> int:
        """Create a new workflow"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO workflows (name, description, type, config, schedule, status)
            VALUES (?, ?, ?, ?, ?, 'active')
        ''', (
            name,
            description,
            workflow_type,
            json.dumps(config),
            json.dumps(schedule_config) if schedule_config else None
        ))
        
        workflow_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return workflow_id
    
    def get_workflow(self, workflow_id: int = None, name: str = None) -> Optional[Dict]:
        """Get a workflow by ID or name"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if workflow_id:
            cursor.execute('SELECT * FROM workflows WHERE id = ?', (workflow_id,))
        elif name:
            cursor.execute('SELECT * FROM workflows WHERE name = ?', (name,))
        else:
            conn.close()
            return None
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        columns = ['id', 'name', 'description', 'type', 'config', 'schedule', 
                  'status', 'created_at', 'updated_at', 'last_run', 
                  'total_runs', 'successful_runs', 'failed_runs']
        
        workflow = dict(zip(columns, row))
        workflow['config'] = json.loads(workflow['config'])
        if workflow['schedule']:
            workflow['schedule'] = json.loads(workflow['schedule'])
        
        return workflow
    
    def list_workflows(self, status: str = None) -> List[Dict]:
        """List all workflows"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status:
            cursor.execute('SELECT * FROM workflows WHERE status = ? ORDER BY created_at DESC', (status,))
        else:
            cursor.execute('SELECT * FROM workflows ORDER BY created_at DESC')
        
        rows = cursor.fetchall()
        conn.close()
        
        columns = ['id', 'name', 'description', 'type', 'config', 'schedule', 
                  'status', 'created_at', 'updated_at', 'last_run', 
                  'total_runs', 'successful_runs', 'failed_runs']
        
        workflows = []
        for row in rows:
            workflow = dict(zip(columns, row))
            workflow['config'] = json.loads(workflow['config'])
            if workflow['schedule']:
                workflow['schedule'] = json.loads(workflow['schedule'])
            workflows.append(workflow)
        
        return workflows
    
    def update_workflow(self, workflow_id: int, **kwargs):
        """Update workflow fields"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        fields = []
        values = []
        
        for key, value in kwargs.items():
            if key in ['config', 'schedule'] and isinstance(value, dict):
                value = json.dumps(value)
            fields.append(f"{key} = ?")
            values.append(value)
        
        fields.append("updated_at = CURRENT_TIMESTAMP")
        values.append(workflow_id)
        
        query = f"UPDATE workflows SET {', '.join(fields)} WHERE id = ?"
        cursor.execute(query, values)
        
        conn.commit()
        conn.close()
    
    def pause_workflow(self, workflow_id: int):
        """Pause a workflow"""
        self.update_workflow(workflow_id, status='paused')
    
    def resume_workflow(self, workflow_id: int):
        """Resume a workflow"""
        self.update_workflow(workflow_id, status='active')
    
    def delete_workflow(self, workflow_id: int):
        """Delete a workflow"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM workflows WHERE id = ?', (workflow_id,))
        cursor.execute('DELETE FROM workflow_executions WHERE workflow_id = ?', (workflow_id,))
        
        conn.commit()
        conn.close()
    
    def log_execution(self, workflow_id: int, status: str, 
                     result: Dict = None, error: str = None) -> int:
        """Log a workflow execution"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO workflow_executions 
            (workflow_id, completed_at, status, result, error)
            VALUES (?, CURRENT_TIMESTAMP, ?, ?, ?)
        ''', (
            workflow_id,
            status,
            json.dumps(result) if result else None,
            error
        ))
        
        execution_id = cursor.lastrowid
        
        # Update workflow stats
        if status == 'success':
            cursor.execute('''
                UPDATE workflows 
                SET last_run = CURRENT_TIMESTAMP,
                    total_runs = total_runs + 1,
                    successful_runs = successful_runs + 1
                WHERE id = ?
            ''', (workflow_id,))
        else:
            cursor.execute('''
                UPDATE workflows 
                SET last_run = CURRENT_TIMESTAMP,
                    total_runs = total_runs + 1,
                    failed_runs = failed_runs + 1
                WHERE id = ?
            ''', (workflow_id,))
        
        conn.commit()
        conn.close()
        
        return execution_id
    
    def get_execution_history(self, workflow_id: int, limit: int = 10) -> List[Dict]:
        """Get execution history for a workflow"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM workflow_executions 
            WHERE workflow_id = ? 
            ORDER BY started_at DESC 
            LIMIT ?
        ''', (workflow_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        columns = ['id', 'workflow_id', 'started_at', 'completed_at', 
                  'status', 'result', 'error']
        
        executions = []
        for row in rows:
            execution = dict(zip(columns, row))
            if execution['result']:
                execution['result'] = json.loads(execution['result'])
            executions.append(execution)
        
        return executions
    
    def get_stats(self) -> Dict:
        """Get overall workflow statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Total workflows
        cursor.execute('SELECT COUNT(*) FROM workflows')
        stats['total_workflows'] = cursor.fetchone()[0]
        
        # Active workflows
        cursor.execute("SELECT COUNT(*) FROM workflows WHERE status = 'active'")
        stats['active_workflows'] = cursor.fetchone()[0]
        
        # Paused workflows
        cursor.execute("SELECT COUNT(*) FROM workflows WHERE status = 'paused'")
        stats['paused_workflows'] = cursor.fetchone()[0]
        
        # Total executions
        cursor.execute('SELECT COUNT(*) FROM workflow_executions')
        stats['total_executions'] = cursor.fetchone()[0]
        
        # Success rate
        cursor.execute("SELECT COUNT(*) FROM workflow_executions WHERE status = 'success'")
        successful = cursor.fetchone()[0]
        
        if stats['total_executions'] > 0:
            stats['success_rate'] = round((successful / stats['total_executions']) * 100, 1)
        else:
            stats['success_rate'] = 0
        
        conn.close()
        return stats


def setup_default_workflow():
    """Setup the default video creation workflow"""
    wm = WorkflowManager()
    
    # Check if default workflow exists
    existing = wm.get_workflow(name='pet-video-automation')
    if existing:
        print("✅ Default workflow already exists")
        return existing['id']
    
    # Create default workflow
    workflow_id = wm.create_workflow(
        name='pet-video-automation',
        description='Automated pet and baby animal video creation and posting',
        workflow_type='video_creation',
        config={
            'video_type': 'pet_animals',
            'platforms': ['tiktok', 'instagram', 'youtube'],
            'aspect_ratio': '9:16',
            'idea_bank': 'default'
        },
        schedule_config={
            'times': [
                {'hour': 5, 'minute': 0},
                {'hour': 10, 'minute': 0},
                {'hour': 15, 'minute': 0},
                {'hour': 19, 'minute': 30}
            ]
        }
    )
    
    print(f"✅ Created default workflow (ID: {workflow_id})")
    return workflow_id


if __name__ == '__main__':
    # Test workflow manager
    print("🔧 Setting up workflow manager...")
    workflow_id = setup_default_workflow()
    
    wm = WorkflowManager()
    
    print("\n📊 Workflow stats:")
    stats = wm.get_stats()
    for key, value in stats.items():
        print(f"  • {key}: {value}")
    
    print("\n📋 Active workflows:")
    workflows = wm.list_workflows(status='active')
    for wf in workflows:
        print(f"  • {wf['name']}: {wf['description']}")
    
    print("\n✅ Workflow manager ready!")
