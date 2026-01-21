"""
Enhanced AI Chat Client
========================
Intelligent AI assistant with memory and workflow understanding
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime


class EnhancedAIClient:
    """AI client with workflow context and memory"""
    
    def __init__(self, api_key: str, model: str = "anthropic/claude-3.5-sonnet"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://openrouter.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://your-automation-system.com",
            "X-Title": "Video Automation System"
        }
    
    def chat(self, message: str, conversation_history: List[Dict] = None,
             system_context: Dict = None) -> str:
        """
        Chat with AI with full system context
        
        Args:
            message: User's message
            conversation_history: Previous messages
            system_context: Current system state (workflows, stats, etc.)
        """
        
        # Build system prompt with context
        system_prompt = self._build_system_prompt(system_context)
        
        # Prepare messages
        messages = []
        
        # Add conversation history
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Make API call
        payload = {
            "model": self.model,
            "messages": messages,
            "system": system_prompt,
            "max_tokens": 2000,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            return result['choices'][0]['message']['content']
        
        except Exception as e:
            return f"Error communicating with AI: {str(e)}"
    
    def _build_system_prompt(self, context: Dict = None) -> str:
        """Build comprehensive system prompt with current context"""
        
        base_prompt = """You are an intelligent automation assistant managing a video creation and social media system.

Your capabilities:
- Create and manage unlimited workflows
- Generate AI videos using Sora
- Post to TikTok, Instagram, YouTube
- Analyze performance and optimize
- Remember all past conversations and decisions

You communicate in a friendly, helpful way and take action when asked. When users request something, you:
1. Confirm you understand
2. Execute the action
3. Report the result clearly

Current system overview:"""
        
        if context:
            # Add current workflows
            if 'workflows' in context:
                base_prompt += f"\n\nActive Workflows ({len(context['workflows'])}):"
                for wf in context['workflows']:
                    base_prompt += f"\n- {wf['name']}: {wf['description']}"
                    base_prompt += f" (Status: {wf['status']}, Runs: {wf['total_runs']})"
            
            # Add statistics
            if 'stats' in context:
                stats = context['stats']
                base_prompt += f"\n\nSystem Statistics:"
                base_prompt += f"\n- Total workflows: {stats.get('total_workflows', 0)}"
                base_prompt += f"\n- Total executions: {stats.get('total_executions', 0)}"
                base_prompt += f"\n- Success rate: {stats.get('success_rate', 0)}%"
            
            # Add recent activity
            if 'recent_videos' in context:
                base_prompt += f"\n\nRecent Videos: {len(context['recent_videos'])} created"
        
        base_prompt += """\n\nWhen users ask you to create workflows, modify settings, or take actions:
- Be proactive and execute immediately
- Provide clear confirmation of what you did
- Offer to show results or make adjustments
- Remember preferences for future interactions

Key Actions You Can Take:
1. CREATE WORKFLOW - When user describes a new automation idea
2. MODIFY WORKFLOW - Adjust schedules, settings, platforms
3. PAUSE/RESUME - Control workflow execution
4. ANALYZE - Review performance and suggest improvements
5. DEBUG - Fix issues and explain problems

Always be helpful, clear, and action-oriented."""
        
        return base_prompt
    
    def generate_workflow_config(self, user_description: str) -> Dict:
        """
        Generate workflow configuration from natural language
        
        Example: "Create videos about puppies playing, post 3x daily"
        Returns: Complete workflow config
        """
        
        prompt = f"""User wants to create this workflow:
"{user_description}"

Generate a JSON workflow configuration with these fields:
- name: short kebab-case name
- description: clear description
- type: workflow type (video_creation, engagement, analytics, etc.)
- config: detailed configuration including:
  - content_type: what content to create
  - platforms: array of platforms (tiktok, instagram, youtube)
  - posting_frequency: how often to post
  - any special settings
- schedule: array of posting times with hour and minute

Return ONLY valid JSON, no explanation."""
        
        response = self.chat(prompt)
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
            else:
                # Fallback: try to parse entire response
                return json.loads(response)
        except:
            # Return error config
            return {
                'error': 'Could not parse workflow configuration',
                'raw_response': response
            }
    
    def analyze_video_performance(self, video_data: List[Dict]) -> str:
        """Analyze video performance and provide insights"""
        
        prompt = f"""Analyze this video performance data and provide insights:

{json.dumps(video_data, indent=2)}

Provide:
1. Key patterns and trends
2. Best performing content types
3. Optimal posting times
4. Actionable recommendations

Keep response concise and actionable."""
        
        return self.chat(prompt)
    
    def debug_error(self, error_log: str, workflow_config: Dict) -> str:
        """Help debug workflow errors"""
        
        prompt = f"""A workflow encountered this error:

Error: {error_log}

Workflow config:
{json.dumps(workflow_config, indent=2)}

Please:
1. Identify the root cause
2. Explain in simple terms
3. Suggest a fix
4. Provide any configuration changes needed

Keep explanation clear for non-technical users."""
        
        return self.chat(prompt)


class ConversationManager:
    """Manages conversation history and context"""
    
    def __init__(self, db_path="automation.db"):
        self.db_path = db_path
        self._init_conversations_table()
    
    def _init_conversations_table(self):
        """Initialize conversations table"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                context TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_message(self, session_id: str, role: str, content: str, context: Dict = None):
        """Add message to conversation history"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO conversations (session_id, role, content, context)
            VALUES (?, ?, ?, ?)
        ''', (session_id, role, content, json.dumps(context) if context else None))
        
        conn.commit()
        conn.close()
    
    def get_conversation(self, session_id: str, limit: int = 20) -> List[Dict]:
        """Get conversation history"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT role, content, timestamp, context 
            FROM conversations 
            WHERE session_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', (session_id, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Reverse to get chronological order
        messages = []
        for row in reversed(rows):
            message = {
                'role': row[0],
                'content': row[1],
                'timestamp': row[2]
            }
            if row[3]:
                message['context'] = json.loads(row[3])
            messages.append(message)
        
        return messages
    
    def clear_conversation(self, session_id: str):
        """Clear conversation history"""
        import sqlite3
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM conversations WHERE session_id = ?', (session_id,))
        conn.commit()
        conn.close()


if __name__ == '__main__':
    # Test AI client
    print("🤖 Testing AI client...")
    
    # This will use the OpenRouter key from credential manager
    from credential_manager import CredentialManager
    cm = CredentialManager()
    
    openrouter_key = cm.get_credential('openrouter')
    if not openrouter_key:
        print("❌ No OpenRouter key found. Run credential_manager.py first.")
        exit(1)
    
    client = EnhancedAIClient(openrouter_key)
    
    # Test chat
    response = client.chat("Hello! I want to create videos about puppies. Can you help?")
    print(f"\n🤖 AI: {response}\n")
    
    print("✅ AI client ready!")
