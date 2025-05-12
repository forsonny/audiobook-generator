const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld(
  'electron', {
    getAppVersion: () => ipcRenderer.invoke('app-version'),
    // Add other IPC functions using the invoke pattern for better error handling
    importBook: (filePath) => ipcRenderer.invoke('import-book', filePath),
    exportAudiobook: (options) => ipcRenderer.invoke('export-audiobook', options),
    generateAudio: (text, voiceParams) => ipcRenderer.invoke('generate-audio', text, voiceParams),
    analyzeText: (text) => ipcRenderer.invoke('analyze-text', text),
    getCharacters: (bookId) => ipcRenderer.invoke('get-characters', bookId),
    saveProject: (project) => ipcRenderer.invoke('save-project', project),
    loadProject: (projectId) => ipcRenderer.invoke('load-project', projectId),
    getProjects: () => ipcRenderer.invoke('get-projects')
  }
); 