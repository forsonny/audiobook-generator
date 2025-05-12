// Renderer process

document.addEventListener('DOMContentLoaded', async () => {
  console.log('Renderer process started');
  
  // Initialize the application
  initApp();
});

async function initApp() {
  try {
    // Get app version from main process
    const version = await window.electron.getAppVersion();
    document.getElementById('app-version').textContent = `v${version}`;
    
    // Setup event listeners
    setupEventListeners();
    
    console.log('Application initialized successfully');
  } catch (error) {
    console.error('Error initializing application:', error);
    showError('Failed to initialize application', error.message);
  }
}

function setupEventListeners() {
  // Book import button
  const importBtn = document.getElementById('import-book-btn');
  if (importBtn) {
    importBtn.addEventListener('click', handleImportBook);
  }
  
  // Export audiobook button
  const exportBtn = document.getElementById('export-audio-btn');
  if (exportBtn) {
    exportBtn.addEventListener('click', handleExportAudiobook);
  }
  
  // Analyze text button
  const analyzeBtn = document.getElementById('analyze-text-btn');
  if (analyzeBtn) {
    analyzeBtn.addEventListener('click', handleAnalyzeText);
  }
  
  // Generate audio button
  const generateBtn = document.getElementById('generate-audio-btn');
  if (generateBtn) {
    generateBtn.addEventListener('click', handleGenerateAudio);
  }
  
  // Save project button
  const saveBtn = document.getElementById('save-project-btn');
  if (saveBtn) {
    saveBtn.addEventListener('click', handleSaveProject);
  }
  
  // Load project button
  const loadBtn = document.getElementById('load-project-btn');
  if (loadBtn) {
    loadBtn.addEventListener('click', handleLoadProject);
  }
}

async function handleImportBook() {
  try {
    // In a real implementation, we would show a file dialog
    // For now, just mock it with a hardcoded path
    const filePath = 'C:/example/book.txt';
    
    showLoading('Importing book...');
    const result = await window.electron.importBook(filePath);
    hideLoading();
    
    if (result.success) {
      showSuccess('Book imported successfully');
      console.log('Imported book:', result);
      // Update UI with book details
    } else {
      showError('Failed to import book', result.error);
    }
  } catch (error) {
    hideLoading();
    console.error('Error importing book:', error);
    showError('Error importing book', error.message);
  }
}

async function handleExportAudiobook() {
  try {
    const options = {
      format: 'mp3',
      quality: 'high',
      outputPath: 'C:/example/output'
    };
    
    showLoading('Exporting audiobook...');
    const result = await window.electron.exportAudiobook(options);
    hideLoading();
    
    if (result.success) {
      showSuccess('Audiobook exported successfully');
      console.log('Exported audiobook:', result);
      // Update UI with export details
    } else {
      showError('Failed to export audiobook', result.error);
    }
  } catch (error) {
    hideLoading();
    console.error('Error exporting audiobook:', error);
    showError('Error exporting audiobook', error.message);
  }
}

async function handleAnalyzeText() {
  try {
    const text = document.getElementById('book-text')?.value || '';
    
    if (!text.trim()) {
      showError('Error', 'No text to analyze');
      return;
    }
    
    showLoading('Analyzing text...');
    const result = await window.electron.analyzeText(text);
    hideLoading();
    
    if (result.success) {
      showSuccess('Text analyzed successfully');
      console.log('Text analysis result:', result);
      // Update UI with characters
      displayCharacters(result.characters);
    } else {
      showError('Failed to analyze text', result.error);
    }
  } catch (error) {
    hideLoading();
    console.error('Error analyzing text:', error);
    showError('Error analyzing text', error.message);
  }
}

async function handleGenerateAudio() {
  try {
    const text = document.getElementById('book-text')?.value || '';
    const voiceParams = {
      pitch: 0,
      speed: 1.0,
      voice: 'default'
    };
    
    if (!text.trim()) {
      showError('Error', 'No text to generate audio from');
      return;
    }
    
    showLoading('Generating audio...');
    const result = await window.electron.generateAudio(text, voiceParams);
    hideLoading();
    
    if (result.success) {
      showSuccess(`Audio generated successfully (${result.duration.toFixed(1)}s)`);
      console.log('Audio generation result:', result);
      // Update UI with audio player
    } else {
      showError('Failed to generate audio', result.error);
    }
  } catch (error) {
    hideLoading();
    console.error('Error generating audio:', error);
    showError('Error generating audio', error.message);
  }
}

async function handleSaveProject() {
  try {
    const project = {
      name: document.getElementById('project-name')?.value || 'Untitled Project',
      text: document.getElementById('book-text')?.value || '',
      characters: [] // would be populated from UI state
    };
    
    showLoading('Saving project...');
    const result = await window.electron.saveProject(project);
    hideLoading();
    
    if (result.success) {
      showSuccess('Project saved successfully');
      console.log('Project saved:', result);
      // Update UI with project ID
    } else {
      showError('Failed to save project', result.error);
    }
  } catch (error) {
    hideLoading();
    console.error('Error saving project:', error);
    showError('Error saving project', error.message);
  }
}

async function handleLoadProject() {
  try {
    // In a real implementation, we would show a dialog to select a project
    // For now, just mock it with a hardcoded ID
    const projectId = 'project123';
    
    showLoading('Loading project...');
    const result = await window.electron.loadProject(projectId);
    hideLoading();
    
    if (result.success) {
      showSuccess('Project loaded successfully');
      console.log('Project loaded:', result);
      // Update UI with project data
    } else {
      showError('Failed to load project', result.error);
    }
  } catch (error) {
    hideLoading();
    console.error('Error loading project:', error);
    showError('Error loading project', error.message);
  }
}

// UI Helper Functions

function displayCharacters(characters) {
  const container = document.getElementById('characters-container');
  if (!container) return;
  
  container.innerHTML = '';
  
  if (!characters || characters.length === 0) {
    container.innerHTML = '<p>No characters detected</p>';
    return;
  }
  
  characters.forEach(character => {
    const charElement = document.createElement('div');
    charElement.classList.add('character-item');
    charElement.innerHTML = `
      <h3>${character.name}</h3>
      <p>${character.description || ''}</p>
      <p>Dialogue lines: ${character.dialogueLines || 0}</p>
      <button class="character-voice-btn" data-character-id="${character.id}">Set Voice</button>
    `;
    container.appendChild(charElement);
  });
  
  // Add event listeners to voice buttons
  document.querySelectorAll('.character-voice-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const characterId = e.target.getAttribute('data-character-id');
      showVoiceSelectionModal(characterId);
    });
  });
}

function showVoiceSelectionModal(characterId) {
  // Implementation of voice selection modal
  console.log(`Showing voice selection for character: ${characterId}`);
  // In a real app, this would show a modal dialog with voice options
}

function showLoading(message = 'Loading...') {
  const loadingElement = document.getElementById('loading-indicator');
  if (loadingElement) {
    loadingElement.textContent = message;
    loadingElement.style.display = 'block';
  }
}

function hideLoading() {
  const loadingElement = document.getElementById('loading-indicator');
  if (loadingElement) {
    loadingElement.style.display = 'none';
  }
}

function showSuccess(message) {
  const notificationElement = document.getElementById('notification');
  if (notificationElement) {
    notificationElement.textContent = message;
    notificationElement.className = 'notification success';
    notificationElement.style.display = 'block';
    
    // Hide after 3 seconds
    setTimeout(() => {
      notificationElement.style.display = 'none';
    }, 3000);
  }
}

function showError(title, message) {
  const notificationElement = document.getElementById('notification');
  if (notificationElement) {
    notificationElement.textContent = `${title}: ${message}`;
    notificationElement.className = 'notification error';
    notificationElement.style.display = 'block';
    
    // Hide after 5 seconds
    setTimeout(() => {
      notificationElement.style.display = 'none';
    }, 5000);
  }
} 