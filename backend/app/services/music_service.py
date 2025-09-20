"""
Music generation service with multiple API providers
"""

import httpx
import asyncio
import structlog
from typing import Dict, Any, Optional, List
from app.core.config import settings
from app.models.music import MusicParameters, MusicGeneration, MusicStatus

logger = structlog.get_logger()

class MusicService:
    """Music generation service with multiple providers"""
    
    def __init__(self):
        self.providers = {
            "suno": self._generate_with_suno,
            "beatoven": self._generate_with_beatoven,
            "elevenlabs": self._generate_with_elevenlabs
        }
    
    async def generate_music(
        self, 
        prompt: str, 
        parameters: MusicParameters,
        provider: str = "suno"
    ) -> Dict[str, Any]:
        """
        Generate music using specified provider
        """
        try:
            if provider not in self.providers:
                raise ValueError(f"Unknown provider: {provider}")
            
            logger.info(f"Generating music with {provider}")
            
            result = await self.providers[provider](prompt, parameters)
            
            logger.info(f"Successfully generated music with {provider}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating music with {provider}: {e}")
            return {
                "success": False,
                "error": str(e),
                "provider": provider
            }
    
    async def _generate_with_suno(self, prompt: str, parameters: MusicParameters) -> Dict[str, Any]:
        """Generate music using Suno API"""
        try:
            if not settings.SUNO_API_KEY:
                return self._get_demo_music_result("suno")
            
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {settings.SUNO_API_KEY}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "prompt": prompt,
                    "duration": parameters.duration,
                    "genre": parameters.genre,
                    "mood": parameters.mood,
                    "tempo": parameters.tempo,
                    "key": parameters.key
                }
                
                response = await client.post(
                    "https://api.suno.ai/v1/generate",
                    headers=headers,
                    json=data,
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "audio_url": result.get("audio_url"),
                        "duration": result.get("duration"),
                        "provider": "suno",
                        "metadata": result
                    }
                else:
                    raise Exception(f"Suno API error: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Suno generation failed: {e}")
            return self._get_demo_music_result("suno")
    
    async def _generate_with_beatoven(self, prompt: str, parameters: MusicParameters) -> Dict[str, Any]:
        """Generate music using Beatoven API"""
        try:
            if not settings.BEATOVEN_API_KEY:
                return self._get_demo_music_result("beatoven")
            
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {settings.BEATOVEN_API_KEY}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "text": prompt,
                    "duration": parameters.duration,
                    "genre": parameters.genre,
                    "mood": parameters.mood,
                    "tempo": parameters.tempo,
                    "key": parameters.key,
                    "instruments": parameters.instruments
                }
                
                response = await client.post(
                    "https://api.beatoven.ai/v1/generate",
                    headers=headers,
                    json=data,
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return {
                        "success": True,
                        "audio_url": result.get("audio_url"),
                        "duration": result.get("duration"),
                        "provider": "beatoven",
                        "metadata": result
                    }
                else:
                    raise Exception(f"Beatoven API error: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"Beatoven generation failed: {e}")
            return self._get_demo_music_result("beatoven")
    
    async def _generate_with_elevenlabs(self, prompt: str, parameters: MusicParameters) -> Dict[str, Any]:
        """Generate music using ElevenLabs API"""
        try:
            if not settings.ELEVENLABS_API_KEY:
                return self._get_demo_music_result("elevenlabs")
            
            # ElevenLabs is primarily for voice, but can be used for music generation
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {settings.ELEVENLABS_API_KEY}",
                    "Content-Type": "application/json"
                }
                
                data = {
                    "text": prompt,
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.5
                    }
                }
                
                response = await client.post(
                    "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM",
                    headers=headers,
                    json=data,
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    # This would return audio data, not a URL
                    return {
                        "success": True,
                        "audio_data": response.content,
                        "duration": parameters.duration,
                        "provider": "elevenlabs",
                        "metadata": {"format": "mp3"}
                    }
                else:
                    raise Exception(f"ElevenLabs API error: {response.status_code}")
                    
        except Exception as e:
            logger.error(f"ElevenLabs generation failed: {e}")
            return self._get_demo_music_result("elevenlabs")
    
    def _get_demo_music_result(self, provider: str) -> Dict[str, Any]:
        """Return demo music result for testing"""
        return {
            "success": True,
            "audio_url": f"https://demo-audio-{provider}.mp3",
            "duration": 45.0,
            "provider": provider,
            "metadata": {
                "demo": True,
                "message": "This is a demo result. In production, this would be real generated music."
            }
        }
    
    async def get_available_providers(self) -> List[Dict[str, Any]]:
        """Get list of available music generation providers"""
        providers = []
        
        if settings.SUNO_API_KEY:
            providers.append({
                "id": "suno",
                "name": "Suno AI",
                "description": "High-quality AI music generation",
                "features": ["vocals", "instrumental", "multiple genres"],
                "max_duration": 300
            })
        
        if settings.BEATOVEN_API_KEY:
            providers.append({
                "id": "beatoven",
                "name": "Beatoven",
                "description": "Professional music generation for content creators",
                "features": ["royalty-free", "multiple moods", "customizable"],
                "max_duration": 180
            })
        
        if settings.ELEVENLABS_API_KEY:
            providers.append({
                "id": "elevenlabs",
                "name": "ElevenLabs",
                "description": "AI voice and audio generation",
                "features": ["voice synthesis", "audio processing"],
                "max_duration": 120
            })
        
        # Always include demo provider
        providers.append({
            "id": "demo",
            "name": "Demo Mode",
            "description": "Demo music generation for testing",
            "features": ["instant generation", "no API key required"],
            "max_duration": 45
        })
        
        return providers
