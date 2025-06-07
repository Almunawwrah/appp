const { app, BrowserWindow, ipcMain, globalShortcut } = require('electron');
const path = require('path');
const robot = require('robotjs');

let mainWindow;
let isSystemControlEnabled = false;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    icon: path.join(__dirname, 'assets/icon.png'),
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true
    }
  });

  mainWindow.loadFile('index.html');

  // Development tools
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }
}

// System cursor control functions
ipcMain.handle('enable-system-control', () => {
  isSystemControlEnabled = true;
  return true;
});

ipcMain.handle('disable-system-control', () => {
  isSystemControlEnabled = false;
  return true;
});

ipcMain.handle('move-cursor', (event, x, y) => {
  if (isSystemControlEnabled) {
    try {
      robot.moveMouse(x, y);
      return true;
    } catch (error) {
      console.error('Error moving cursor:', error);
      return false;
    }
  }
  return false;
});

ipcMain.handle('click-mouse', (event, button) => {
  if (isSystemControlEnabled) {
    try {
      robot.mouseClick(button || 'left');
      return true;
    } catch (error) {
      console.error('Error clicking mouse:', error);
      return false;
    }
  }
  return false;
});

app.whenReady().then(() => {
  createWindow();

  // Register global shortcuts for emergency stop
  globalShortcut.register('CommandOrControl+Shift+Escape', () => {
    isSystemControlEnabled = false;
    mainWindow.webContents.send('emergency-stop');
  });

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('will-quit', () => {
  globalShortcut.unregisterAll();
});
