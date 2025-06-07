# Create a comprehensive Python script for system-wide cursor control
# Fixed version with proper string escaping

system_cursor_script = '''
"""
CamMouse System-Wide Cursor Control
===================================
Aplikasi desktop untuk kontrol kursor global menggunakan gesture tangan
dengan MediaPipe dan PyAutoGUI untuk kontrol sistem di seluruh desktop.

Dependensi:
- opencv-python
- mediapipe  
- pyautogui
- tkinter (built-in Python)
- pillow
- numpy

Install:
pip install opencv-python mediapipe pyautogui pillow numpy

Author: AI Assistant
Version: 2.1.0
"""

import cv2
import mediapipe as mp
import pyautogui
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import numpy as np
from PIL import Image, ImageTk
import json
import os
import sys

class CamMouseSystemController:
    def __init__(self):
        """Inisialisasi controller untuk kontrol kursor sistem"""
        # Konfigurasi MediaPipe
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
        # Konfigurasi PyAutoGUI untuk kontrol sistem
        pyautogui.FAILSAFE = True  # Failsafe ke pojok kiri atas
        pyautogui.PAUSE = 0.01  # Delay minimal antar aksi
        
        # Status aplikasi
        self.is_running = False
        self.is_system_control_enabled = False
        self.camera = None
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Konfigurasi gesture
        self.cursor_sensitivity = 1.5
        self.click_threshold = 0.05
        self.last_click_time = 0
        self.click_cooldown = 0.3  # Detik
        
        # Smoothing untuk gerakan kursor
        self.cursor_smoothing = 0.7
        self.last_cursor_pos = None
        
        # Performance tracking
        self.fps_counter = 0
        self.last_fps_time = time.time()
        self.current_fps = 0
        
    def calculate_distance(self, point1, point2):
        """Hitung jarak Euclidean antara dua titik landmark"""
        return np.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    def process_hand_landmarks(self, landmarks, frame_width, frame_height):
        """Proses landmark tangan untuk kontrol kursor"""
        if not landmarks:
            return None
            
        # Ambil landmark penting
        index_tip = landmarks.landmark[8]  # Ujung jari telunjuk
        thumb_tip = landmarks.landmark[4]  # Ujung jempol
        middle_tip = landmarks.landmark[12]  # Ujung jari tengah
        
        # Konversi koordinat ke layar
        cursor_x = int(index_tip.x * self.screen_width * self.cursor_sensitivity)
        cursor_y = int(index_tip.y * self.screen_height * self.cursor_sensitivity)
        
        # Batas layar
        cursor_x = max(0, min(cursor_x, self.screen_width - 1))
        cursor_y = max(0, min(cursor_y, self.screen_height - 1))
        
        # Smoothing gerakan kursor
        if self.last_cursor_pos:
            cursor_x = int(self.last_cursor_pos[0] * self.cursor_smoothing + 
                          cursor_x * (1 - self.cursor_smoothing))
            cursor_y = int(self.last_cursor_pos[1] * self.cursor_smoothing + 
                          cursor_y * (1 - self.cursor_smoothing))
        
        self.last_cursor_pos = (cursor_x, cursor_y)
        
        # Deteksi gesture
        gestures = {
            'cursor_pos': (cursor_x, cursor_y),
            'left_click': False,
            'right_click': False,
            'scroll': None
        }
        
        # Left click: jempol dan telunjuk berdekatan
        left_click_distance = self.calculate_distance(thumb_tip, index_tip)
        if left_click_distance < self.click_threshold:
            gestures['left_click'] = True
            
        # Right click: jempol dan jari tengah berdekatan
        right_click_distance = self.calculate_distance(thumb_tip, middle_tip)
        if right_click_distance < self.click_threshold:
            gestures['right_click'] = True
            
        return gestures
    
    def execute_system_control(self, gestures):
        """Eksekusi kontrol sistem berdasarkan gesture"""
        if not self.is_system_control_enabled:
            return
            
        current_time = time.time()
        
        # Gerakkan kursor
        try:
            pyautogui.moveTo(gestures['cursor_pos'][0], gestures['cursor_pos'][1], 
                           duration=0, _pause=False)
        except pyautogui.FailSafeException:
            self.disable_system_control()
            return
            
        # Click dengan cooldown
        if current_time - self.last_click_time > self.click_cooldown:
            if gestures['left_click']:
                pyautogui.click()
                self.last_click_time = current_time
            elif gestures['right_click']:
                pyautogui.rightClick()
                self.last_click_time = current_time
    
    def start_camera(self):
        """Mulai capture kamera"""
        try:
            self.camera = cv2.VideoCapture(0)
            if not self.camera.isOpened():
                raise Exception("Tidak dapat mengakses kamera")
            self.is_running = True
            return True
        except Exception as e:
            messagebox.showerror("Error Kamera", f"Gagal mengakses kamera: {str(e)}")
            return False
    
    def stop_camera(self):
        """Hentikan capture kamera"""
        self.is_running = False
        self.is_system_control_enabled = False
        if self.camera:
            self.camera.release()
            self.camera = None
    
    def enable_system_control(self):
        """Aktifkan kontrol sistem"""
        if self.is_running:
            self.is_system_control_enabled = True
            return True
        return False
    
    def disable_system_control(self):
        """Nonaktifkan kontrol sistem"""
        self.is_system_control_enabled = False
    
    def process_frame(self):
        """Proses frame kamera untuk deteksi gesture"""
        if not self.is_running or not self.camera:
            return None, None
            
        ret, frame = self.camera.read()
        if not ret:
            return None, None
            
        # Flip frame secara horizontal untuk efek mirror
        frame = cv2.flip(frame, 1)
        
        # Konversi BGR ke RGB untuk MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Deteksi tangan
        results = self.hands.process(rgb_frame)
        
        gestures = None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Gambar landmark pada frame
                self.mp_drawing.draw_landmarks(
                    frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                # Proses gesture
                gestures = self.process_hand_landmarks(
                    hand_landmarks, frame.shape[1], frame.shape[0])
                
                # Eksekusi kontrol sistem
                if gestures:
                    self.execute_system_control(gestures)
        
        # Update FPS counter
        self.fps_counter += 1
        current_time = time.time()
        if current_time - self.last_fps_time >= 1.0:
            self.current_fps = self.fps_counter
            self.fps_counter = 0
            self.last_fps_time = current_time
        
        return frame, gestures

class CamMouseGUI:
    def __init__(self):
        """Inisialisasi GUI aplikasi"""
        self.controller = CamMouseSystemController()
        self.root = tk.Tk()
        self.setup_gui()
        self.update_thread = None
        self.is_gui_running = True
        
    def setup_gui(self):
        """Setup interface GUI"""
        self.root.title("CamMouse Pro - Kontrol Kursor Sistem")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Control Panel
        control_frame = ttk.LabelFrame(main_frame, text="Panel Kontrol", padding="10")
        control_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Buttons
        self.start_btn = ttk.Button(control_frame, text="🎥 Mulai Kamera", 
                                   command=self.start_camera)
        self.start_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.stop_btn = ttk.Button(control_frame, text="⏹️ Stop Kamera", 
                                  command=self.stop_camera, state='disabled')
        self.stop_btn.grid(row=0, column=1, padx=(0, 10))
        
        self.system_btn = ttk.Button(control_frame, text="⚡ Aktifkan Kontrol Sistem", 
                                    command=self.toggle_system_control, state='disabled')
        self.system_btn.grid(row=0, column=2)
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(main_frame, text="Pengaturan", padding="10")
        settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Sensitivity
        ttk.Label(settings_frame, text="Sensitivitas Kursor:").grid(row=0, column=0, sticky=tk.W)
        self.sensitivity_var = tk.DoubleVar(value=1.5)
        sensitivity_scale = ttk.Scale(settings_frame, from_=0.5, to=3.0, 
                                     variable=self.sensitivity_var, 
                                     command=self.update_sensitivity)
        sensitivity_scale.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Click threshold
        ttk.Label(settings_frame, text="Threshold Click:").grid(row=2, column=0, sticky=tk.W)
        self.threshold_var = tk.DoubleVar(value=0.05)
        threshold_scale = ttk.Scale(settings_frame, from_=0.02, to=0.1, 
                                   variable=self.threshold_var,
                                   command=self.update_threshold)
        threshold_scale.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Status
        status_frame = ttk.LabelFrame(settings_frame, text="Status Sistem")
        status_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="Status: Siap")
        self.status_label.grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        
        self.fps_label = ttk.Label(status_frame, text="FPS: 0")
        self.fps_label.grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        
        # Video frame
        self.video_frame = ttk.LabelFrame(main_frame, text="Live Feed", padding="5")
        self.video_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.video_label = ttk.Label(self.video_frame, text="Kamera tidak aktif", 
                                    background="black", foreground="white")
        self.video_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.video_frame.columnconfigure(0, weight=1)
        self.video_frame.rowconfigure(0, weight=1)
        
        # Deployment info
        deploy_frame = ttk.LabelFrame(main_frame, text="Info Deployment", padding="10")
        deploy_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        deploy_text = """Untuk membuat aplikasi standalone:
1. Install PyInstaller: pip install pyinstaller
2. Jalankan: pyinstaller --onefile --windowed cammouse_system.py
3. File executable akan tersedia di folder dist/"""
        
        ttk.Label(deploy_frame, text=deploy_text, justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
        
    def start_camera(self):
        """Mulai kamera dan update thread"""
        if self.controller.start_camera():
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.system_btn.config(state='normal')
            self.status_label.config(text="Status: Kamera Aktif")
            
            # Start update thread
            if self.update_thread is None or not self.update_thread.is_alive():
                self.update_thread = threading.Thread(target=self.update_video, daemon=True)
                self.update_thread.start()
    
    def stop_camera(self):
        """Stop kamera"""
        self.controller.stop_camera()
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.system_btn.config(state='disabled', text="⚡ Aktifkan Kontrol Sistem")
        self.status_label.config(text="Status: Siap")
        self.video_label.config(image="", text="Kamera tidak aktif")
        
    def toggle_system_control(self):
        """Toggle kontrol sistem"""
        if self.controller.is_system_control_enabled:
            self.controller.disable_system_control()
            self.system_btn.config(text="⚡ Aktifkan Kontrol Sistem")
            self.status_label.config(text="Status: Kamera Aktif")
        else:
            if self.controller.enable_system_control():
                self.system_btn.config(text="🛑 Nonaktifkan Kontrol Sistem")
                self.status_label.config(text="Status: KONTROL SISTEM AKTIF")
    
    def update_sensitivity(self, value):
        """Update sensitivitas kursor"""
        self.controller.cursor_sensitivity = float(value)
    
    def update_threshold(self, value):
        """Update threshold click"""
        self.controller.click_threshold = float(value)
    
    def update_video(self):
        """Update video feed dalam thread terpisah"""
        while self.controller.is_running and self.is_gui_running:
            try:
                frame, gestures = self.controller.process_frame()
                if frame is not None:
                    # Resize frame untuk display
                    height, width = frame.shape[:2]
                    max_width, max_height = 640, 480
                    
                    if width > max_width or height > max_height:
                        scale = min(max_width/width, max_height/height)
                        new_width = int(width * scale)
                        new_height = int(height * scale)
                        frame = cv2.resize(frame, (new_width, new_height))
                    
                    # Convert untuk Tkinter
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(frame_rgb)
                    photo = ImageTk.PhotoImage(image)
                    
                    # Update GUI di main thread
                    self.root.after(0, self.update_video_label, photo)
                    self.root.after(0, self.update_fps_label)
                    
            except Exception as e:
                print(f"Error dalam update video: {e}")
                break
                
            time.sleep(1/30)  # Target 30 FPS
    
    def update_video_label(self, photo):
        """Update label video"""
        try:
            self.video_label.config(image=photo, text="")
            self.video_label.image = photo  # Keep reference
        except:
            pass
    
    def update_fps_label(self):
        """Update FPS label"""
        try:
            self.fps_label.config(text=f"FPS: {self.controller.current_fps}")
        except:
            pass
    
    def on_closing(self):
        """Handle penutupan aplikasi"""
        self.is_gui_running = False
        self.controller.stop_camera()
        self.root.destroy()
    
    def run(self):
        """Jalankan aplikasi"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Tampilkan peringatan awal
        warning_msg = """Selamat datang di CamMouse Pro!

Pastikan kamera Anda berfungsi dengan baik.
Gerakkan jari telunjuk untuk mengontrol kursor.
Satukan jempol dan telunjuk untuk klik kiri.
Satukan jempol dan jari tengah untuk klik kanan.

PERINGATAN: Fitur kontrol sistem akan mengontrol kursor di seluruh desktop!"""
        
        messagebox.showinfo("CamMouse Pro", warning_msg)
        
        self.root.mainloop()

def main():
    """Fungsi utama aplikasi"""
    try:
        app = CamMouseGUI()
        app.run()
    except KeyboardInterrupt:
        print("\\nAplikasi dihentikan oleh pengguna")
    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    main()
'''

# Save the script to a file
with open('cammouse_system_controller.py', 'w', encoding='utf-8') as f:
    f.write(system_cursor_script)

print("✅ File script Python telah dibuat: cammouse_system_controller.py")
print("📝 Script ini berisi implementasi lengkap untuk kontrol kursor sistem global")