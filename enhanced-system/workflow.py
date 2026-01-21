"""
Workflow Engine
===============
The main automation that runs your video creation workflow
"""

import time
import traceback
from datetime import datetime
from typing import Dict, Optional
import logging

from config import Config
from database import Database
from ideas import get_next_idea
from api_clients import (
    KieAPI, OpenAIClient, BlotatoClient, 
    SCRIPT_GENERATION_SYSTEM_PROMPT
)


class WorkflowEngine:
    """Main workflow engine for video automation"""
    
    def __init__(self):
        self.db = Database(Config.DATABASE_PATH)
        self.kie = KieAPI(Config.KIE_API_KEY)
        self.openai = OpenAIClient(Config.OPENAI_API_KEY)
        self.blotato = BlotatoClient(Config.BLOTATO_API_KEY)
        
        self.current_idea_index = 0
        
        # Setup logging
        logging.basicConfig(
            level=getattr(logging, Config.LOG_LEVEL),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(Config.LOG_FILE),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def run_workflow(self) -> Dict:
        """
        Run the complete workflow:
        1. Get idea from bank
        2. Generate script
        3. Create video with Sora
        4. Wait for completion
        5. Post to social media
        """
        run_id = self.db.add_workflow_run()
        video_id = None
        
        try:
            self.logger.info("🚀 Starting workflow run")
            
            # Step 1: Get next idea
            self.logger.info("📝 Getting next idea...")
            idea, self.current_idea_index = get_next_idea(self.current_idea_index)
            self.logger.info(f"   Idea: {idea['slug']}")
            
            # Step 2: Generate script
            self.logger.info("✍️  Generating script with AI...")
            script = self.openai.generate_script(idea, SCRIPT_GENERATION_SYSTEM_PROMPT)
            self.logger.info(f"   Title: {script['title']}")
            
            # Create video record in database
            video_id = self.db.add_video(idea, script)
            
            # Step 3: Create video with Sora
            self.logger.info("🎬 Creating video with Sora...")
            sora_response = self.kie.create_video(
                prompt=script['prompt'],
                aspect_ratio=Config.VIDEO_ASPECT_RATIO,
                model=Config.VIDEO_MODEL
            )
            
            task_id = sora_response['data']['taskId']
            self.db.update_video(video_id, sora_task_id=task_id, status='generating')
            self.logger.info(f"   Task ID: {task_id}")
            
            # Step 4: Wait for video completion
            self.logger.info("⏳ Waiting for video generation (this may take a few minutes)...")
            result = self.kie.wait_for_completion(task_id, max_wait=600)
            
            video_url = result['data']['resultJson']
            if isinstance(video_url, str):
                import json
                video_url = json.loads(video_url)['resultUrls'][0]
            else:
                video_url = video_url['resultUrls'][0]
            
            self.db.update_video(video_id, video_url=video_url, status='generated')
            self.logger.info(f"   Video ready: {video_url}")
            
            # Step 5: Upload media to Blotato
            self.logger.info("📤 Uploading to Blotato...")
            media = self.blotato.upload_media(video_url)
            media_url = media['url']
            
            # Step 6: Post to social media
            post_content = f"{script['description']} {script.get('hashtags', '')}"
            
            # Post to YouTube
            self.logger.info("📺 Posting to YouTube...")
            try:
                self.blotato.create_post(
                    platform="youtube",
                    account_id=Config.YOUTUBE_ACCOUNT_ID,
                    content=post_content,
                    media_url=media_url,
                    title=script['title'],
                    containsSyntheticMedia=True
                )
                self.db.update_video(video_id, posted_youtube=True)
                self.logger.info("   ✅ Posted to YouTube")
            except Exception as e:
                self.logger.error(f"   ❌ YouTube posting failed: {e}")
            
            # Post to Instagram
            self.logger.info("📸 Posting to Instagram...")
            try:
                self.blotato.create_post(
                    platform="instagram",
                    account_id=Config.INSTAGRAM_ACCOUNT_ID,
                    content=post_content,
                    media_url=media_url
                )
                self.db.update_video(video_id, posted_instagram=True)
                self.logger.info("   ✅ Posted to Instagram")
            except Exception as e:
                self.logger.error(f"   ❌ Instagram posting failed: {e}")
            
            # Post to TikTok
            self.logger.info("🎵 Posting to TikTok...")
            try:
                self.blotato.create_post(
                    platform="tiktok",
                    account_id=Config.TIKTOK_ACCOUNT_ID,
                    content=post_content,
                    media_url=media_url,
                    isAiGenerated=True
                )
                self.db.update_video(video_id, posted_tiktok=True)
                self.logger.info("   ✅ Posted to TikTok")
            except Exception as e:
                self.logger.error(f"   ❌ TikTok posting failed: {e}")
            
            # Mark as completed
            self.db.update_video(video_id, status='completed')
            self.db.complete_workflow_run(run_id, 'completed', video_id)
            
            self.logger.info("✅ Workflow completed successfully!")
            
            return {
                'success': True,
                'video_id': video_id,
                'video_url': video_url,
                'title': script['title']
            }
            
        except Exception as e:
            error_msg = str(e)
            error_trace = traceback.format_exc()
            
            self.logger.error(f"❌ Workflow failed: {error_msg}")
            self.logger.error(error_trace)
            
            if video_id:
                self.db.update_video(video_id, status='failed', error=error_msg)
            
            self.db.complete_workflow_run(run_id, 'failed', video_id, error_msg)
            
            return {
                'success': False,
                'error': error_msg,
                'trace': error_trace
            }
    
    def test_apis(self) -> Dict:
        """Test all API connections"""
        results = {}
        
        # Test Kie.ai
        try:
            # Just check if we can initialize
            self.kie.headers  # This will raise if key is invalid format
            results['kie'] = {'status': 'ok', 'message': 'API key format valid'}
        except Exception as e:
            results['kie'] = {'status': 'error', 'message': str(e)}
        
        # Test OpenAI
        try:
            # Simple test message
            test_result = self.openai.generate_script(
                {"test": "minimal"},
                "Return JSON: {\"test\": \"ok\"}"
            )
            results['openai'] = {'status': 'ok', 'message': 'API working'}
        except Exception as e:
            results['openai'] = {'status': 'error', 'message': str(e)}
        
        # Test Blotato
        try:
            self.blotato.headers  # This will raise if key is invalid format
            results['blotato'] = {'status': 'ok', 'message': 'API key format valid'}
        except Exception as e:
            results['blotato'] = {'status': 'error', 'message': str(e)}
        
        return results


def run_single_workflow():
    """Helper function to run a single workflow"""
    engine = WorkflowEngine()
    return engine.run_workflow()


if __name__ == '__main__':
    # Run a test workflow
    print("🎬 Starting Video Automation Workflow")
    print("=" * 50)
    
    result = run_single_workflow()
    
    print("\n" + "=" * 50)
    if result['success']:
        print("✅ SUCCESS!")
        print(f"Video: {result['title']}")
        print(f"URL: {result['video_url']}")
    else:
        print("❌ FAILED!")
        print(f"Error: {result['error']}")
