"""
Web Application
===============
Simple web dashboard and chat interface
"""

from flask import Flask, render_template, request, jsonify, session
import threading
import os
from datetime import datetime

from config import Config, check_config
from database import Database
from workflow import WorkflowEngine
from scheduler import AutomationScheduler
from api_clients import ClaudeClient


# Initialize Flask app
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Initialize components
db = Database(Config.DATABASE_PATH)
workflow_engine = WorkflowEngine()
scheduler = AutomationScheduler()
claude = None

# Check if Claude API is available
try:
    if Config.ANTHROPIC_API_KEY != 'your-anthropic-api-key-here':
        claude = ClaudeClient(Config.ANTHROPIC_API_KEY)
except:
    pass

# Global state
scheduler_thread = None
scheduler_running = False


@app.route('/')
def index():
    """Main dashboard"""
    stats = db.get_stats()
    recent_videos = db.get_recent_videos(limit=10)
    logs = db.get_logs(limit=50)
    
    return render_template('dashboard.html',
                         stats=stats,
                         videos=recent_videos,
                         logs=logs,
                         scheduler_running=scheduler_running,
                         config_ok=check_config())


@app.route('/api/workflow/run', methods=['POST'])
def run_workflow():
    """Manually trigger a workflow run"""
    try:
        result = workflow_engine.run_workflow()
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/scheduler/start', methods=['POST'])
def start_scheduler():
    """Start the automatic scheduler"""
    global scheduler_thread, scheduler_running
    
    if scheduler_running:
        return jsonify({'success': False, 'error': 'Scheduler already running'})
    
    scheduler_running = True
    scheduler_thread = threading.Thread(target=scheduler.start, daemon=True)
    scheduler_thread.start()
    
    return jsonify({'success': True, 'message': 'Scheduler started'})


@app.route('/api/scheduler/stop', methods=['POST'])
def stop_scheduler():
    """Stop the automatic scheduler"""
    global scheduler_running
    
    if not scheduler_running:
        return jsonify({'success': False, 'error': 'Scheduler not running'})
    
    scheduler.stop()
    scheduler_running = False
    
    return jsonify({'success': True, 'message': 'Scheduler stopped'})


@app.route('/api/stats')
def get_stats():
    """Get current statistics"""
    return jsonify(db.get_stats())


@app.route('/api/videos')
def get_videos():
    """Get recent videos"""
    limit = request.args.get('limit', 10, type=int)
    return jsonify(db.get_recent_videos(limit))


@app.route('/api/logs')
def get_logs():
    """Get recent logs"""
    limit = request.args.get('limit', 100, type=int)
    level = request.args.get('level', None)
    return jsonify(db.get_logs(limit, level))


@app.route('/chat')
def chat_page():
    """Chat interface with Claude"""
    if not claude:
        return "Claude API not configured. Add your ANTHROPIC_API_KEY to config.py", 503
    
    return render_template('chat.html')


@app.route('/api/chat', methods=['POST'])
def chat_with_claude():
    """Send message to Claude"""
    if not claude:
        return jsonify({'error': 'Claude API not configured'}), 503
    
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    # Get conversation history from session
    if 'conversation' not in session:
        session['conversation'] = []
    
    conversation = session['conversation']
    
    # System prompt for Claude to help with automation
    system_prompt = """You are an AI automation assistant helping the user manage their video creation workflow.

You have access to the following system capabilities:
- Run workflows manually
- Check system status and statistics  
- View recent videos and logs
- Modify configuration
- Add new video ideas
- Create new workflows

When the user asks you to do something, you should:
1. Understand what they want
2. Explain what you'll do in simple terms
3. Provide the specific code or configuration changes needed

Be helpful, clear, and friendly. The user is not technical, so explain things simply."""
    
    try:
        response = claude.chat(message, system_prompt, conversation)
        
        # Update conversation history
        conversation.append({"role": "user", "content": message})
        conversation.append({"role": "assistant", "content": response})
        session['conversation'] = conversation[-20:]  # Keep last 20 messages
        
        return jsonify({
            'success': True,
            'response': response
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/test')
def test_apis():
    """Test all API connections"""
    results = workflow_engine.test_apis()
    return jsonify(results)


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'scheduler_running': scheduler_running,
        'database': os.path.exists(Config.DATABASE_PATH)
    })


if __name__ == '__main__':
    print("\n🎬 Video Automation System")
    print("=" * 50)
    
    if check_config():
        print("\n✅ Configuration OK")
        print(f"\n🌐 Starting web server on port {Config.WEB_PORT}...")
        print(f"\n   Dashboard: http://localhost:{Config.WEB_PORT}")
        print(f"   Chat: http://localhost:{Config.WEB_PORT}/chat")
        print("\n" + "=" * 50 + "\n")
        
        app.run(
            host='0.0.0.0',
            port=Config.WEB_PORT,
            debug=False
        )
    else:
        print("\n❌ Please configure your API keys first!")
        print("\nEdit config.py and add your API keys, or set them as environment variables.")
