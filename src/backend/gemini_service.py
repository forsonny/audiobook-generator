#!/usr/bin/env python3
import os
import json
import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class GeminiError(Exception):
    """Base exception for Gemini service errors."""
    pass

class GeminiAPIError(GeminiError):
    """Raised when there's an error with the Gemini API."""
    pass

class GeminiConfigError(GeminiError):
    """Raised when there's a configuration error."""
    pass

class GeminiRequestError(GeminiError):
    """Raised when there's an error with the request to Gemini API."""
    pass

class CharacterInfo:
    """Data class for character information."""
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        dialogue_count: int = 0,
        confidence: float = 0.0,
        is_narrator: bool = False,
        character_traits: Optional[List[str]] = None,
        gender: Optional[str] = None,
        age: Optional[str] = None,
        speaking_style: Optional[str] = None,
        voice_suggestions: Optional[List[Dict[str, Any]]] = None,
    ):
        self.name = name
        self.description = description or ""
        self.dialogue_count = dialogue_count
        self.confidence = confidence
        self.is_narrator = is_narrator
        self.character_traits = character_traits or []
        self.gender = gender
        self.age = age
        self.speaking_style = speaking_style
        self.voice_suggestions = voice_suggestions or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "dialogue_count": self.dialogue_count,
            "confidence": self.confidence,
            "is_narrator": self.is_narrator,
            "character_traits": self.character_traits,
            "gender": self.gender,
            "age": self.age,
            "speaking_style": self.speaking_style,
            "voice_suggestions": self.voice_suggestions,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CharacterInfo':
        """Create CharacterInfo from dictionary."""
        return cls(
            name=data["name"],
            description=data.get("description", ""),
            dialogue_count=data.get("dialogue_count", 0),
            confidence=data.get("confidence", 0.0),
            is_narrator=data.get("is_narrator", False),
            character_traits=data.get("character_traits", []),
            gender=data.get("gender"),
            age=data.get("age"),
            speaking_style=data.get("speaking_style"),
            voice_suggestions=data.get("voice_suggestions", []),
        )

class DialogueInfo:
    """Data class for dialogue information."""
    def __init__(
        self,
        text: str,
        character_name: str,
        start_index: int,
        end_index: int,
        confidence: float = 0.0,
        emotion: Optional[str] = None,
    ):
        self.text = text
        self.character_name = character_name
        self.start_index = start_index
        self.end_index = end_index
        self.confidence = confidence
        self.emotion = emotion
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "text": self.text,
            "character_name": self.character_name,
            "start_index": self.start_index,
            "end_index": self.end_index,
            "confidence": self.confidence,
            "emotion": self.emotion,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DialogueInfo':
        """Create DialogueInfo from dictionary."""
        return cls(
            text=data["text"],
            character_name=data["character_name"],
            start_index=data["start_index"],
            end_index=data["end_index"],
            confidence=data.get("confidence", 0.0),
            emotion=data.get("emotion"),
        )

class GeminiService:
    """Service for interacting with Google's Gemini API for text analysis."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Gemini service.
        
        Args:
            api_key: Google Gemini API key. If None, will try to load from environment.
        """
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        
        if not self.api_key:
            logger.warning("No Gemini API key provided. Service will operate in mock mode.")
        
        logger.info("Gemini service initialized")
    
    async def _make_api_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a request to the Gemini API.
        
        Args:
            endpoint: API endpoint to call
            data: Request data
            
        Returns:
            Response data from API
            
        Raises:
            GeminiAPIError: If there's an error with the API call
        """
        # In a real implementation, we would use aiohttp or similar to make the API request
        try:
            # Mock API request
            logger.info(f"Making request to Gemini API: {endpoint}")
            
            # Simulate API latency
            await asyncio.sleep(0.5)
            
            # Return mock response
            if endpoint == "analyzeCharacters":
                return self._mock_character_analysis(data.get("text", ""))
            elif endpoint == "analyzeDialogue":
                return self._mock_dialogue_analysis(data.get("text", ""))
            elif endpoint == "suggestVoices":
                return self._mock_voice_suggestions(data.get("characters", []))
            else:
                raise GeminiAPIError(f"Unknown endpoint: {endpoint}")
                
        except Exception as e:
            logger.error(f"Error making Gemini API request: {str(e)}")
            raise GeminiAPIError(f"Error making API request: {str(e)}")
    
    def _validate_api_key(self) -> None:
        """
        Validate the API key.
        
        Raises:
            GeminiConfigError: If no API key is configured
        """
        if not self.api_key:
            raise GeminiConfigError("No Gemini API key configured. Set GEMINI_API_KEY environment variable or pass to constructor.")
    
    def _validate_text_input(self, text: str) -> None:
        """
        Validate text input.
        
        Args:
            text: The text to validate
            
        Raises:
            ValueError: If the text is invalid
        """
        if not text:
            raise ValueError("Text cannot be empty")
            
        if not isinstance(text, str):
            raise ValueError("Text must be a string")
            
        # Check if text is too long
        if len(text) > 1000000:  # 1MB limit
            raise ValueError(f"Text is too long ({len(text)} chars). Maximum is 1,000,000 characters.")
    
    async def identify_characters(self, text: str) -> List[CharacterInfo]:
        """
        Identify characters in text using Gemini AI.
        
        Args:
            text: The text to analyze
            
        Returns:
            List of identified characters with information
            
        Raises:
            GeminiConfigError: If no API key is configured
            GeminiAPIError: If there's an error with the API call
            ValueError: If the input is invalid
        """
        # Validate inputs
        self._validate_text_input(text)
        
        try:
            # In a real implementation, we would check the API key
            if self.api_key:
                self._validate_api_key()
                
                # Make the API request
                response = await self._make_api_request("analyzeCharacters", {
                    "text": text,
                    "max_characters": 50,
                    "language": "en",
                    "include_description": True,
                })
                
                # Parse and return the results
                characters = []
                for char_data in response.get("characters", []):
                    characters.append(CharacterInfo.from_dict(char_data))
                
                logger.info(f"Identified {len(characters)} characters in text")
                return characters
            else:
                # Mock response mode
                mock_response = self._mock_character_analysis(text)
                characters = []
                for char_data in mock_response.get("characters", []):
                    characters.append(CharacterInfo.from_dict(char_data))
                
                logger.info(f"[MOCK] Identified {len(characters)} characters in text")
                return characters
                
        except GeminiConfigError:
            raise
        except GeminiAPIError:
            raise
        except Exception as e:
            logger.error(f"Error identifying characters: {str(e)}")
            raise GeminiRequestError(f"Error identifying characters: {str(e)}")
    
    async def identify_dialogue(self, text: str, characters: List[CharacterInfo]) -> List[DialogueInfo]:
        """
        Identify dialogue in text and associate with characters using Gemini AI.
        
        Args:
            text: The text to analyze
            characters: List of characters identified in the text
            
        Returns:
            List of dialogue segments with character attribution
            
        Raises:
            GeminiConfigError: If no API key is configured
            GeminiAPIError: If there's an error with the API call
            ValueError: If the input is invalid
        """
        # Validate inputs
        self._validate_text_input(text)
        
        if not characters:
            raise ValueError("Character list cannot be empty")
        
        try:
            # In a real implementation, we would check the API key
            if self.api_key:
                self._validate_api_key()
                
                # Convert characters to the format expected by the API
                char_data = [char.to_dict() for char in characters]
                
                # Make the API request
                response = await self._make_api_request("analyzeDialogue", {
                    "text": text,
                    "characters": char_data,
                    "language": "en",
                    "include_emotion": True,
                })
                
                # Parse and return the results
                dialogues = []
                for dialogue_data in response.get("dialogues", []):
                    dialogues.append(DialogueInfo.from_dict(dialogue_data))
                
                logger.info(f"Identified {len(dialogues)} dialogue segments in text")
                return dialogues
            else:
                # Mock response mode
                mock_response = self._mock_dialogue_analysis(text)
                dialogues = []
                for dialogue_data in mock_response.get("dialogues", []):
                    dialogues.append(DialogueInfo.from_dict(dialogue_data))
                
                logger.info(f"[MOCK] Identified {len(dialogues)} dialogue segments in text")
                return dialogues
                
        except GeminiConfigError:
            raise
        except GeminiAPIError:
            raise
        except Exception as e:
            logger.error(f"Error identifying dialogue: {str(e)}")
            raise GeminiRequestError(f"Error identifying dialogue: {str(e)}")
    
    async def suggest_voices(self, characters: List[CharacterInfo]) -> Dict[str, List[Dict[str, Any]]]:
        """
        Suggest voice profiles for characters based on their traits.
        
        Args:
            characters: List of characters to suggest voices for
            
        Returns:
            Dictionary mapping character names to suggested voice profiles
            
        Raises:
            GeminiConfigError: If no API key is configured
            GeminiAPIError: If there's an error with the API call
            ValueError: If the input is invalid
        """
        if not characters:
            raise ValueError("Character list cannot be empty")
        
        try:
            # In a real implementation, we would check the API key
            if self.api_key:
                self._validate_api_key()
                
                # Convert characters to the format expected by the API
                char_data = [char.to_dict() for char in characters]
                
                # Make the API request
                response = await self._make_api_request("suggestVoices", {
                    "characters": char_data,
                })
                
                # Parse and return the results
                suggestions = response.get("voice_suggestions", {})
                
                logger.info(f"Generated voice suggestions for {len(suggestions)} characters")
                return suggestions
            else:
                # Mock response mode
                mock_response = self._mock_voice_suggestions(characters)
                suggestions = mock_response.get("voice_suggestions", {})
                
                logger.info(f"[MOCK] Generated voice suggestions for {len(suggestions)} characters")
                return suggestions
                
        except GeminiConfigError:
            raise
        except GeminiAPIError:
            raise
        except Exception as e:
            logger.error(f"Error suggesting voices: {str(e)}")
            raise GeminiRequestError(f"Error suggesting voices: {str(e)}")
    
    def _mock_character_analysis(self, text: str) -> Dict[str, Any]:
        """Generate mock character analysis for testing."""
        # Estimate the number of characters based on text length
        text_length = len(text)
        num_characters = min(max(2, text_length // 10000), 10)
        
        mock_characters = []
        for i in range(num_characters):
            is_narrator = (i == 0)  # First character is narrator
            
            if is_narrator:
                name = "Narrator"
                desc = "The narrator of the story"
                traits = ["observant", "descriptive"]
                gender = None
                age = None
                style = "formal"
            else:
                name = f"Character {i}"
                desc = f"A supporting character in the story"
                traits = ["trait1", "trait2"]
                gender = "male" if i % 2 == 0 else "female"
                age = "adult"
                style = "casual"
            
            char = {
                "name": name,
                "description": desc,
                "dialogue_count": (text_length // 500) * (3 if is_narrator else 1),
                "confidence": 0.9 - (i * 0.05),
                "is_narrator": is_narrator,
                "character_traits": traits,
                "gender": gender,
                "age": age,
                "speaking_style": style,
            }
            mock_characters.append(char)
        
        return {
            "characters": mock_characters,
            "language_detected": "en",
            "character_count": len(mock_characters),
        }
    
    def _mock_dialogue_analysis(self, text: str) -> Dict[str, Any]:
        """Generate mock dialogue analysis for testing."""
        # Create some mock dialogue segments
        text_length = len(text)
        num_dialogues = min(max(5, text_length // 5000), 50)
        
        mock_dialogues = []
        current_pos = 0
        
        for i in range(num_dialogues):
            # Calculate a random dialogue length
            dialogue_length = min(100, text_length // num_dialogues)
            
            # If we've exceeded text length, break
            if current_pos + dialogue_length >= text_length:
                break
            
            # Skip ahead to simulate narrative between dialogues
            current_pos += min(500, text_length // (num_dialogues * 2))
            
            # If we've exceeded text length, break
            if current_pos >= text_length:
                break
            
            # Create a mock dialogue
            character_index = i % 3  # Cycle through 3 character types
            character_name = "Narrator" if character_index == 0 else f"Character {character_index}"
            
            dialogue = {
                "text": text[current_pos:current_pos + dialogue_length] if current_pos + dialogue_length < text_length else text[current_pos:],
                "character_name": character_name,
                "start_index": current_pos,
                "end_index": current_pos + dialogue_length,
                "confidence": 0.8,
                "emotion": ["neutral", "happy", "sad", "angry"][i % 4],
            }
            
            mock_dialogues.append(dialogue)
            current_pos += dialogue_length
        
        return {
            "dialogues": mock_dialogues,
            "dialogue_count": len(mock_dialogues),
        }
    
    def _mock_voice_suggestions(self, characters: Union[List[CharacterInfo], List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Generate mock voice suggestions for testing."""
        voice_suggestions = {}
        
        # Ensure we're working with character dictionaries
        char_list = []
        for char in characters:
            if isinstance(char, CharacterInfo):
                char_list.append(char.to_dict())
            else:
                char_list.append(char)
        
        for char in char_list:
            name = char.get("name", "Unknown")
            is_narrator = char.get("is_narrator", False)
            gender = char.get("gender")
            age = char.get("age")
            
            # Generate appropriate voice suggestions
            suggestions = []
            
            if is_narrator:
                suggestions.append({
                    "voice_id": "narrator_1",
                    "name": "Clear Narrator",
                    "pitch": 0,
                    "speed": 1.0,
                    "confidence": 0.95,
                })
                suggestions.append({
                    "voice_id": "narrator_2",
                    "name": "Storyteller",
                    "pitch": -1,
                    "speed": 0.9,
                    "confidence": 0.9,
                })
            elif gender == "male":
                suggestions.append({
                    "voice_id": "male_1",
                    "name": "Standard Male",
                    "pitch": 0,
                    "speed": 1.0,
                    "confidence": 0.9,
                })
                suggestions.append({
                    "voice_id": "male_2",
                    "name": "Deep Male",
                    "pitch": -2,
                    "speed": 0.95,
                    "confidence": 0.85,
                })
            elif gender == "female":
                suggestions.append({
                    "voice_id": "female_1",
                    "name": "Standard Female",
                    "pitch": 1,
                    "speed": 1.0,
                    "confidence": 0.9,
                })
                suggestions.append({
                    "voice_id": "female_2",
                    "name": "Soft Female",
                    "pitch": 2,
                    "speed": 1.05,
                    "confidence": 0.85,
                })
            else:
                suggestions.append({
                    "voice_id": "neutral_1",
                    "name": "Neutral Voice",
                    "pitch": 0,
                    "speed": 1.0,
                    "confidence": 0.8,
                })
            
            voice_suggestions[name] = suggestions
        
        return {
            "voice_suggestions": voice_suggestions,
        }

# Singleton instance
gemini_service = GeminiService()

async def get_gemini_service() -> GeminiService:
    """Get the Gemini service singleton instance."""
    return gemini_service 