"""
API Clients
===========
Simple wrappers for all external APIs
"""

import requests
import time
from typing import Dict, Optional
import json


class KieAPI:
    """Kie.ai API for Sora video generation"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.kie.ai/api/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def create_video(self, prompt: str, aspect_ratio: str = "9:16", 
                     model: str = "sora-2-text-to-video") -> Dict:
        """Create a new video generation task"""
        url = f"{self.base_url}/jobs/createTask"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "aspect_ratio": aspect_ratio
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_task_status(self, task_id: str) -> Dict:
        """Check the status of a video generation task"""
        url = f"{self.base_url}/jobs/recordInfo"
        params = {"taskId": task_id}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def wait_for_completion(self, task_id: str, max_wait: int = 600, 
                           check_interval: int = 10) -> Dict:
        """Wait for video generation to complete"""
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            result = self.get_task_status(task_id)
            
            # Check if completed
            if result.get('data', {}).get('status') == 'SUCCESS':
                return result
            
            # Check if failed
            if result.get('data', {}).get('status') in ['FAILED', 'ERROR']:
                raise Exception(f"Video generation failed: {result}")
            
            # Wait and try again
            time.sleep(check_interval)
        
        raise TimeoutError(f"Video generation timed out after {max_wait} seconds")


class OpenAIClient:
    """OpenAI API for script generation"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def generate_script(self, idea: Dict, system_prompt: str) -> Dict:
        """Generate a video script from an idea"""
        url = f"{self.base_url}/chat/completions"
        
        user_message = f"""Here is the idea object:

{json.dumps(idea, indent=2)}

Using ONLY this idea object and the system instructions, generate:
- a viral-friendly short title
- a 1–2 sentence description
- one fully detailed, hyper-realistic Sora 2 prompt.

Do not invent a new concept.
Do not change the core hook, characters, or safety constraints.
Apply only small natural variations (lighting, angle, props).
Output ONLY the JSON object described in the system message."""

        payload = {
            "model": "chatgpt-4o-latest",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            "response_format": {"type": "json_object"}
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        content = result['choices'][0]['message']['content']
        return json.loads(content)


class BlotatoClient:
    """Blotato API for social media posting"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://backend.blotato.com/v2"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def upload_media(self, media_url: str) -> Dict:
        """Upload media to Blotato"""
        url = f"{self.base_url}/media"
        
        payload = {"mediaUrl": media_url}
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()
    
    def create_post(self, platform: str, account_id: str, 
                   content: str, media_url: str, **kwargs) -> Dict:
        """Create a post on social media"""
        url = f"{self.base_url}/posts"
        
        payload = {
            "platform": platform,
            "accountId": account_id,
            "content": content,
            "mediaUrls": [media_url],
            **kwargs
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()


class ClaudeClient:
    """Anthropic Claude API for chat interface"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.anthropic.com/v1"
        self.headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json"
        }
    
    def chat(self, message: str, system_prompt: str = None, 
            conversation_history: list = None) -> str:
        """Chat with Claude"""
        url = f"{self.base_url}/messages"
        
        messages = conversation_history or []
        messages.append({"role": "user", "content": message})
        
        payload = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 4096,
            "messages": messages
        }
        
        if system_prompt:
            payload["system"] = system_prompt
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        return result['content'][0]['text']


# System prompt for script generation
SCRIPT_GENERATION_SYSTEM_PROMPT = """You are a SORA 2 PROMPT BUILDER for hyper-realistic, short-form pet videos (dogs, cats, babies with pets, etc.).

You ALWAYS receive one JSON idea object from the Idea Bank. That object contains:
- slug
- language
- coreHook
- settingHints
- coreCharacters
- coreAction
- safetyConstraints
- styleTags

Your job is NOT to invent a new idea.
Your job is to turn THIS idea into a full, production-ready Sora 2 prompt that looks like a real director's brief for a hyper-realistic smartphone video.

You MUST output ONLY valid JSON with these fields:
{
  "title": "A viral-friendly short title under 60 characters",
  "description": "1–2 sentence description for TikTok/Shorts captions",
  "prompt": "THE FULL DETAILED SORA PROMPT HERE",
  "hashtags": "Viral hashtags for this video, space-separated"
}

IMPORTANT:
- Preserve the coreHook, coreAction, characters, and safetyConstraints exactly
- Use specific camera details (smartphone, handheld, angle, distance)
- Include physical realism (weight, joints, physics)
- Add natural lighting details
- Keep it as ONE continuous shot
- Make the prompt detailed enough for Sora to generate perfectly
- No bullet points, no headings in the prompt - just natural paragraphs
"""
