# Gemini API Integration Guide for TTS Audiobook Application

## Overview

This document provides detailed implementation guidelines for integrating the Google Gemini API into the TTS Audiobook Application. The Gemini API will significantly enhance the application's capabilities in character identification, dialogue detection, and contextual analysis, improving the overall quality of generated audiobooks.

## Key Integration Areas

### 1. Character Identification

The Gemini API will be the primary engine for character identification, providing significantly improved accuracy over traditional NLP methods.

#### Implementation Details

1. **API Client Setup**:
    
    ```python
    # ai/gemini/client.py
    import google.generativeai as genai
    from typing import Dict, List, Any
    
    class GeminiClient:
        def __init__(self, api_key: str):
            self.api_key = api_key
            genai.configure(api_key=api_key)
            
        def analyze_characters(self, text_context: str, 
                               known_characters: List[Dict[str, Any]] = None) -> Dict:
            """
            Analyze text to identify characters and their attributes.
            
            Args:
                text_context: Book text to analyze (chapter or section)
                known_characters: Previously identified characters to maintain consistency
                
            Returns:
                Dictionary with identified characters and attributes
            """
            # Construct prompt with appropriate context and instructions
            prompt = self._build_character_prompt(text_context, known_characters)
            
            # Call Gemini API
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            
            # Parse structured response
            return self._parse_character_response(response.text)
            
        def _build_character_prompt(self, text_context, known_characters):
            # Prompt engineering for character identification
            prompt = """
            Analyze the following text from a book and identify all characters mentioned.
            For each character, provide:
            1. Name (and any aliases/nicknames)
            2. Role in the story (protagonist, antagonist, supporting character)
            3. Brief description based on textual clues
            4. Gender (if determinable from context)
            5. Speech patterns or distinctive language traits
            
            Return the information in a structured JSON format like:
            {
                "characters": [
                    {
                        "name": "Character name",
                        "aliases": ["nickname1", "nickname2"],
                        "role": "protagonist",
                        "description": "Brief description",
                        "gender": "male/female/unknown",
                        "speech_patterns": "Description of how they speak"
                    }
                ]
            }
            
            TEXT:
            """
            prompt += text_context
            
            # Include known characters for consistency
            if known_characters and len(known_characters) > 0:
                prompt += "\n\nPreviously identified characters (maintain consistency):\n"
                for char in known_characters:
                    prompt += f"- {char['name']}"
                    if char.get('aliases'):
                        prompt += f" (aliases: {', '.join(char['aliases'])})"
                    prompt += "\n"
            
            return prompt
            
        def _parse_character_response(self, response_text):
            """Parse the structured response from Gemini API"""
            # Extract JSON from response - implementation depends on response format
            # This would include error handling for malformed responses
            # ...
            return parsed_response
    ```
    
2. **Character Analyzer Service**:
    
    ```python
    # ai/gemini/character_analyzer.py
    from typing import List, Dict, Any
    from .client import GeminiClient
    from data.repository import CharacterRepository
    
    class CharacterAnalyzer:
        def __init__(self, gemini_client: GeminiClient, character_repo: CharacterRepository):
            self.client = gemini_client
            self.character_repo = character_repo
            
        async def analyze_book_characters(self, project_id: str, 
                                         text_segments: List[Dict[str, Any]]) -> Dict:
            """
            Perform deep character analysis on book text.
            
            Args:
                project_id: Project identifier
                text_segments: List of text segments to analyze
                
            Returns:
                Dictionary with character information and dialogue attribution
            """
            # Get any existing characters for the project
            existing_characters = self.character_repo.get_characters(project_id)
            
            # Group text into appropriate context windows for analysis
            context_windows = self._create_context_windows(text_segments)
            
            # Process each context window
            all_characters = {}
            for context in context_windows:
                # Get character analysis from Gemini
                character_data = await self.client.analyze_characters(
                    context, existing_characters
                )
                
                # Merge with existing character data
                all_characters = self._merge_character_data(all_characters, character_data)
            
            # Store updated character information
            for char_id, char_data in all_characters.items():
                self.character_repo.update_character(project_id, char_id, char_data)
                
            return all_characters
            
        def attribute_dialogue(self, project_id: str, segment_id: str, 
                              context: Dict[str, Any]) -> Dict:
            """
            Attribute a specific dialogue segment to a character.
            
            Args:
                project_id: Project identifier
                segment_id: Dialogue segment to attribute
                context: Surrounding text context
                
            Returns:
                Attribution with character and confidence
            """
            characters = self.character_repo.get_characters(project_id)
            
            # Build prompt for dialogue attribution
            prompt = self._build_attribution_prompt(context, characters)
            
            # Get attribution from Gemini
            attribution = self.client.analyze_dialogue_attribution(prompt)
            
            return attribution
            
        def _create_context_windows(self, text_segments):
            """Group text segments into appropriate context windows for analysis"""
            # Implementation to create overlapping context windows
            # ...
            return context_windows
            
        def _merge_character_data(self, existing, new_data):
            """Merge character data to maintain consistency"""
            # Logic to detect and merge the same character
            # identified across different contexts
            # ...
            return merged_data
    ```
    
3. **Integration with Character Identification Pipeline**:
    
    ```python
    # text_processing/character_identifier.py
    from ai.gemini.character_analyzer import CharacterAnalyzer
    from ai.fallback.local_nlp import LocalCharacterIdentifier
    
    class CharacterIdentifier:
        def __init__(self, character_analyzer: CharacterAnalyzer, 
                     local_identifier: LocalCharacterIdentifier):
            self.character_analyzer = character_analyzer
            self.local_identifier = local_identifier
            
        async def identify_characters(self, project_id: str, text_segments: List):
            """Identify characters using the best available method"""
            try:
                # Try using Gemini API first
                characters = await self.character_analyzer.analyze_book_characters(
                    project_id, text_segments
                )
                return characters, "gemini"
            except Exception as e:
                # Fall back to local NLP methods
                print(f"Gemini API error: {e}. Falling back to local processing.")
                characters = self.local_identifier.identify_characters(
                    project_id, text_segments
                )
                return characters, "local"
    ```
    

### 2. Dialogue and Narration Detection

The Gemini API will enhance dialogue detection, especially for complex literary styles without clear punctuation patterns.

#### Implementation Details

1. **Dialogue Analyzer Service**:
    
    ```python
    # ai/gemini/dialogue_analyzer.py
    from typing import List, Dict, Any
    from .client import GeminiClient
    
    class DialogueAnalyzer:
        def __init__(self, gemini_client: GeminiClient):
            self.client = gemini_client
            
        async def analyze_dialogue(self, text: str) -> List[Dict[str, Any]]:
            """
            Analyze text to identify dialogue vs narration.
            
            Args:
                text: Text content to analyze
                
            Returns:
                List of segments with type classification
            """
            # Construct prompt for dialogue analysis
            prompt = self._build_dialogue_prompt(text)
            
            # Call Gemini API
            response = await self.client.generate_content(prompt)
            
            # Parse response to extract dialogue segments
            segments = self._parse_dialogue_response(response.text)
            
            return segments
            
        def _build_dialogue_prompt(self, text: str) -> str:
            """Build prompt for dialogue identification"""
            prompt = """
            Analyze the following text from a book and identify which parts are dialogue 
            (spoken by characters) and which parts are narration.
            
            For dialogue, indicate where it begins and ends, and if possible, 
            which character is speaking.
            
            Return the analysis in JSON format:
            {
                "segments": [
                    {
                        "text": "segment text",
                        "type": "dialogue" or "narration",
                        "speaker": "character name" (if dialogue and identifiable),
                        "confidence": 0.0-1.0 (confidence in classification)
                    }
                ]
            }
            
            TEXT:
            """
            prompt += text
            return prompt
            
        def _parse_dialogue_response(self, response_text: str) -> List[Dict[str, Any]]:
            """Parse the structured response from Gemini API"""
            # Extract JSON from response
            # Handle potential parsing errors
            # ...
            return parsed_segments
    ```
    
2. **Hybrid Dialogue Detection System**:
    
    ```python
    # text_processing/dialogue_identifier.py
    import re
    from typing import List, Dict, Any
    from ai.gemini.dialogue_analyzer import DialogueAnalyzer
    
    class DialogueIdentifier:
        def __init__(self, dialogue_analyzer: DialogueAnalyzer):
            self.dialogue_analyzer = dialogue_analyzer
            # Regex for common dialogue patterns
            self.quote_pattern = re.compile(r'"([^"]*)"')
            
        async def identify_dialogue(self, text: str) -> List[Dict[str, Any]]:
            """
            Identify dialogue and narration in text using hybrid approach.
            
            Args:
                text: Text content to analyze
                
            Returns:
                List of segments with type classification
            """
            # First pass: Use regex for obvious dialogue with quotation marks
            segments = self._identify_simple_dialogue(text)
            
            # Identify uncertain segments that need deeper analysis
            uncertain_segments = self._find_uncertain_segments(segments)
            
            if uncertain_segments:
                # Build context for uncertain segments
                context = self._build_context(text, uncertain_segments)
                
                # Use Gemini API for uncertain segments
                ai_segments = await self.dialogue_analyzer.analyze_dialogue(context)
                
                # Merge AI results with rule-based results
                segments = self._merge_segment_results(segments, ai_segments)
            
            return segments
            
        def _identify_simple_dialogue(self, text: str) -> List[Dict[str, Any]]:
            """Use regex to identify obvious dialogue with quotation marks"""
            # Implementation for basic dialogue identification
            # ...
            return segments
            
        def _find_uncertain_segments(self, segments: List[Dict[str, Any]]) -> List[int]:
            """Identify segments that might need AI analysis"""
            # Logic to determine which segments are uncertain
            # ...
            return uncertain_indices
            
        def _build_context(self, text: str, uncertain_segments: List[int]) -> str:
            """Build text context around uncertain segments for AI analysis"""
            # Extract relevant context with surrounding text
            # ...
            return context
            
        def _merge_segment_results(self, rule_segments: List[Dict[str, Any]], 
                                 ai_segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            """Merge results from rule-based and AI-based analysis"""
            # Logic to combine results, prioritizing high-confidence attributions
            # ...
            return merged_segments
    ```
    

### 3. Cache System for API Optimization

A caching system will optimize API usage and improve responsiveness.

#### Implementation Details

```python
# ai/cache/response_cache.py
import json
import hashlib
import os
from typing import Any, Optional
import pickle
from datetime import datetime, timedelta

class ResponseCache:
    def __init__(self, cache_dir: str, ttl_days: int = 30):
        """
        Initialize response cache.
        
        Args:
            cache_dir: Directory to store cache files
            ttl_days: Time-to-live in days for cache entries
        """
        self.cache_dir = cache_dir
        self.ttl_days = ttl_days
        os.makedirs(cache_dir, exist_ok=True)
        
    def get(self, prompt: str) -> Optional[Any]:
        """
        Get cached response for a prompt if available.
        
        Args:
            prompt: The prompt string used as cache key
            
        Returns:
            Cached response or None if not found/expired
        """
        cache_key = self._generate_key(prompt)
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.pickle")
        
        if not os.path.exists(cache_path):
            return None
            
        # Check if cache is expired
        if self._is_expired(cache_path):
            os.remove(cache_path)
            return None
            
        try:
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        except Exception:
            return None
            
    def set(self, prompt: str, response: Any) -> None:
        """
        Cache a response for a prompt.
        
        Args:
            prompt: The prompt string used as cache key
            response: The response to cache
        """
        cache_key = self._generate_key(prompt)
        cache_path = os.path.join(self.cache_dir, f"{cache_key}.pickle")
        
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(response, f)
        except Exception as e:
            print(f"Cache write error: {e}")
            
    def _generate_key(self, prompt: str) -> str:
        """Generate a unique cache key from a prompt"""
        return hashlib.md5(prompt.encode('utf-8')).hexdigest()
        
    def _is_expired(self, cache_path: str) -> bool:
        """Check if a cache entry is expired based on modification time"""
        mtime = os.path.getmtime(cache_path)
        mtime_datetime = datetime.fromtimestamp(mtime)
        expiry_time = mtime_datetime + timedelta(days=self.ttl_days)
        return datetime.now() > expiry_time
```

### 4. API Key Management

Secure management of Gemini API keys is essential.

#### Implementation Details

```python
# utils/api_utils.py
import keyring
import os
from typing import Optional

class APIKeyManager:
    def __init__(self, service_name: str = "tts_audiobook_app"):
        """
        Initialize API key manager.
        
        Args:
            service_name: Name used in the system keychain
        """
        self.service_name = service_name
        
    def get_gemini_api_key(self) -> Optional[str]:
        """
        Get stored Gemini API key from secure storage.
        
        Returns:
            API key or None if not found
        """
        # Try to get from environment first (for development)
        env_key = os.environ.get("GEMINI_API_KEY")
        if env_key:
            return env_key
            
        # Otherwise get from system keychain
        return keyring.get_password(self.service_name, "gemini_api_key")
        
    def set_gemini_api_key(self, api_key: str) -> None:
        """
        Store Gemini API key in secure storage.
        
        Args:
            api_key: The API key to store
        """
        keyring.set_password(self.service_name, "gemini_api_key", api_key)
        
    def delete_gemini_api_key(self) -> None:
        """Remove stored Gemini API key from secure storage."""
        try:
            keyring.delete_password(self.service_name, "gemini_api_key")
        except keyring.errors.PasswordDeleteError:
            # Key might not exist
            pass
```

## Example Workflow: Character Identification and Dialogue Attribution

This workflow demonstrates how the different components interact to process a book chapter:

```python
# Example workflow in api/routes.py

@app.post("/api/project/{project_id}/analyze/characters")
async def analyze_project_characters(project_id: str):
    """API endpoint to analyze characters in a project using Gemini"""
    # Get project data
    project = project_repository.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    # Get text content
    text_segments = text_repository.get_text_segments(project_id)
    
    # Initialize components
    api_key_manager = APIKeyManager()
    api_key = api_key_manager.get_gemini_api_key()
    
    if not api_key:
        raise HTTPException(
            status_code=400, 
            detail="Gemini API key not configured. Please add it in settings."
        )
    
    # Initialize services
    gemini_client = GeminiClient(api_key)
    response_cache = ResponseCache(f"./cache/{project_id}")
    
    # Initialize analyzers with caching
    gemini_client.set_cache(response_cache)
    character_analyzer = CharacterAnalyzer(gemini_client, character_repository)
    dialogue_analyzer = DialogueAnalyzer(gemini_client)
    
    # Start background task for analysis
    task_id = background_tasks.add_task(
        process_book_analysis,
        project_id=project_id,
        text_segments=text_segments,
        character_analyzer=character_analyzer,
        dialogue_analyzer=dialogue_analyzer
    )
    
    return {"task_id": task_id, "status": "processing"}

async def process_book_analysis(
    project_id: str,
    text_segments: List[Dict],
    character_analyzer: CharacterAnalyzer,
    dialogue_analyzer: DialogueAnalyzer
):
    """Background task to process book analysis"""
    try:
        # Step 1: Identify characters
        characters, method = await character_identifier.identify_characters(
            project_id, text_segments
        )
        
        # Step 2: Identify dialogue segments
        all_segments = []
        for chunk in split_into_chunks(text_segments):
            chunk_text = " ".join([seg["text"] for seg in chunk])
            dialogue_segments = await dialogue_identifier.identify_dialogue(chunk_text)
            all_segments.extend(dialogue_segments)
        
        # Step 3: Attribute dialogue to characters
        for segment in all_segments:
            if segment["type"] == "dialogue":
                context = build_context_for_segment(all_segments, segment)
                attribution = await character_analyzer.attribute_dialogue(
                    project_id, segment["id"], context
                )
                segment["speaker"] = attribution["character"]
                segment["confidence"] = attribution["confidence"]
                
        # Step 4: Save results
        segment_repository.save_segments(project_id, all_segments)
        
        # Update project status
        project_repository.update_status(
            project_id, 
            status="character_analysis_complete"
        )
        
    except Exception as e:
        # Log error and update project status
        logger.error(f"Analysis failed for project {project_id}: {e}")
        project_repository.update_status(
            project_id, 
            status="analysis_failed",
            error=str(e)
        )
```

## Frontend Integration

The UI needs components to manage Gemini API settings and display AI-powered character information.

### API Key Setup Component

```jsx
// src/components/Settings/GeminiApiConfig.jsx
import React, { useState, useEffect } from 'react';

const GeminiApiConfig = () => {
  const [apiKey, setApiKey] = useState('');
  const [isConfigured, setIsConfigured] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Check if API key is configured
  useEffect(() => {
    const checkApiStatus = async () => {
      try {
        const response = await window.api.checkGeminiApiStatus();
        setIsConfigured(response.configured);
      } catch (err) {
        setError('Failed to check API status');
      }
    };
    
    checkApiStatus();
  }, []);

  const handleSaveKey = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      await window.api.saveGeminiApiKey(apiKey);
      setIsConfigured(true);
      setApiKey(''); // Clear for security
    } catch (err) {
      setError('Failed to save API key');
    } finally {
      setIsLoading(false);
    }
  };

  const handleTestConnection = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await window.api.testGeminiApi();
      if (response.success) {
        alert('Connection successful!');
      } else {
        setError(`API test failed: ${response.error}`);
      }
    } catch (err) {
      setError('Failed to test API connection');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="gemini-api-config">
      <h3>Gemini API Configuration</h3>
      
      {isConfigured ? (
        <div className="status configured">
          <span className="status-icon">✓</span>
          <span>Gemini API is configured</span>
          <button 
            onClick={handleTestConnection}
            disabled={isLoading}
          >
            Test Connection
          </button>
          <button 
            onClick={() => setIsConfigured(false)}
            className="change-key"
          >
            Change API Key
          </button>
        </div>
      ) : (
        <div className="api-key-form">
          <p>
            Enter your Google Cloud API key for Gemini. 
            <a href="https://cloud.google.com/generative-ai" target="_blank" rel="noopener noreferrer">
              Get a Gemini API key
            </a>
          </p>
          
          <div className="input-group">
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="Enter Gemini API key"
            />
            <button 
              onClick={handleSaveKey}
              disabled={!apiKey || isLoading}
            >
              {isLoading ? 'Saving...' : 'Save API Key'}
            </button>
          </div>
          
          {error && <div className="error-message">{error}</div>}
        </div>
      )}
      
      <div className="info-panel">
        <h4>Enhanced Features with Gemini API:</h4>
        <ul>
          <li>Advanced character identification</li>
          <li>Improved dialogue detection</li>
          <li>Context-aware speaker attribution</li>
          <li>Book genre detection and analysis</li>
        </ul>
        <p className="note">
          Your API key is stored securely in your system's keychain.
          API calls are optimized and cached to minimize usage.
        </p>
      </div>
    </div>
  );
};

export default GeminiApiConfig;
```

### Character Management Component

```jsx
// src/components/CharacterPanel/CharacterList.jsx
import React, { useState, useEffect } from 'react';

const CharacterList = ({ projectId }) => {
  const [characters, setCharacters] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedCharacter, setSelectedCharacter] = useState(null);

  useEffect(() => {
    const fetchCharacters = async () => {
      try {
        setLoading(true);
        const response = await window.api.getProjectCharacters(projectId);
        setCharacters(response.characters);
      } catch (err) {
        setError('Failed to load characters');
      } finally {
        setLoading(false);
      }
    };
    
    fetchCharacters();
  }, [projectId]);

  const handleAnalyzeCharacters = async () => {
    try {
      setLoading(true);
      await window.api.analyzeProjectCharacters(projectId);
      // This will start a background task, so we'll need to poll for updates
      pollAnalysisStatus();
    } catch (err) {
      setError('Failed to start character analysis');
      setLoading(false);
    }
  };

  const pollAnalysisStatus = async () => {
    // Implementation to poll for analysis task completion
    // and update the character list when done
    // ...
  };

  const renderCharacterDetails = (character) => {
    if (!character) return null;
    
    return (
      <div className="character-details">
        <h3>{character.name}</h3>
        
        {character.aliases && character.aliases.length > 0 && (
          <div className="character-aliases">
            <h4>Also known as:</h4>
            <p>{character.aliases.join(', ')}</p>
          </div>
        )}
        
        <div className="character-role">
          <h4>Role:</h4>
          <p>{character.role || 'Unknown'}</p>
        </div>
        
        {character.description && (
          <div className="character-description">
            <h4>Description:</h4>
            <p>{character.description}</p>
          </div>
        )}
        
        {character.speech_patterns && (
          <div className="character-speech">
            <h4>Speech Patterns:</h4>
            <p>{character.speech_patterns}</p>
          </div>
        )}
        
        <div className="character-stats">
          <h4>Statistics:</h4>
          <p>Dialogue Lines: {character.dialogue_count || 0}</p>
          <p>Confidence: {character.confidence ? `${(character.confidence * 100).toFixed(0)}%` : 'N/A'}</p>
          <p>Analysis Method: {character.analysis_method || 'Unknown'}</p>
        </div>
      </div>
    );
  };

  return (
    <div className="character-panel">
      <div className="panel-header">
        <h2>Characters</h2>
        <button 
          onClick={handleAnalyzeCharacters}
          disabled={loading}
          className="analyze-button"
        >
          {loading ? 'Analyzing...' : 'Analyze with Gemini AI'}
        </button>
      </div>
      
      {error && <div className="error-message">{error}</div>}
      
      <div className="character-content">
        <div className="character-list">
          {characters.map(character => (
            <div 
              key={character.id}
              className={`character-item ${selectedCharacter?.id === character.id ? 'selected' : ''}`}
              onClick={() => setSelectedCharacter(character)}
            >
              <div className="character-name">{character.name}</div>
              <div className="character-type">{character.role || 'Unknown'}</div>
              {character.analysis_method === 'gemini' && (
                <div className="ai-badge">AI</div>
              )}
            </div>
          ))}
          
          {characters.length === 0 && !loading && (
            <div className="empty-state">
              <p>No characters identified yet</p>
              <p>Click "Analyze with Gemini AI" to detect characters</p>
            </div>
          )}
        </div>
        
        <div className="character-detail-panel">
          {renderCharacterDetails(selectedCharacter)}
        </div>
      </div>
    </div>
  );
};

export default CharacterList;
```

## Backend IPC Handlers (Electron)

```javascript
// electron/ipc.js
const { ipcMain } = require('electron');
const keytar = require('keytar');
const fetch = require('node-fetch');

// Setup IPC handlers for Gemini API
function setupGeminiHandlers() {
  // Check if Gemini API is configured
  ipcMain.handle('check-gemini-api-status', async () => {
    try {
      const apiKey = await keytar.getPassword('tts_audiobook_app', 'gemini_api_key');
      return { configured: !!apiKey };
    } catch (error) {
      console.error('Error checking API status:', error);
      return { configured: false, error: error.message };
    }
  });

  // Save Gemini API key
  ipcMain.handle('save-gemini-api-key', async (event, apiKey) => {
    try {
      await keytar.setPassword('tts_audiobook_app', 'gemini_api_key', apiKey);
      return { success: true };
    } catch (error) {
      console.error('Error saving API key:', error);
      throw new Error('Failed to save API key');
    }
  });

  // Test Gemini API connection
  ipcMain.handle('test-gemini-api', async () => {
    try {
      const apiKey = await keytar.getPassword('tts_audiobook_app', 'gemini_api_key');
      if (!apiKey) {
        return { success: false, error: 'API key not configured' };
      }

      // Simple test request to Gemini API
      const response = await fetch(
        'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + apiKey,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            contents: [
              {
                parts: [
                  { text: 'Hello, please respond with "API connection successful" if you can read this message.' }
                ]
              }
            ]
          })
        }
      );

      const data = await response.json();
      
      if (response.ok && data.candidates && data.candidates[0].content) {
        return { success: true };
      } else {
        return { 
          success: false, 
          error: data.error ? data.error.message : 'Unknown API error' 
        };
      }
    } catch (error) {
      console.error('Error testing API connection:', error);
      return { success: false, error: error.message };
    }
  });
}

module.exports = {
  setupGeminiHandlers,
  // Other IPC setup functions...
};
```

## Implementation Timeline

1. **Week 1-2: Initial Gemini API Integration**
    
    - Set up API key management
    - Create basic API client
    - Implement response caching system
2. **Week 3-4: Character Identification**
    
    - Develop character analysis prompts
    - Implement character data extraction
    - Create fallback mechanisms
3. **Week 5-6: Dialogue Detection**
    
    - Implement hybrid dialogue detection
    - Optimize context windowing
    - Create dialogue attribution system
4. **Week 7-8: UI Integration**
    
    - Develop API configuration UI
    - Create character management interface
    - Implement analysis visualization
5. **Week 9-10: Testing and Optimization**
    
    - Performance testing and optimization
    - Error handling improvements
    - Cache effectiveness evaluation

## Summary of Benefits

Integrating the Gemini API into the TTS Audiobook Application provides several significant benefits:

1. **Superior Character Identification**: The Gemini API's advanced language understanding will identify characters with much higher accuracy than rule-based methods, even in complex literary works.
    
2. **Improved Dialogue Detection**: The ability to recognize dialogue without clear punctuation cues will enable the application to handle a wider variety of writing styles.
    
3. **Context-Aware Analysis**: Understanding the narrative context will result in more accurate attribution of dialogue to characters.
    
4. **Enhanced User Experience**: AI-powered insights about characters and their relationships will help users make better voice assignment decisions.
    
5. **Adaptability**: The hybrid approach ensures the application remains functional even when offline, while taking advantage of advanced AI capabilities when available.