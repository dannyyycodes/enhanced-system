"""
Simple Configuration File
==========================
Just add your API keys here - that's it!
"""

import os

class Config:
    # ============================================
    # API KEYS - Just paste your keys here
    # ============================================
    
    # Kie.ai (Sora Video Generation)
    KIE_API_KEY = os.getenv('KIE_API_KEY', 'your-kie-api-key-here')
    
    # OpenAI (Script Generation)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your-openai-api-key-here')
    
    # Blotato (Social Media Posting)
    BLOTATO_API_KEY = os.getenv('BLOTATO_API_KEY', 'your-blotato-api-key-here')
    
    # Anthropic Claude (For Chat Interface)
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', 'your-anthropic-api-key-here')
    
    # ============================================
    # WORKFLOW SETTINGS
    # ============================================
    
    # How often to post (in hours)
    POST_SCHEDULE = [
        {"hour": 5, "minute": 0},    # 5:00 AM
        {"hour": 10, "minute": 0},   # 10:00 AM
        {"hour": 15, "minute": 0},   # 3:00 PM
        {"hour": 19, "minute": 30},  # 7:30 PM
    ]
    
    # Video settings
    VIDEO_ASPECT_RATIO = "9:16"  # Vertical for TikTok/Instagram/YouTube Shorts
    VIDEO_MODEL = "sora-2-text-to-video"
    
    # Social Media Account IDs (from Blotato)
    TIKTOK_ACCOUNT_ID = "22514"
    INSTAGRAM_ACCOUNT_ID = "22251"
    YOUTUBE_ACCOUNT_ID = "19977"
    
    # Google Drive Folder (optional)
    GOOGLE_DRIVE_FOLDER_ID = "1BoGrbKCr7jobZ1-o4iIFJiCmO_PQRRrM"
    
    # ============================================
    # SYSTEM SETTINGS
    # ============================================
    
    # Database
    DATABASE_PATH = "automation.db"
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FILE = "automation.log"
    
    # Monitoring
    CHECK_INTERVAL = 60  # Check health every 60 seconds
    MAX_RETRIES = 3
    
    # Web Interface
    WEB_PORT = 5000
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-this-secret-key')


# Easy function to check if all required keys are set
def check_config():
    """Check if all required API keys are configured"""
    missing = []
    
    if Config.KIE_API_KEY == 'your-kie-api-key-here':
        missing.append('KIE_API_KEY')
    if Config.OPENAI_API_KEY == 'your-openai-api-key-here':
        missing.append('OPENAI_API_KEY')
    if Config.BLOTATO_API_KEY == 'your-blotato-api-key-here':
        missing.append('BLOTATO_API_KEY')
    if Config.ANTHROPIC_API_KEY == 'your-anthropic-api-key-here':
        missing.append('ANTHROPIC_API_KEY')
    
    if missing:
        print("\n⚠️  Missing API Keys:")
        for key in missing:
            print(f"   - {key}")
        print("\n💡 Add them to config.py or set as environment variables\n")
        return False
    
    print("✅ All API keys configured!")
    return True
