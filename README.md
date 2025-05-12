# Audiobook Generator

A powerful desktop application for converting text books into high-quality audiobooks using the Kokoro TTS model and Gemini AI for character detection.

## Features

- **Import various book formats** - Support for TXT, EPUB, PDF, DOCX, and more
- **AI-powered character detection** - Automatically identify characters using Google Gemini API
- **Dialogue/narration detection** - Smart identification of dialogue vs. narrative text
- **High-quality TTS voices** - Lifelike audio using the Kokoro TTS model
- **Voice customization** - Adjust pitch, speed, and emotion for each character
- **Multi-format export** - Export as MP3, M4B (with chapters), WAV, or OGG
- **Offline functionality** - Work without an internet connection using local models
- **Project management** - Save, organize, and resume your audiobook projects

## Prerequisites

- Node.js (v16+)
- Python 3.8+
- CUDA-compatible GPU (recommended but optional)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/audiobook-generator.git
   cd audiobook-generator
   ```

2. Install Node.js dependencies:
   ```
   npm install
   ```

3. Install Python dependencies:
   ```
   pip install -r src/backend/requirements.txt
   ```

4. (Optional) Set up environment variables:
   - Create a `.env` file in the project root
   - Add your API keys:
     ```
     GEMINI_API_KEY=your_gemini_api_key
     ```

## Development

### Option 1: Start Everything at Once (Recommended)

Run this command to start both the backend and frontend together:

```
npm run start:all
```

Or for development mode with hot reloading:

```
npm run dev:all
```

On Windows, you can also use the provided batch file:

```
start.bat
```

### Option 2: Start Separately

1. Start the Python backend:
   ```
   cd src/backend
   python app.py
   ```
   or
   ```
   npm run backend
   ```

2. In a new terminal, start the Electron app:
   ```
   npm run frontend
   ```
   or
   ```
   npm run dev
   ```

## Building for Production

To create a production build:

```
npm run build
```

The packaged application will be available in the `dist` directory.

## Technologies Used

- **Frontend**: Electron, HTML/CSS/JavaScript
- **Backend**: Python, FastAPI
- **TTS Engine**: Kokoro TTS
- **Text Analysis**: Google Gemini API
- **Audio Processing**: PyDub, FFmpeg

## License

[MIT License](LICENSE)

## Screenshots

![Application UI](Project/UI%20Mockups/ui-mockup.png)
![Book Import](Project/UI%20Mockups/book-import-screen.png)
![Character Voice Assignment](Project/UI%20Mockups/character-voice-screen.png)
![Text Editor](Project/UI%20Mockups/text-editor-screen.png)
![Export Screen](Project/UI%20Mockups/export-screen.png) 