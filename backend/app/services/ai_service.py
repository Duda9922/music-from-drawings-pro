"""
Advanced AI service for image analysis and music generation
"""

import google.generativeai as genai
from typing import Dict, Any, Optional
import structlog
from PIL import Image
import json
import asyncio
from app.core.config import settings

logger = structlog.get_logger()

class AIService:
    """Advanced AI service using multiple providers"""
    
    def __init__(self):
        self.gemini_model = None
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize AI models"""
        try:
            if settings.GEMINI_API_KEY:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel('gemini-pro-vision')
                logger.info("Gemini model initialized")
            else:
                logger.warning("Gemini API key not provided")
        except Exception as e:
            logger.error(f"Failed to initialize AI models: {e}")
    
    async def analyze_drawing(self, image: Image.Image) -> Dict[str, Any]:
        """
        Analyze drawing using advanced AI with structured output
        """
        try:
            if not self.gemini_model:
                return self._get_demo_analysis()
            
            prompt = """
            Analyze this drawing and provide a comprehensive analysis in JSON format.
            Focus on visual elements that translate to musical characteristics.
            
            Return ONLY a valid JSON object with this exact structure:
            {
                "colors": {
                    "dominant": "description of dominant colors",
                    "palette": ["color1", "color2", "color3"],
                    "temperature": "warm|cool|neutral",
                    "saturation": 0.0-1.0,
                    "brightness": 0.0-1.0,
                    "mood": "description of color mood"
                },
                "lines": {
                    "quality": "smooth|jagged|geometric|organic",
                    "thickness": "thin|medium|thick|varied",
                    "direction": "horizontal|vertical|diagonal|curved|chaotic",
                    "density": 0.0-1.0,
                    "style": "description of line style"
                },
                "composition": {
                    "density": 0.0-1.0,
                    "symmetry": 0.0-1.0,
                    "balance": "balanced|unbalanced|dynamic",
                    "focus_points": ["description1", "description2"],
                    "negative_space": 0.0-1.0
                },
                "subject": {
                    "main_subject": "description of main subject",
                    "scene_type": "landscape|portrait|abstract|still_life|action",
                    "elements": ["element1", "element2", "element3"],
                    "narrative": "description of story or scene"
                },
                "mood": {
                    "primary": "joyful|melancholic|energetic|calm|tense|playful|dramatic",
                    "secondary": "additional mood descriptors",
                    "intensity": 0.0-1.0,
                    "emotional_tone": "description of emotional tone"
                },
                "style": {
                    "artistic_style": "realistic|abstract|cartoon|sketch|painterly",
                    "technique": "description of drawing technique",
                    "complexity": 0.0-1.0,
                    "refinement": "rough|polished|detailed|minimalist"
                },
                "musical_suggestions": {
                    "genre": "suggested music genre",
                    "tempo_range": "slow|moderate|fast",
                    "key_suggestion": "major|minor|modal",
                    "instrumentation": ["suggested instruments"],
                    "mood_mapping": "how visual mood maps to musical mood"
                }
            }
            
            Be extremely specific and descriptive. Focus on elements that would translate to musical characteristics.
            """
            
            response = self.gemini_model.generate_content([prompt, image])
            
            # Parse JSON response
            try:
                analysis = json.loads(response.text.strip())
                logger.info("Successfully analyzed drawing with Gemini")
                return analysis
            except json.JSONDecodeError:
                logger.warning("Failed to parse Gemini response as JSON, using fallback")
                return self._get_demo_analysis()
                
        except Exception as e:
            logger.error(f"Error analyzing drawing: {e}")
            return self._get_demo_analysis()
    
    def _get_demo_analysis(self) -> Dict[str, Any]:
        """Fallback analysis for demo purposes"""
        return {
            "colors": {
                "dominant": "vibrant warm colors",
                "palette": ["orange", "yellow", "red"],
                "temperature": "warm",
                "saturation": 0.8,
                "brightness": 0.7,
                "mood": "energetic and cheerful"
            },
            "lines": {
                "quality": "smooth",
                "thickness": "medium",
                "direction": "curved",
                "density": 0.6,
                "style": "flowing and organic"
            },
            "composition": {
                "density": 0.5,
                "symmetry": 0.7,
                "balance": "balanced",
                "focus_points": ["central figure", "background elements"],
                "negative_space": 0.3
            },
            "subject": {
                "main_subject": "abstract creative composition",
                "scene_type": "abstract",
                "elements": ["geometric shapes", "flowing lines", "colorful forms"],
                "narrative": "creative expression and artistic exploration"
            },
            "mood": {
                "primary": "playful",
                "secondary": "creative and energetic",
                "intensity": 0.7,
                "emotional_tone": "uplifting and inspiring"
            },
            "style": {
                "artistic_style": "abstract",
                "technique": "freeform drawing",
                "complexity": 0.6,
                "refinement": "polished"
            },
            "musical_suggestions": {
                "genre": "electronic pop",
                "tempo_range": "moderate",
                "key_suggestion": "major",
                "instrumentation": ["synthesizer", "drums", "bass"],
                "mood_mapping": "playful visuals translate to upbeat, energetic music"
            }
        }
    
    async def generate_music_prompt(self, analysis: Dict[str, Any]) -> str:
        """
        Generate detailed music prompt from visual analysis
        """
        try:
            colors = analysis.get("colors", {})
            lines = analysis.get("lines", {})
            composition = analysis.get("composition", {})
            subject = analysis.get("subject", {})
            mood = analysis.get("mood", {})
            style = analysis.get("style", {})
            musical_suggestions = analysis.get("musical_suggestions", {})
            
            # Map visual elements to musical parameters
            tempo = self._map_density_to_tempo(composition.get("density", 0.5))
            key_signature = self._map_colors_to_key(colors)
            genre = musical_suggestions.get("genre", "contemporary instrumental")
            instruments = self._map_style_to_instruments(style, subject)
            dynamics = self._map_mood_to_dynamics(mood)
            
            prompt = f"""
            Create a {genre} instrumental piece inspired by a {style.get('artistic_style', 'abstract')} drawing.
            
            Visual Analysis:
            - Subject: {subject.get('main_subject', 'abstract composition')}
            - Colors: {colors.get('mood', 'vibrant')} ({colors.get('temperature', 'warm')} palette)
            - Lines: {lines.get('style', 'flowing')} with {lines.get('quality', 'smooth')} quality
            - Composition: {composition.get('balance', 'balanced')} with {composition.get('density', 0.5):.1f} density
            - Mood: {mood.get('primary', 'playful')} with {mood.get('intensity', 0.7):.1f} intensity
            - Style: {style.get('refinement', 'polished')} {style.get('artistic_style', 'abstract')} technique
            
            Musical Parameters:
            - Genre: {genre}
            - Tempo: {tempo} BPM
            - Key: {key_signature}
            - Instruments: {', '.join(instruments)}
            - Dynamics: {dynamics}
            - Duration: 30-45 seconds
            - Mood: {mood.get('emotional_tone', 'uplifting')}
            
            Create music that captures the essence and energy of this visual artwork.
            The piece should feel like a musical interpretation of the drawing's colors, lines, and mood.
            """
            
            return prompt.strip()
            
        except Exception as e:
            logger.error(f"Error generating music prompt: {e}")
            return "Create an instrumental piece inspired by this creative drawing."
    
    def _map_density_to_tempo(self, density: float) -> int:
        """Map visual density to musical tempo"""
        if density < 0.3:
            return 60 + int(density * 40)  # 60-72 BPM
        elif density < 0.7:
            return 80 + int(density * 40)  # 80-108 BPM
        else:
            return 120 + int(density * 60)  # 120-180 BPM
    
    def _map_colors_to_key(self, colors: Dict[str, Any]) -> str:
        """Map color analysis to musical key"""
        temperature = colors.get("temperature", "neutral")
        brightness = colors.get("brightness", 0.5)
        
        if temperature == "warm" and brightness > 0.6:
            return "C major"
        elif temperature == "cool" or brightness < 0.4:
            return "A minor"
        elif brightness > 0.7:
            return "G major"
        else:
            return "F major"
    
    def _map_style_to_instruments(self, style: Dict[str, Any], subject: Dict[str, Any]) -> list:
        """Map artistic style to instrument selection"""
        artistic_style = style.get("artistic_style", "abstract")
        scene_type = subject.get("scene_type", "abstract")
        
        base_instruments = ["piano", "strings"]
        
        if artistic_style == "realistic":
            base_instruments.extend(["acoustic guitar", "woodwinds"])
        elif artistic_style == "abstract":
            base_instruments.extend(["synthesizer", "electronic"])
        elif artistic_style == "cartoon":
            base_instruments.extend(["xylophone", "bells", "brass"])
        
        if scene_type == "landscape":
            base_instruments.extend(["flute", "nature sounds"])
        elif scene_type == "portrait":
            base_instruments.extend(["cello", "violin"])
        elif scene_type == "action":
            base_instruments.extend(["drums", "electric guitar"])
        
        return base_instruments[:5]  # Limit to 5 instruments
    
    def _map_mood_to_dynamics(self, mood: Dict[str, Any]) -> str:
        """Map mood to musical dynamics"""
        intensity = mood.get("intensity", 0.5)
        primary = mood.get("primary", "neutral")
        
        if intensity > 0.8 or primary in ["energetic", "dramatic"]:
            return "forte to fortissimo"
        elif intensity > 0.6 or primary in ["playful", "joyful"]:
            return "mezzo-forte"
        elif intensity < 0.3 or primary in ["calm", "melancholic"]:
            return "piano to pianissimo"
        else:
            return "mezzo-piano to mezzo-forte"
