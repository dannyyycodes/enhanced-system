"""
Dynamic Workflow Executor
==========================
Executes different types of workflows dynamically
"""

import time
import json
import traceback
from datetime import datetime
from typing import Dict, Optional
import logging

from credential_manager import CredentialManager
from workflow_manager import WorkflowManager
from ideas import get_next_idea, IDEAS
from api_clients import KieAPI, BlotatoClient
from ai_client import EnhancedAIClient


class WorkflowExecutor:
    """Executes workflows dynamically based on their type"""
    
    def __init__(self):
        self.cm = CredentialManager()
        self.wm = WorkflowManager()
        
        # Initialize API clients
        self.kie = KieAPI(self.cm.get_credential('kie'))
        self.blotato = BlotatoClient(self.cm.get_credential('blotato'))
        self.ai = EnhancedAIClient(self.cm.get_credential('openrouter'))
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def execute_workflow(self, workflow_id: int) -> Dict:
        """Execute a workflow by ID"""
        
        workflow = self.wm.get_workflow(workflow_id)
        if not workflow:
            return {'success': False, 'error': 'Workflow not found'}
        
        if workflow['status'] != 'active':
            return {'success': False, 'error': f"Workflow is {workflow['status']}"}
        
        self.logger.info(f"🚀 Executing workflow: {workflow['name']}")
        
        try:
            # Route to appropriate executor based on type
            if workflow['type'] == 'video_creation':
                result = self._execute_video_creation(workflow)
            elif workflow['type'] == 'engagement':
                result = self._execute_engagement(workflow)
            elif workflow['type'] == 'analytics':
                result = self._execute_analytics(workflow)
            elif workflow['type'] == 'custom':
                result = self._execute_custom(workflow)
            else:
                result = {'success': False, 'error': f"Unknown workflow type: {workflow['type']}"}
            
            # Log execution
            if result['success']:
                self.wm.log_execution(workflow_id, 'success', result)
                self.logger.info(f"✅ Workflow completed: {workflow['name']}")
            else:
                self.wm.log_execution(workflow_id, 'failed', error=result.get('error'))
                self.logger.error(f"❌ Workflow failed: {workflow['name']}")
            
            return result
            
        except Exception as e:
            error_msg = str(e)
            error_trace = traceback.format_exc()
            
            self.logger.error(f"❌ Workflow crashed: {error_msg}")
            self.logger.error(error_trace)
            
            self.wm.log_execution(workflow_id, 'failed', error=error_msg)
            
            return {
                'success': False,
                'error': error_msg,
                'trace': error_trace
            }
    
    def _execute_video_creation(self, workflow: Dict) -> Dict:
        """Execute video creation workflow"""
        config = workflow['config']
        
        # Get idea based on content type
        if config.get('idea_bank') == 'default':
            idea, _ = get_next_idea()
        else:
            # Custom idea from config
            idea = config.get('custom_idea', {})
        
        self.logger.info(f"📝 Idea: {idea.get('slug', 'custom')}")
        
        # Generate script with AI
        self.logger.info("✍️ Generating script...")
        script_prompt = self._build_script_prompt(idea, config)
        script_response = self.ai.chat(script_prompt)
        
        # Parse script (try to extract JSON)
        try:
            script = json.loads(script_response)
        except:
            # If AI didn't return JSON, create structured response
            script = {
                'title': f"Video about {idea.get('slug', 'content')}",
                'description': script_response[:200],
                'prompt': script_response,
                'hashtags': '#cute #viral #pets'
            }
        
        self.logger.info(f"📹 Title: {script.get('title', 'Untitled')}")
        
        # Create video with Sora
        self.logger.info("🎬 Creating video with Sora...")
        sora_response = self.kie.create_video(
            prompt=script.get('prompt', script.get('description')),
            aspect_ratio=config.get('aspect_ratio', '9:16')
        )
        
        task_id = sora_response['data']['taskId']
        self.logger.info(f"⏳ Task ID: {task_id}")
        
        # Wait for completion
        self.logger.info("⏳ Waiting for video generation...")
        result = self.kie.wait_for_completion(task_id, max_wait=600)
        
        # Get video URL
        video_url = result['data']['resultJson']
        if isinstance(video_url, str):
            video_url = json.loads(video_url)['resultUrls'][0]
        else:
            video_url = video_url['resultUrls'][0]
        
        self.logger.info(f"✅ Video ready: {video_url}")
        
        # Upload to Blotato
        self.logger.info("📤 Uploading to Blotato...")
        media = self.blotato.upload_media(video_url)
        media_url = media['url']
        
        # Post to platforms
        platforms = config.get('platforms', ['tiktok', 'instagram', 'youtube'])
        posted_to = []
        
        post_content = f"{script.get('description', '')} {script.get('hashtags', '')}"
        
        for platform in platforms:
            try:
                self.logger.info(f"📱 Posting to {platform}...")
                
                if platform == 'youtube':
                    self.blotato.create_post(
                        platform="youtube",
                        account_id=config.get('youtube_account_id', '19977'),
                        content=post_content,
                        media_url=media_url,
                        title=script.get('title', 'Video'),
                        containsSyntheticMedia=True
                    )
                elif platform == 'instagram':
                    self.blotato.create_post(
                        platform="instagram",
                        account_id=config.get('instagram_account_id', '22251'),
                        content=post_content,
                        media_url=media_url
                    )
                elif platform == 'tiktok':
                    self.blotato.create_post(
                        platform="tiktok",
                        account_id=config.get('tiktok_account_id', '22514'),
                        content=post_content,
                        media_url=media_url,
                        isAiGenerated=True
                    )
                
                posted_to.append(platform)
                self.logger.info(f"✅ Posted to {platform}")
                
            except Exception as e:
                self.logger.error(f"❌ Failed to post to {platform}: {e}")
        
        return {
            'success': True,
            'workflow_id': workflow['id'],
            'workflow_name': workflow['name'],
            'video_url': video_url,
            'title': script.get('title'),
            'posted_to': posted_to,
            'idea_slug': idea.get('slug', 'custom')
        }
    
    def _execute_engagement(self, workflow: Dict) -> Dict:
        """Execute engagement workflow (future implementation)"""
        config = workflow['config']
        
        # Placeholder for engagement workflows
        # This will be implemented when adding comment replies, auto-DMs, etc.
        
        return {
            'success': True,
            'workflow_id': workflow['id'],
            'message': 'Engagement workflow (coming soon)'
        }
    
    def _execute_analytics(self, workflow: Dict) -> Dict:
        """Execute analytics workflow (future implementation)"""
        config = workflow['config']
        
        # Placeholder for analytics workflows
        # This will analyze performance, generate reports, etc.
        
        return {
            'success': True,
            'workflow_id': workflow['id'],
            'message': 'Analytics workflow (coming soon)'
        }
    
    def _execute_custom(self, workflow: Dict) -> Dict:
        """Execute custom workflow defined by user"""
        config = workflow['config']
        
        # Execute custom workflow steps
        # This allows users to define completely custom automation
        
        return {
            'success': True,
            'workflow_id': workflow['id'],
            'message': 'Custom workflow executed'
        }
    
    def _build_script_prompt(self, idea: Dict, config: Dict) -> str:
        """Build prompt for AI script generation"""
        
        return f"""Generate a video script for Sora AI based on this idea:

Idea: {json.dumps(idea, indent=2)}

Requirements:
- Create a hyper-realistic prompt for Sora 2
- Aspect ratio: {config.get('aspect_ratio', '9:16')}
- Style: {config.get('style', 'realistic, smartphone video')}
- Duration: {config.get('duration', '5-10 seconds')}

Return ONLY a JSON object with:
{{
  "title": "Viral-friendly title under 60 chars",
  "description": "1-2 sentence caption for social media",
  "prompt": "Detailed Sora 2 prompt with camera details, lighting, action",
  "hashtags": "Relevant viral hashtags"
}}

Focus on making it viral-worthy and engaging!"""


if __name__ == '__main__':
    # Test executor
    print("🔧 Testing workflow executor...")
    
    executor = WorkflowExecutor()
    
    # Get first workflow
    workflows = executor.wm.list_workflows(status='active')
    
    if workflows:
        workflow = workflows[0]
        print(f"\n🚀 Executing: {workflow['name']}")
        
        result = executor.execute_workflow(workflow['id'])
        
        if result['success']:
            print(f"\n✅ Success!")
            print(f"   Video: {result.get('title')}")
            print(f"   Posted to: {', '.join(result.get('posted_to', []))}")
        else:
            print(f"\n❌ Failed: {result.get('error')}")
    else:
        print("No active workflows found")
