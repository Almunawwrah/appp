# Create requirements.txt
requirements = """opencv-python==4.8.1.78
mediapipe==0.10.9
pyautogui==0.9.54
pillow==10.0.1
numpy==1.24.3
"""

with open('requirements.txt', 'w') as f:
    f.write(requirements)

print("✅ File requirements.txt telah dibuat")

# Create deployment script for PyInstaller
deployment_script = '''#!/bin/bash
# Script untuk membuat executable dengan PyInstaller

echo "🚀 Memulai proses packaging aplikasi CamMouse Pro..."

# Install PyInstaller jika belum ada
pip install pyinstaller

# Buat executable
echo "📦 Membuat executable..."
pyinstaller --onefile --windowed \\
    --name "CamMousePro" \\
    --icon="icon.ico" \\
    --add-data "requirements.txt;." \\
    cammouse_system_controller.py

echo "✅ Proses packaging selesai!"
echo "📁 File executable tersedia di: dist/CamMousePro.exe"
echo ""
echo "🔧 Cara distribusi:"
echo "1. Copy folder dist/ ke komputer target"
echo "2. Pastikan kamera tersedia"
echo "3. Jalankan CamMousePro.exe"
echo ""
echo "⚠️  Catatan keamanan:"
echo "- Aplikasi memerlukan akses kamera"
echo "- Fitur kontrol sistem bekerja global di desktop"
echo "- Gunakan failsafe (geser mouse ke pojok kiri atas) untuk emergency stop"
'''

with open('build_executable.sh', 'w') as f:
    f.write(deployment_script)

print("✅ File deployment script telah dibuat: build_executable.sh")

# Create Windows batch file for deployment
windows_deployment = '''@echo off
echo 🚀 Memulai proses packaging aplikasi CamMouse Pro untuk Windows...

REM Install PyInstaller jika belum ada
pip install pyinstaller

REM Buat executable
echo 📦 Membuat executable...
pyinstaller --onefile --windowed ^
    --name "CamMousePro" ^
    --icon="icon.ico" ^
    --add-data "requirements.txt;." ^
    cammouse_system_controller.py

echo ✅ Proses packaging selesai!
echo 📁 File executable tersedia di: dist\\CamMousePro.exe
echo.
echo 🔧 Cara distribusi:
echo 1. Copy folder dist\\ ke komputer target  
echo 2. Pastikan kamera tersedia
echo 3. Jalankan CamMousePro.exe
echo.
echo ⚠️  Catatan keamanan:
echo - Aplikasi memerlukan akses kamera
echo - Fitur kontrol sistem bekerja global di desktop
echo - Gunakan failsafe (geser mouse ke pojok kiri atas) untuk emergency stop

pause
'''

with open('build_executable.bat', 'w') as f:
    f.write(windows_deployment)

print("✅ File deployment script Windows telah dibuat: build_executable.bat")

# Create Electron alternative structure
electron_package_json = '''{
  "name": "cammouse-pro-desktop",
  "version": "2.1.0",
  "description": "System-wide cursor control using camera gestures",
  "main": "main.js",
  "scripts": {
    "start": "electron .",
    "build": "electron-builder",
    "dist": "electron-builder --publish=never"
  },
  "author": "AI Assistant",
  "license": "MIT",
  "devDependencies": {
    "electron": "^27.0.0",
    "electron-builder": "^24.6.4"
  },
  "dependencies": {
    "@mediapipe/hands": "^0.4.1675469404",
    "@mediapipe/camera_utils": "^0.3.1675466862",
    "@mediapipe/drawing_utils": "^0.3.1620248257",
    "robotjs": "^0.6.0"
  },
  "build": {
    "appId": "com.cammouse.pro",
    "productName": "CamMouse Pro",
    "directories": {
      "output": "dist"
    },
    "files": [
      "**/*",
      "!node_modules",
      "!src",
      "!docs"
    ],
    "win": {
      "target": "nsis",
      "icon": "assets/icon.ico"
    },
    "mac": {
      "target": "dmg",
      "icon": "assets/icon.icns"
    },
    "linux": {
      "target": "AppImage",
      "icon": "assets/icon.png"
    }
  }
}'''

with open('electron_package.json', 'w') as f:
    f.write(electron_package_json)

print("✅ File Electron package.json telah dibuat: electron_package.json")

# Create Electron main.js template
electron_main = '''const { app, BrowserWindow, ipcMain, globalShortcut } = require('electron');
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
'''

with open('electron_main.js', 'w') as f:
    f.write(electron_main)

print("✅ File Electron main.js telah dibuat: electron_main.js")

print("\n📋 Summary file yang telah dibuat:")
print("1. cammouse_system_controller.py - Script utama aplikasi Python")
print("2. requirements.txt - Dependensi Python")
print("3. build_executable.sh - Script packaging untuk Linux/Mac")
print("4. build_executable.bat - Script packaging untuk Windows")
print("5. electron_package.json - Konfigurasi untuk Electron app")
print("6. electron_main.js - Main process untuk Electron app")

print("\n🚀 Petunjuk Deployment:")
print("\n📌 Python Desktop App:")
print("1. Install dependensi: pip install -r requirements.txt")
print("2. Jalankan: python cammouse_system_controller.py")
print("3. Untuk executable: jalankan build_executable.bat (Windows) atau build_executable.sh (Linux/Mac)")

print("\n📌 Electron Desktop App:")
print("1. Copy electron_package.json ke package.json dalam folder proyek Electron")
print("2. Install: npm install")
print("3. Jalankan: npm start")
print("4. Build: npm run dist")