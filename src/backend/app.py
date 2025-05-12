#!/usr/bin/env python3
import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Any

from fastapi import FastAPI, HTTPException, UploadFile, File, Body, Depends, Request, status, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
import uvicorn

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Audiobook Generator Backend",
    description="Backend API for Audiobook Generator Application",
    version="0.1.0",
)

# Define allowed origins for CORS
# In production, restrict to your Electron app's origin
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:3000",
    "app://.",  # Electron app origin
]

# Add CORS middleware with restricted origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a router for health endpoints
health_router = APIRouter()

# Basic in-memory storage (would be replaced with database in production)
projects = {}
books = {}
characters = {}
voices = {}

# Define Pydantic models for request validation
class BookImportRequest(BaseModel):
    book_type: str = Field(..., description="The type of the book (e.g., epub, pdf, txt)")
    preserve_structure: bool = Field(True, description="Whether to preserve the book's structure")
    extract_metadata: bool = Field(True, description="Whether to extract metadata from the book")

    @validator('book_type')
    def validate_book_type(cls, v):
        allowed_types = ['epub', 'pdf', 'txt', 'docx', 'html']
        if v.lower() not in allowed_types:
            raise ValueError(f'Book type must be one of {allowed_types}')
        return v

class TextAnalysisRequest(BaseModel):
    book_id: str = Field(..., description="The ID of the book to analyze")
    use_gemini: bool = Field(True, description="Whether to use Gemini AI for analysis")

    @validator('book_id')
    def validate_book_id(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError('Book ID must be a non-empty string')
        return v

class AudioGenerationRequest(BaseModel):
    book_id: str = Field(..., description="The ID of the book")
    character_id: str = Field(..., description="The ID of the character")
    text: str = Field(..., description="The text to generate audio for")
    voice_params: Dict[str, Any] = Field(default_factory=dict, description="Parameters for voice customization")

    @validator('text')
    def validate_text(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError('Text must be a non-empty string')
        if len(v) > 10000:
            raise ValueError('Text is too long (max 10000 characters)')
        return v

class ProjectCreationRequest(BaseModel):
    name: str = Field(..., description="The name of the project")
    book_id: str = Field(..., description="The ID of the book")
    template: Optional[str] = Field(None, description="Optional template to use")

    @validator('name')
    def validate_name(cls, v):
        if not v or not isinstance(v, str):
            raise ValueError('Project name must be a non-empty string')
        return v

# Error handler middleware
@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.exception(f"Unhandled error processing request: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "error", "message": "Internal server error"},
        )

@app.get("/")
async def root():
    """Root endpoint to check if API is running."""
    return {"status": "ok", "message": "Audiobook Generator Backend API"}

# Handle both GET and HEAD requests for health checks
@health_router.get("/health")
@health_router.head("/health")
async def health_check():
    """Health check endpoint for startup coordination."""
    return {
        "status": "healthy",
        "uptime": "active",
        "services": {
            "database": "simulated",
            "tts_engine": "ready",
            "gemini_api": "ready"
        }
    }

# Include the health router
app.include_router(health_router)

@app.get("/api/version")
async def get_version():
    """Get the API version."""
    return {"version": "0.1.0"}

@app.post("/api/import-book")
async def import_book(
    file: UploadFile = File(...),
    request: BookImportRequest = Depends(),
):
    """Import a book file and parse it."""
    try:
        # Validate file
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="File has no filename"
            )
            
        # Check file extension
        file_ext = file.filename.split('.')[-1].lower()
        if file_ext not in ['txt', 'epub', 'pdf', 'docx', 'html']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"Unsupported file format: {file_ext}"
            )
        
        # In a real implementation, we would save the file, parse it, etc.
        # For now, we'll just return a mock response
        book_id = f"book_{len(books) + 1}"
        filename = file.filename
        
        # Mock book data
        books[book_id] = {
            "id": book_id,
            "filename": filename,
            "type": request.book_type,
            "title": filename.split(".")[0],  # Simple title extraction
            "author": "Unknown Author",
            "chapters": [{"title": f"Chapter {i+1}", "content": f"Content for chapter {i+1}"} for i in range(3)],
            "metadata": {
                "extracted": request.extract_metadata,
                "preserve_structure": request.preserve_structure,
            }
        }
        
        logger.info(f"Imported book: {filename} (ID: {book_id})")
        
        return {
            "book_id": book_id,
            "status": "success",
            "message": f"Successfully imported {filename}",
            "book_data": books[book_id]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error importing book: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to import book: {str(e)}")

@app.post("/api/analyze-text")
async def analyze_text(request: TextAnalysisRequest):
    """Analyze text to identify characters and dialogue."""
    try:
        if request.book_id not in books:
            raise HTTPException(status_code=404, detail=f"Book not found: {request.book_id}")
        
        # Mock character data
        char_count = 3
        mock_characters = [
            {
                "id": f"char_{i+1}",
                "name": f"Character {i+1}",
                "dialogue_lines": 10 * (i+1),
                "confidence": 0.9 - (i * 0.1),
                "description": f"Description for Character {i+1}",
                "is_narrator": i == 0
            }
            for i in range(char_count)
        ]
        
        characters[request.book_id] = mock_characters
        
        logger.info(f"Analyzed text for book: {request.book_id} (Found {char_count} characters)")
        
        return {
            "book_id": request.book_id,
            "status": "success",
            "characters": mock_characters,
            "used_gemini": request.use_gemini
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to analyze text: {str(e)}")

@app.post("/api/generate-audio")
async def generate_audio(request: AudioGenerationRequest):
    """Generate audio for text using TTS."""
    try:
        if request.book_id not in books:
            raise HTTPException(status_code=404, detail=f"Book not found: {request.book_id}")
        
        # Mock audio generation
        audio_id = f"audio_{request.book_id}_{request.character_id}_{len(voices) + 1}"
        
        # In a real implementation, we would call the TTS model
        voices[audio_id] = {
            "id": audio_id,
            "book_id": request.book_id,
            "character_id": request.character_id,
            "text": request.text,
            "params": request.voice_params,
            "duration": len(request.text) / 20,  # Mock duration calculation
            "file_path": f"/path/to/audio/{audio_id}.mp3"  # Mock file path
        }
        
        logger.info(f"Generated audio: {audio_id}")
        
        return {
            "audio_id": audio_id,
            "status": "success",
            "duration": voices[audio_id]["duration"],
            "file_path": voices[audio_id]["file_path"]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating audio: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate audio: {str(e)}")

@app.post("/api/create-project")
async def create_project(request: ProjectCreationRequest):
    """Create a new audiobook project."""
    try:
        if request.book_id not in books:
            raise HTTPException(status_code=404, detail=f"Book not found: {request.book_id}")
        
        project_id = f"project_{len(projects) + 1}"
        
        # Mock project data
        projects[project_id] = {
            "id": project_id,
            "name": request.name,
            "book_id": request.book_id,
            "template": request.template,
            "created_at": "2023-07-01T12:00:00Z",  # Mock date
            "status": "pending",
            "progress": 0,
        }
        
        logger.info(f"Created project: {request.name} (ID: {project_id})")
        
        return {
            "project_id": project_id,
            "status": "success",
            "project_data": projects[project_id]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating project: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")

@app.get("/api/projects")
async def get_projects():
    """Get all projects."""
    return {"projects": list(projects.values())}

@app.get("/api/project/{project_id}")
async def get_project(project_id: str):
    """Get a specific project."""
    if project_id not in projects:
        raise HTTPException(status_code=404, detail=f"Project not found: {project_id}")
    
    return {"project": projects[project_id]}

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5000, reload=True) 