"""
Enhanced Web Application
=========================
Beautiful chat interface with workflow management
"""

from flask import Flask, render_template_string, request, jsonify, session
import threading
import os
import uuid
from datetime import datetime

from credential_manager import CredentialManager
from workflow_manager import WorkflowManager
from workflow_executor import WorkflowExecutor
from ai_client import EnhancedAIClient, ConversationManager
from database import Database
from scheduler import AutomationScheduler


# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'change-this-in-production-' + str(uuid.uuid4()))

# Initialize components
cm = CredentialManager()
wm = WorkflowManager()
executor = WorkflowExecutor()
db = Database()
scheduler = AutomationScheduler()
conv_manager = ConversationManager()

# Initialize AI client
try:
    openrouter_key = cm.get_credential('openrouter')
    if openrouter_key:
        ai_client = EnhancedAIClient(openrouter_key)
    else:
        ai_client = None
except:
    ai_client = None

# Global state
scheduler_thread = None
scheduler_running = False


# Beautiful modern dashboard HTML
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎬 Automation Hub</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 20px;
            color: white;
        }
        
        h1 { font-size: 36px; margin-bottom: 10px; }
        .subtitle { opacity: 0.9; font-size: 16px; }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .tab {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border: none;
            color: white;
            padding: 15px 30px;
            border-radius: 12px;
            cursor: pointer;
            font-size: 16px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .tab:hover {
            background: rgba(255,255,255,0.2);
            transform: translateY(-2px);
        }
        
        .tab.active {
            background: white;
            color: #667eea;
        }
        
        .content {
            background: white;
            border-radius: 20px;
            padding: 30px;
            min-height: 600px;
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 25px;
            border-radius: 15px;
            color: white;
            text-align: center;
        }
        
        .stat-value {
            font-size: 48px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .stat-label {
            font-size: 14px;
            opacity: 0.9;
        }
        
        .workflow-card {
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s;
        }
        
        .workflow-card:hover {
            border-color: #667eea;
            transform: translateY(-2px);
        }
        
        .workflow-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        
        .workflow-name {
            font-size: 20px;
            font-weight: 600;
            color: #1e293b;
        }
        
        .workflow-status {
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
        }
        
        .status-active {
            background: #10b981;
            color: white;
        }
        
        .status-paused {
            background: #6b7280;
            color: white;
        }
        
        .workflow-desc {
            color: #64748b;
            margin-bottom: 15px;
        }
        
        .workflow-stats {
            display: flex;
            gap: 20px;
            font-size: 14px;
            color: #64748b;
        }
        
        .btn {
            padding: 12px 24px;
            border: none;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-primary:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }
        
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 600px;
        }
        
        .messages {
            flex: 1;
            overflow-y: auto;
            padding: 20px;
            background: #f8fafc;
            border-radius: 12px;
            margin-bottom: 20px;
        }
        
        .message {
            margin-bottom: 20px;
            display: flex;
            gap: 12px;
        }
        
        .message-user {
            flex-direction: row-reverse;
        }
        
        .avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            flex-shrink: 0;
        }
        
        .avatar-user {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .avatar-ai {
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        }
        
        .message-content {
            max-width: 70%;
            padding: 15px 20px;
            border-radius: 12px;
            line-height: 1.6;
        }
        
        .message-user .message-content {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-bottom-right-radius: 4px;
        }
        
        .message-ai .message-content {
            background: white;
            border: 2px solid #e2e8f0;
            border-bottom-left-radius: 4px;
        }
        
        .input-area {
            display: flex;
            gap: 10px;
        }
        
        #messageInput {
            flex: 1;
            padding: 15px 20px;
            background: #f8fafc;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            font-size: 14px;
            font-family: inherit;
            resize: none;
        }
        
        #messageInput:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .hidden { display: none; }
        
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: #64748b;
        }
        
        .empty-state h3 {
            font-size: 24px;
            margin-bottom: 10px;
            color: #1e293b;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎬 Automation Hub</h1>
            <p class="subtitle">Your AI-powered workflow management system</p>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('dashboard')">📊 Dashboard</button>
            <button class="tab" onclick="showTab('workflows')">⚡ Workflows</button>
            <button class="tab" onclick="showTab('chat')">💬 Chat</button>
        </div>
        
        <div class="content">
            <!-- Dashboard Tab -->
            <div id="dashboard-tab" class="tab-content">
                <div class="stats-grid" id="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">0</div>
                        <div class="stat-label">Active Workflows</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">0</div>
                        <div class="stat-label">Total Executions</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">0%</div>
                        <div class="stat-label">Success Rate</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">0</div>
                        <div class="stat-label">Videos Created</div>
                    </div>
                </div>
                
                <h2 style="margin-bottom: 20px;">Recent Activity</h2>
                <div id="recent-activity">
                    <div class="empty-state">
                        <h3>No activity yet</h3>
                        <p>Create your first workflow to get started!</p>
                    </div>
                </div>
            </div>
            
            <!-- Workflows Tab -->
            <div id="workflows-tab" class="tab-content hidden">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px;">
                    <h2>Your Workflows</h2>
                    <button class="btn btn-primary" onclick="showTab('chat')">✨ Create New Workflow</button>
                </div>
                
                <div id="workflows-list"></div>
            </div>
            
            <!-- Chat Tab -->
            <div id="chat-tab" class="tab-content hidden">
                <div class="chat-container">
                    <div class="messages" id="messages">
                        <div class="message message-ai">
                            <div class="avatar avatar-ai">🤖</div>
                            <div class="message-content">
                                <strong>Hey! I'm your AI automation assistant.</strong><br><br>
                                I can help you:<br>
                                • Create unlimited workflows<br>
                                • Manage existing automations<br>
                                • Analyze performance<br>
                                • Debug issues<br>
                                <br>
                                Just tell me what you want in plain English! 😊
                            </div>
                        </div>
                    </div>
                    
                    <div class="input-area">
                        <textarea id="messageInput" placeholder="Type your message..." rows="1"></textarea>
                        <button class="btn btn-primary" onclick="sendMessage()">Send</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let currentTab = 'dashboard';
        
        function showTab(tab) {
            currentTab = tab;
            
            // Update tabs
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            event.target.classList.add('active');
            
            // Update content
            document.querySelectorAll('.tab-content').forEach(c => c.classList.add('hidden'));
            document.getElementById(tab + '-tab').classList.remove('hidden');
            
            // Load data for tab
            if (tab === 'dashboard') loadDashboard();
            if (tab === 'workflows') loadWorkflows();
        }
        
        async function loadDashboard() {
            try {
                const stats = await fetch('/api/stats').then(r => r.json());
                
                document.querySelector('.stats-grid').innerHTML = `
                    <div class="stat-card">
                        <div class="stat-value">${stats.active_workflows || 0}</div>
                        <div class="stat-label">Active Workflows</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.total_executions || 0}</div>
                        <div class="stat-label">Total Executions</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.success_rate || 0}%</div>
                        <div class="stat-label">Success Rate</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">${stats.total_workflows || 0}</div>
                        <div class="stat-label">Total Workflows</div>
                    </div>
                `;
            } catch (error) {
                console.error('Error loading dashboard:', error);
            }
        }
        
        async function loadWorkflows() {
            try {
                const workflows = await fetch('/api/workflows').then(r => r.json());
                const listEl = document.getElementById('workflows-list');
                
                if (workflows.length === 0) {
                    listEl.innerHTML = `
                        <div class="empty-state">
                            <h3>No workflows yet</h3>
                            <p>Click "Create New Workflow" to get started!</p>
                        </div>
                    `;
                    return;
                }
                
                listEl.innerHTML = workflows.map(wf => `
                    <div class="workflow-card">
                        <div class="workflow-header">
                            <div class="workflow-name">${wf.name}</div>
                            <span class="workflow-status status-${wf.status}">${wf.status.toUpperCase()}</span>
                        </div>
                        <div class="workflow-desc">${wf.description}</div>
                        <div class="workflow-stats">
                            <span>✅ ${wf.successful_runs} successful</span>
                            <span>❌ ${wf.failed_runs} failed</span>
                            <span>📅 Last run: ${wf.last_run || 'Never'}</span>
                        </div>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Error loading workflows:', error);
            }
        }
        
        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;
            
            addMessage(message, 'user');
            input.value = '';
            
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message })
                });
                
                const result = await response.json();
                
                if (result.success) {
                    addMessage(result.response, 'ai');
                } else {
                    addMessage('Sorry, I encountered an error: ' + result.error, 'ai');
                }
            } catch (error) {
                addMessage('Sorry, I couldn\\'t connect: ' + error, 'ai');
            }
        }
        
        function addMessage(text, sender) {
            const messagesEl = document.getElementById('messages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message message-' + sender;
            
            messageDiv.innerHTML = `
                <div class="avatar avatar-${sender}">${sender === 'user' ? '👤' : '🤖'}</div>
                <div class="message-content">${text.replace(/\\n/g, '<br>')}</div>
            `;
            
            messagesEl.appendChild(messageDiv);
            messagesEl.scrollTop = messagesEl.scrollHeight;
        }
        
        // Auto-resize textarea
        document.getElementById('messageInput').addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 150) + 'px';
        });
        
        // Send on Enter
        document.getElementById('messageInput').addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });
        
        // Load initial data
        loadDashboard();
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Main dashboard"""
    return render_template_string(DASHBOARD_HTML)


@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    try:
        workflow_stats = wm.get_stats()
        db_stats = db.get_stats()
        
        return jsonify({
            'total_workflows': workflow_stats.get('total_workflows', 0),
            'active_workflows': workflow_stats.get('active_workflows', 0),
            'paused_workflows': workflow_stats.get('paused_workflows', 0),
            'total_executions': workflow_stats.get('total_executions', 0),
            'success_rate': workflow_stats.get('success_rate', 0),
            'total_videos': db_stats.get('total_videos', 0),
            'successful_runs': db_stats.get('successful_runs', 0),
            'failed_runs': db_stats.get('failed_runs', 0)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/workflows')
def get_workflows():
    """Get all workflows"""
    try:
        workflows = wm.list_workflows()
        return jsonify(workflows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/workflows/<int:workflow_id>/execute', methods=['POST'])
def execute_workflow_route(workflow_id):
    """Execute a workflow"""
    try:
        result = executor.execute_workflow(workflow_id)
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/chat', methods=['POST'])
def chat():
    """Chat with AI assistant"""
    if not ai_client:
        return jsonify({'success': False, 'error': 'AI client not configured'}), 503
    
    try:
        data = request.json
        message = data.get('message', '')
        
        if not message:
            return jsonify({'success': False, 'error': 'No message provided'}), 400
        
        # Get or create session ID
        if 'session_id' not in session:
            session['session_id'] = str(uuid.uuid4())
        
        session_id = session['session_id']
        
        # Get conversation history
        history = conv_manager.get_conversation(session_id, limit=10)
        history_msgs = [{'role': h['role'], 'content': h['content']} for h in history]
        
        # Get current system context
        context = {
            'workflows': wm.list_workflows(status='active'),
            'stats': wm.get_stats(),
            'recent_videos': db.get_recent_videos(limit=5)
        }
        
        # Chat with AI
        response = ai_client.chat(message, history_msgs, context)
        
        # Save conversation
        conv_manager.add_message(session_id, 'user', message)
        conv_manager.add_message(session_id, 'assistant', response, context)
        
        return jsonify({
            'success': True,
            'response': response
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ai_available': ai_client is not None
    })


if __name__ == '__main__':
    print("\n🎬 Video Automation System - Enhanced Edition")
    print("=" * 50)
    print("\n🌐 Starting web server...")
    print(f"\n   Dashboard: http://localhost:5000")
    print("\n" + "=" * 50 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False
    )
