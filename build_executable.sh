#!/bin/bash
# Script untuk membuat executable dengan PyInstaller

echo "🚀 Memulai proses packaging aplikasi CamMouse Pro..."

# Install PyInstaller jika belum ada
pip install pyinstaller

# Buat executable
echo "📦 Membuat executable..."
pyinstaller --onefile --windowed \
    --name "CamMousePro" \
    --icon="icon.ico" \
    --add-data "requirements.txt;." \
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
