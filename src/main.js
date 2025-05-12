const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');

// Keep a global reference of the window object to avoid garbage collection
let mainWindow;

function createWindow() {
  // Create the browser window with initial dimensions
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    minWidth: 1024,
    minHeight: 768,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  // Load the index.html file directly instead of trying to use a dev server
  mainWindow.loadFile(path.join(__dirname, 'index.html'));
  
  // Open DevTools only in development mode
  if (isDev) {
    mainWindow.webContents.openDevTools();
  }

  // Emitted when the window is closed
  mainWindow.on('closed', () => {
    // Dereference the window object
    mainWindow = null;
  });
}

// Create window when Electron has finished initialization
app.whenReady().then(() => {
  createWindow();
  setupIpcHandlers();
});

// Quit when all windows are closed, except on macOS
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

// On macOS, re-create window when dock icon is clicked
app.on('activate', () => {
  if (mainWindow === null) {
    createWindow();
  }
});

// Set up all IPC handlers
function setupIpcHandlers() {
  // App version handler
  ipcMain.handle('app-version', () => {
    return app.getVersion();
  });

  // Book import handler
  ipcMain.handle('import-book', async (event, filePath) => {
    try {
      // Here you would call your backend service to import the book
      // For now, just return a mock response
      return { success: true, filePath };
    } catch (error) {
      console.error('Error importing book:', error);
      return { success: false, error: error.message };
    }
  });

  // Export audiobook handler
  ipcMain.handle('export-audiobook', async (event, options) => {
    try {
      // Here you would call your backend service to export the audiobook
      return { success: true, options };
    } catch (error) {
      console.error('Error exporting audiobook:', error);
      return { success: false, error: error.message };
    }
  });

  // Audio generation handler
  ipcMain.handle('generate-audio', async (event, text, voiceParams) => {
    try {
      // Here you would call your backend service to generate audio
      return { success: true, duration: text.length / 10 };
    } catch (error) {
      console.error('Error generating audio:', error);
      return { success: false, error: error.message };
    }
  });

  // Text analysis handler
  ipcMain.handle('analyze-text', async (event, text) => {
    try {
      // Here you would call your backend service to analyze text
      return { success: true, characters: [] };
    } catch (error) {
      console.error('Error analyzing text:', error);
      return { success: false, error: error.message };
    }
  });

  // Get characters handler
  ipcMain.handle('get-characters', async (event, bookId) => {
    try {
      // Here you would call your backend service to get characters
      return { success: true, characters: [] };
    } catch (error) {
      console.error('Error getting characters:', error);
      return { success: false, error: error.message };
    }
  });

  // Project management handlers
  ipcMain.handle('save-project', async (event, project) => {
    try {
      // Here you would call your backend service to save the project
      return { success: true, projectId: Date.now().toString() };
    } catch (error) {
      console.error('Error saving project:', error);
      return { success: false, error: error.message };
    }
  });

  ipcMain.handle('load-project', async (event, projectId) => {
    try {
      // Here you would call your backend service to load the project
      return { success: true, project: { id: projectId, name: 'Project ' + projectId } };
    } catch (error) {
      console.error('Error loading project:', error);
      return { success: false, error: error.message };
    }
  });

  ipcMain.handle('get-projects', async () => {
    try {
      // Here you would call your backend service to get all projects
      return { success: true, projects: [] };
    } catch (error) {
      console.error('Error getting projects:', error);
      return { success: false, error: error.message };
    }
  });
} 