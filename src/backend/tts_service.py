#!/usr/bin/env python3
import os
import logging
import tempfile
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List, Union

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class TTSError(Exception):
    """Base exception for TTS service errors."""
    pass

class TTSModelNotFoundError(TTSError):
    """Raised when the TTS model is not found."""
    pass

class TTSProcessingError(TTSError):
    """Raised when there's an error processing the text."""
    pass

class KokoroTTSService:
    """Service for interacting with Kokoro TTS system."""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize the Kokoro TTS service.
        
        Args:
            model_path: Path to the pre-trained model. If None, uses the default.
        """
        self.model_path = model_path or os.environ.get("KOKORO_MODEL_PATH", "./models/kokoro_tts")
        self.initialized = False
        self.available_voices = []
        self.model = None
        
        # Validate model path
        model_dir = Path(self.model_path)
        if not model_dir.exists():
            logger.warning(f"Model directory not found: {self.model_path}")
            # We'll initialize lazily when needed
        else:
            self._load_model()
    
    def _load_model(self) -> None:
        """
        Load the TTS model.
        
        Raises:
            TTSModelNotFoundError: If the model cannot be loaded.
        """
        try:
            logger.info(f"Loading Kokoro TTS model from {self.model_path}...")
            # In a real implementation, we would actually load the model here
            # self.model = KokoroTTS.load_model(self.model_path)
            
            # Mock model loading
            self.model = "MockKokoroTTSModel"
            self.available_voices = [
                {"id": "voice_1", "name": "Female 1", "gender": "female", "language": "en-US"},
                {"id": "voice_2", "name": "Male 1", "gender": "male", "language": "en-US"},
                {"id": "voice_3", "name": "Female 2", "gender": "female", "language": "en-US"},
                {"id": "voice_4", "name": "Male 2", "gender": "male", "language": "en-US"},
            ]
            self.initialized = True
            logger.info("Kokoro TTS model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load Kokoro TTS model: {str(e)}")
            raise TTSModelNotFoundError(f"Failed to load Kokoro TTS model: {str(e)}")
    
    def ensure_model_loaded(self) -> None:
        """
        Ensure the model is loaded before use.
        
        Raises:
            TTSModelNotFoundError: If the model cannot be loaded.
        """
        if not self.initialized:
            self._load_model()
            if not self.initialized:
                raise TTSModelNotFoundError("TTS model could not be initialized")
    
    def generate_audio(
        self, 
        text: str, 
        voice_id: str, 
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Generate audio from text using Kokoro TTS.
        
        Args:
            text: The text to convert to speech
            voice_id: The ID of the voice to use
            params: Additional parameters for voice customization
                - pitch: Voice pitch adjustment (-10.0 to 10.0)
                - speed: Speech speed adjustment (0.5 to 2.0)
                - emotion: Emotional tone (neutral, happy, sad, angry)
                - emphasis: Words to emphasize (list of words)
                
        Returns:
            Dict containing:
                - file_path: Path to the generated audio file
                - duration: Duration of the audio in seconds
                - format: Audio format (e.g., "mp3", "wav")
                - sample_rate: Sample rate of the audio
                
        Raises:
            TTSModelNotFoundError: If the TTS model is not loaded
            TTSProcessingError: If there's an error processing the text
            ValueError: If the inputs are invalid
        """
        # Validate inputs
        if not text or not isinstance(text, str):
            raise ValueError("Text must be a non-empty string")
        
        if not voice_id or not isinstance(voice_id, str):
            raise ValueError("Voice ID must be a non-empty string")
        
        if len(text) > 10000:
            raise ValueError("Text is too long (max 10000 characters)")
        
        params = params or {}
        
        # Ensure the model is loaded
        try:
            self.ensure_model_loaded()
        except TTSModelNotFoundError as e:
            logger.error(f"Model not loaded: {str(e)}")
            raise
        
        # Check if the voice exists
        voice_exists = any(voice["id"] == voice_id for voice in self.available_voices)
        if not voice_exists:
            available_ids = [voice["id"] for voice in self.available_voices]
            raise ValueError(f"Voice ID '{voice_id}' not found. Available voices: {available_ids}")
        
        try:
            logger.info(f"Generating audio for text of length {len(text)} with voice {voice_id}")
            
            # Validate and process parameters
            processed_params = self._process_params(params)
            
            # In a real implementation, we would call the actual TTS model
            # audio_data = self.model.generate(text, voice_id, **processed_params)
            
            # For now, create a mock audio file
            temp_dir = tempfile.gettempdir()
            audio_file = Path(temp_dir) / f"kokoro_tts_{voice_id}_{hash(text) % 10000}.mp3"
            
            # Mock writing an audio file
            with open(audio_file, "w") as f:
                f.write("Mock audio data")
            
            # Mock duration calculation based on text length and speech rate
            speech_rate = processed_params.get("speed", 1.0)
            words = len(text.split())
            duration = (words / 150) * (1 / speech_rate)  # Assuming 150 wpm is normal
            
            result = {
                "file_path": str(audio_file),
                "duration": duration,
                "format": "mp3",
                "sample_rate": 24000,
                "text_length": len(text),
                "voice_id": voice_id,
                "parameters": processed_params
            }
            
            logger.info(f"Generated audio file at {audio_file} with duration {duration:.2f}s")
            return result
            
        except Exception as e:
            logger.error(f"Error generating audio: {str(e)}")
            raise TTSProcessingError(f"Failed to generate audio: {str(e)}")
    
    def _process_params(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and validate the voice parameters.
        
        Args:
            params: The parameters to process
            
        Returns:
            Processed parameters with defaults applied
            
        Raises:
            ValueError: If any parameter is invalid
        """
        processed = {}
        
        # Process pitch
        if "pitch" in params:
            pitch = params["pitch"]
            if not isinstance(pitch, (int, float)):
                raise ValueError("Pitch must be a number")
            if pitch < -10.0 or pitch > 10.0:
                raise ValueError("Pitch must be between -10.0 and 10.0")
            processed["pitch"] = pitch
        else:
            processed["pitch"] = 0.0
        
        # Process speed
        if "speed" in params:
            speed = params["speed"]
            if not isinstance(speed, (int, float)):
                raise ValueError("Speed must be a number")
            if speed < 0.5 or speed > 2.0:
                raise ValueError("Speed must be between 0.5 and 2.0")
            processed["speed"] = speed
        else:
            processed["speed"] = 1.0
        
        # Process emotion
        valid_emotions = ["neutral", "happy", "sad", "angry"]
        if "emotion" in params:
            emotion = params["emotion"]
            if not isinstance(emotion, str):
                raise ValueError("Emotion must be a string")
            if emotion not in valid_emotions:
                raise ValueError(f"Emotion must be one of: {valid_emotions}")
            processed["emotion"] = emotion
        else:
            processed["emotion"] = "neutral"
        
        # Process emphasis
        if "emphasis" in params:
            emphasis = params["emphasis"]
            if not isinstance(emphasis, list):
                raise ValueError("Emphasis must be a list of words")
            processed["emphasis"] = emphasis
        else:
            processed["emphasis"] = []
        
        return processed
    
    def get_available_voices(self) -> List[Dict[str, Any]]:
        """
        Get list of available voices.
        
        Returns:
            List of voice dictionaries with properties
            
        Raises:
            TTSModelNotFoundError: If the TTS model is not loaded
        """
        try:
            self.ensure_model_loaded()
            return self.available_voices
        except TTSModelNotFoundError as e:
            logger.error(f"Failed to get available voices: {str(e)}")
            raise

    def customize_voice(
        self, 
        voice_id: str, 
        customizations: Dict[str, Any]
    ) -> str:
        """
        Create a customized voice based on an existing one.
        
        Args:
            voice_id: Base voice to customize
            customizations: Customization parameters
                - name: Name for the new voice
                - pitch_shift: Base pitch adjustment
                - timbre: Timbre adjustment
                - speaking_style: Speaking style to emulate
                
        Returns:
            ID of the new customized voice
            
        Raises:
            TTSModelNotFoundError: If the TTS model is not loaded
            TTSProcessingError: If there's an error creating the voice
            ValueError: If the inputs are invalid
        """
        # Validate inputs
        if not voice_id or not isinstance(voice_id, str):
            raise ValueError("Voice ID must be a non-empty string")
        
        if not customizations or not isinstance(customizations, dict):
            raise ValueError("Customizations must be a non-empty dictionary")
        
        # Ensure the model is loaded
        try:
            self.ensure_model_loaded()
        except TTSModelNotFoundError as e:
            logger.error(f"Model not loaded: {str(e)}")
            raise
        
        # Check if the base voice exists
        voice_exists = any(voice["id"] == voice_id for voice in self.available_voices)
        if not voice_exists:
            available_ids = [voice["id"] for voice in self.available_voices]
            raise ValueError(f"Base voice ID '{voice_id}' not found. Available voices: {available_ids}")
        
        try:
            logger.info(f"Customizing voice {voice_id}")
            
            # In a real implementation, we would create a custom voice
            # new_voice_id = self.model.customize_voice(voice_id, **customizations)
            
            # For now, create a mock custom voice ID
            base_voice = next(voice for voice in self.available_voices if voice["id"] == voice_id)
            new_voice_id = f"custom_{voice_id}_{len(self.available_voices) + 1}"
            
            # Add the new voice to available voices
            new_voice = {
                "id": new_voice_id,
                "name": customizations.get("name", f"Customized {base_voice['name']}"),
                "gender": base_voice["gender"],
                "language": base_voice["language"],
                "is_custom": True,
                "base_voice_id": voice_id,
                "customizations": customizations
            }
            
            self.available_voices.append(new_voice)
            
            logger.info(f"Created customized voice with ID {new_voice_id}")
            return new_voice_id
            
        except Exception as e:
            logger.error(f"Error customizing voice: {str(e)}")
            raise TTSProcessingError(f"Failed to customize voice: {str(e)}")

# Singleton instance
tts_service = KokoroTTSService()

async def get_tts_service() -> KokoroTTSService:
    """Factory function to get the TTS service instance."""
    return tts_service 