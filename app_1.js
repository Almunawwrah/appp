// HandCursor Pro - Enhanced Application JavaScript

class HandCursorApp {
    constructor() {
        this.isSystemActive = false;
        this.isCameraActive = false;
        this.fps = 0;
        this.gestureData = null;
        this.systemData = null;
        this.deploymentData = null;
        this.performanceData = null;
        this.animationId = null;
        this.fpsInterval = null;
        this.performanceInterval = null;
        
        this.init();
    }

    init() {
        this.loadApplicationData();
        this.setupEventListeners();
        this.initializeInterface();
        this.startPerformanceMonitoring();
    }

    loadApplicationData() {
        // Load data from the provided JSON structure
        this.gestureData = [
            {
                name: "Cursor Movement",
                description: "Index finger tracking for cursor position",
                landmark: "Index fingertip (8)",
                status: "Ready",
                confidence: 0
            },
            {
                name: "Left Click",
                description: "Thumb and index finger pinch",
                landmark: "Thumb (4) + Index (8)",
                status: "Ready",
                confidence: 0
            },
            {
                name: "Right Click", 
                description: "Thumb and middle finger pinch",
                landmark: "Thumb (4) + Middle (12)",
                status: "Ready",
                confidence: 0
            },
            {
                name: "Scroll",
                description: "Two finger vertical movement",
                landmark: "Index (8) + Middle (12)",
                status: "Ready",
                confidence: 0
            }
        ];

        this.systemData = [
            {
                component: "MediaPipe Hands",
                status: "Loaded",
                version: "0.10.9",
                performance: "Ready"
            },
            {
                component: "PyAutoGUI",
                status: "Ready",
                version: "0.9.54",
                permissions: "Granted"
            },
            {
                component: "Camera Access",
                status: "Ready",
                resolution: "1280x720",
                device: "USB Camera"
            },
            {
                component: "System Control",
                status: "Ready",
                scope: "Global",
                platform: "Windows 10"
            }
        ];

        this.deploymentData = [
            {
                method: "PyInstaller",
                platform: "Windows",
                size: "~150MB",
                requirements: "Python 3.8+"
            },
            {
                method: "Electron",
                platform: "Cross-platform", 
                size: "~200MB",
                requirements: "Node.js"
            },
            {
                method: "cx_Freeze",
                platform: "Windows/Mac/Linux",
                size: "~120MB", 
                requirements: "Python 3.7+"
            }
        ];

        this.performanceData = {
            fps: 0,
            latency: "--",
            cpuUsage: "--",
            memoryUsage: "--",
            accuracy: "--"
        };
    }

    setupEventListeners() {
        // Theme toggle
        const themeToggle = document.getElementById('themeToggle');
        themeToggle?.addEventListener('click', () => this.toggleTheme());

        // Camera controls
        const startCamera = document.getElementById('startCamera');
        startCamera?.addEventListener('click', () => this.toggleCamera());

        // System control
        const enableSystem = document.getElementById('enableSystem');
        enableSystem?.addEventListener('click', () => this.toggleSystemControl());

        // Calibration
        const calibrateSystem = document.getElementById('calibrateSystem');
        calibrateSystem?.addEventListener('click', () => this.startCalibration());

        // Sensitivity sliders
        this.setupSliders();

        // Settings tabs
        this.setupTabs();

        // Deployment actions
        this.setupDeploymentActions();

        // Keyboard shortcuts
        this.setupKeyboardShortcuts();
    }

    setupSliders() {
        const sliders = [
            { id: 'cursorSensitivity', suffix: 'x' },
            { id: 'gestureThreshold', suffix: '' },
            { id: 'smoothing', suffix: '' }
        ];

        sliders.forEach(slider => {
            const element = document.getElementById(slider.id);
            if (element) {
                const valueDisplay = element.nextElementSibling;
                element.addEventListener('input', (e) => {
                    if (valueDisplay) {
                        valueDisplay.textContent = e.target.value + slider.suffix;
                    }
                    this.updateGestureSettings();
                });
            }
        });
    }

    setupTabs() {
        const tabButtons = document.querySelectorAll('.tab-btn');
        const tabContents = document.querySelectorAll('.tab-content');

        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetTab = button.getAttribute('data-tab');
                
                // Update button states
                tabButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                
                // Update content visibility
                tabContents.forEach(content => {
                    content.classList.remove('active');
                    if (content.id === targetTab) {
                        content.classList.add('active');
                    }
                });
            });
        });
    }

    setupDeploymentActions() {
        const generateBtn = document.getElementById('generateExecutable');
        const copyBtn = document.getElementById('copyBuildScript');
        const docsBtn = document.getElementById('openDocs');

        generateBtn?.addEventListener('click', () => this.simulateExecutableGeneration());
        copyBtn?.addEventListener('click', () => this.copyBuildScript());
        docsBtn?.addEventListener('click', () => this.openDocumentation());
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.shiftKey && e.key === 'H') {
                e.preventDefault();
                this.toggleSystemControl();
            }
            
            if (e.ctrlKey && e.key === ' ') {
                e.preventDefault();
                this.toggleCamera();
            }

            if (e.ctrlKey && e.altKey && e.key === 'c') {
                e.preventDefault();
                this.startCalibration();
            }
        });
    }

    initializeInterface() {
        this.populateGestureStatus();
        this.populateSystemComponents();
        this.populateDeploymentOptions();
        this.updatePerformanceMetrics();
        this.updateSystemStatus();
    }

    updateSystemStatus() {
        const statusIndicator = document.getElementById('systemStatus');
        if (statusIndicator) {
            const statusDot = statusIndicator.querySelector('.status-dot');
            const statusText = statusIndicator.querySelector('span');
            
            if (this.isSystemActive) {
                statusDot?.classList.add('active');
                if (statusText) statusText.textContent = 'Kontrol Aktif';
            } else if (this.isCameraActive) {
                statusDot?.classList.remove('active');
                if (statusText) statusText.textContent = 'Kamera Aktif';
            } else {
                statusDot?.classList.remove('active');
                if (statusText) statusText.textContent = 'Sistem Siap';
            }
        }
    }

    populateGestureStatus() {
        const container = document.getElementById('gestureStatus');
        if (!container) return;

        container.innerHTML = this.gestureData.map(gesture => `
            <div class="gesture-item ${gesture.status.toLowerCase()}">
                <div>
                    <div class="gesture-name">${gesture.name}</div>
                    <div class="gesture-description">${gesture.description}</div>
                    <div class="gesture-description">Landmark: ${gesture.landmark}</div>
                </div>
                <div class="gesture-confidence">${gesture.confidence}%</div>
            </div>
        `).join('');
    }

    populateSystemComponents() {
        const container = document.getElementById('componentsList');
        if (!container) return;

        container.innerHTML = this.systemData.map(component => `
            <div class="component-item">
                <div>
                    <div class="component-name">${component.component}</div>
                    <div class="component-version">v${component.version}</div>
                </div>
                <div class="status status--${this.getStatusClass(component.status)}">
                    ${component.status}
                </div>
            </div>
        `).join('');
    }

    getStatusClass(status) {
        const statusMap = {
            'loaded': 'success',
            'ready': 'success', 
            'active': 'success',
            'enabled': 'success',
            'offline': 'error',
            'error': 'error'
        };
        return statusMap[status.toLowerCase()] || 'info';
    }

    populateDeploymentOptions() {
        const container = document.getElementById('deploymentOptions');
        if (!container) return;

        container.innerHTML = this.deploymentData.map(option => `
            <div class="deployment-option">
                <h4>${option.method}</h4>
                <div class="deployment-details">
                    <div class="deployment-detail">
                        <span>Platform:</span>
                        <span>${option.platform}</span>
                    </div>
                    <div class="deployment-detail">
                        <span>Ukuran:</span>
                        <span>${option.size}</span>
                    </div>
                    <div class="deployment-detail">
                        <span>Requirements:</span>
                        <span>${option.requirements}</span>
                    </div>
                </div>
            </div>
        `).join('');
    }

    updatePerformanceMetrics() {
        const elements = {
            latency: document.getElementById('latency'),
            cpuUsage: document.getElementById('cpuUsage'),
            memoryUsage: document.getElementById('memoryUsage'),
            accuracy: document.getElementById('accuracy')
        };

        Object.keys(elements).forEach(key => {
            if (elements[key]) {
                elements[key].textContent = this.performanceData[key];
            }
        });
    }

    toggleTheme() {
        const html = document.documentElement;
        const themeToggle = document.getElementById('themeToggle');
        
        const currentTheme = html.getAttribute('data-color-scheme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        html.setAttribute('data-color-scheme', newTheme);
        
        if (themeToggle) {
            themeToggle.textContent = newTheme === 'dark' ? '☀️ Light' : '🌙 Dark';
        }

        // Add transition class
        document.body.classList.add('theme-transition');
        setTimeout(() => {
            document.body.classList.remove('theme-transition');
        }, 250);
    }

    toggleCamera() {
        const startCamera = document.getElementById('startCamera');
        const enableSystem = document.getElementById('enableSystem');
        const cameraStatus = document.getElementById('cameraStatus');
        const cameraContainer = document.getElementById('cameraContainer');
        const cameraCanvas = document.getElementById('cameraCanvas');
        const placeholder = document.getElementById('cameraPlaceholder');

        this.isCameraActive = !this.isCameraActive;

        if (this.isCameraActive) {
            // Update button
            startCamera.textContent = '⏸️ Stop Kamera';
            startCamera.classList.remove('btn--primary');
            startCamera.classList.add('btn--secondary');
            
            // Update camera status
            if (cameraStatus) {
                cameraStatus.textContent = '🟢 Online';
                cameraStatus.classList.add('active');
            }

            // Enable system control
            if (enableSystem) {
                enableSystem.disabled = false;
                enableSystem.classList.remove('btn--secondary');
                enableSystem.classList.add('btn--outline');
            }

            // Show camera simulation
            if (placeholder) placeholder.style.display = 'none';
            if (cameraCanvas) {
                cameraCanvas.style.display = 'block';
                this.startCameraSimulation();
            }

            // Update gesture data for active camera
            this.gestureData.forEach(gesture => {
                gesture.confidence = Math.floor(Math.random() * 30) + 70;
                gesture.status = 'Ready';
            });

            this.startFPSCounter();
            this.populateGestureStatus();
            this.updatePerformanceData();
        } else {
            // Update button
            startCamera.textContent = '📹 Mulai Kamera';
            startCamera.classList.remove('btn--secondary');
            startCamera.classList.add('btn--primary');
            
            // Update camera status
            if (cameraStatus) {
                cameraStatus.textContent = '📴 Offline';
                cameraStatus.classList.remove('active');
            }

            // Disable system control
            if (enableSystem) {
                enableSystem.disabled = true;
                enableSystem.classList.remove('btn--outline');
                enableSystem.classList.add('btn--secondary');
            }

            // Stop system if active
            if (this.isSystemActive) {
                this.toggleSystemControl();
            }

            // Hide camera simulation
            if (placeholder) placeholder.style.display = 'block';
            if (cameraCanvas) cameraCanvas.style.display = 'none';

            // Reset gesture data
            this.gestureData.forEach(gesture => {
                gesture.confidence = 0;
                gesture.status = 'Ready';
            });

            this.stopFPSCounter();
            this.populateGestureStatus();
            this.resetPerformanceData();
        }

        this.updateSystemStatus();
    }

    startCameraSimulation() {
        const canvas = document.getElementById('cameraCanvas');
        const gestureInfo = document.getElementById('gestureInfo');
        
        if (!canvas) return;

        const ctx = canvas.getContext('2d');
        gestureInfo.style.display = 'block';
        
        let handPosition = { x: 320, y: 200 };
        let targetPosition = { x: 320, y: 200 };
        
        const animate = () => {
            if (!this.isCameraActive) {
                gestureInfo.style.display = 'none';
                return;
            }

            // Clear canvas
            ctx.fillStyle = '#1a1a2e';
            ctx.fillRect(0, 0, canvas.width, canvas.height);

            // Update hand position smoothly
            handPosition.x += (targetPosition.x - handPosition.x) * 0.1;
            handPosition.y += (targetPosition.y - handPosition.y) * 0.1;

            // Randomly update target position
            if (Math.random() < 0.02) {
                targetPosition.x = Math.random() * (canvas.width - 100) + 50;
                targetPosition.y = Math.random() * (canvas.height - 100) + 50;
            }

            // Draw hand landmarks
            this.drawHandLandmarks(ctx, handPosition);
            
            // Update gesture info
            this.updateGestureInfo();

            this.animationId = requestAnimationFrame(animate);
        };

        animate();
    }

    drawHandLandmarks(ctx, center) {
        // Define hand landmark positions relative to center
        const landmarks = [
            { x: center.x, y: center.y + 50, label: 'Wrist', color: '#FFC185' },
            { x: center.x - 20, y: center.y + 20, label: 'Thumb', color: '#B4413C' },
            { x: center.x, y: center.y - 30, label: 'Index', color: '#1FB8CD' },
            { x: center.x + 20, y: center.y - 25, label: 'Middle', color: '#5D878F' },
            { x: center.x + 35, y: center.y - 15, label: 'Ring', color: '#D2BA4C' },
            { x: center.x + 45, y: center.y, label: 'Pinky', color: '#964325' }
        ];

        // Draw connections
        landmarks.forEach((point, index) => {
            if (index > 0) {
                ctx.beginPath();
                ctx.moveTo(landmarks[0].x, landmarks[0].y);
                ctx.lineTo(point.x, point.y);
                ctx.strokeStyle = '#5D878F';
                ctx.lineWidth = 2;
                ctx.stroke();
            }
        });

        // Draw landmark points
        landmarks.forEach((point, index) => {
            ctx.beginPath();
            ctx.arc(point.x, point.y, index === 2 ? 8 : 5, 0, 2 * Math.PI);
            ctx.fillStyle = point.color;
            ctx.fill();
            
            if (index === 2) { // Highlight index finger
                ctx.strokeStyle = '#1FB8CD';
                ctx.lineWidth = 3;
                ctx.stroke();
            }
        });

        // Draw gesture detection area around index finger
        ctx.beginPath();
        ctx.arc(landmarks[2].x, landmarks[2].y, 25, 0, 2 * Math.PI);
        ctx.strokeStyle = '#1FB8CD';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 5]);
        ctx.stroke();
        ctx.setLineDash([]);

        // Draw cursor indicator
        ctx.beginPath();
        ctx.arc(landmarks[2].x, landmarks[2].y, 3, 0, 2 * Math.PI);
        ctx.fillStyle = '#DB4545';
        ctx.fill();
    }

    updateGestureInfo() {
        const currentGesture = document.getElementById('currentGesture');
        const gestureConfidence = document.getElementById('gestureConfidence');
        
        // Simulate gesture detection
        const gestures = ['Cursor Movement', 'Left Click', 'Right Click', 'Scroll'];
        const randomGesture = gestures[Math.floor(Math.random() * gestures.length)];
        const confidence = Math.floor(Math.random() * 25) + 75;
        
        if (currentGesture) currentGesture.textContent = randomGesture;
        if (gestureConfidence) gestureConfidence.textContent = `${confidence}%`;
    }

    toggleSystemControl() {
        const enableSystem = document.getElementById('enableSystem');

        this.isSystemActive = !this.isSystemActive;

        if (this.isSystemActive) {
            enableSystem.textContent = '⏹️ Nonaktifkan Kontrol';
            enableSystem.classList.remove('btn--outline');
            enableSystem.classList.add('btn--error');
            
            // Start gesture simulation
            this.simulateGestureDetection();
            
            // Update performance for active system
            this.performanceData = {
                fps: 30,
                latency: "45ms",
                cpuUsage: "15%", 
                memoryUsage: "180MB",
                accuracy: "94%"
            };
        } else {
            enableSystem.textContent = '⚡ Aktifkan Kontrol Sistem';
            enableSystem.classList.remove('btn--error');
            enableSystem.classList.add('btn--outline');
            
            // Stop gesture simulation
            if (this.gestureInterval) {
                clearInterval(this.gestureInterval);
            }
        }

        this.updateSystemStatus();
        this.updatePerformanceMetrics();
    }

    simulateGestureDetection() {
        if (!this.isSystemActive) return;

        this.gestureInterval = setInterval(() => {
            if (!this.isSystemActive) return;

            this.gestureData.forEach(gesture => {
                gesture.confidence = Math.max(70, Math.min(99, gesture.confidence + (Math.random() - 0.5) * 10));
                
                if (Math.random() < 0.3) {
                    const statuses = ['Active', 'Detected', 'Ready'];
                    gesture.status = statuses[Math.floor(Math.random() * statuses.length)];
                }
            });

            this.populateGestureStatus();
        }, 2000);
    }

    startCalibration() {
        const button = document.getElementById('calibrateSystem');
        const originalText = button.textContent;
        
        button.textContent = '🔄 Kalibrasi...';
        button.disabled = true;
        
        setTimeout(() => {
            button.textContent = '✅ Kalibrasi Selesai!';
            setTimeout(() => {
                button.textContent = originalText;
                button.disabled = false;
            }, 2000);
        }, 3000);
    }

    updateGestureSettings() {
        // Simulate updating gesture settings based on sliders
        if (this.isCameraActive || this.isSystemActive) {
            this.populateGestureStatus();
        }
    }

    startFPSCounter() {
        const fpsElement = document.getElementById('fpsCounter');
        if (!fpsElement) return;

        this.fpsInterval = setInterval(() => {
            this.fps = Math.floor(Math.random() * 5) + 28; // 28-32 FPS simulation
            fpsElement.textContent = `${this.fps} FPS`;
        }, 1000);
    }

    stopFPSCounter() {
        if (this.fpsInterval) {
            clearInterval(this.fpsInterval);
            const fpsElement = document.getElementById('fpsCounter');
            if (fpsElement) fpsElement.textContent = '0 FPS';
        }
    }

    updatePerformanceData() {
        if (this.isCameraActive) {
            this.performanceData = {
                fps: this.fps,
                latency: "45ms",
                cpuUsage: "8%",
                memoryUsage: "120MB", 
                accuracy: "85%"
            };
        }
        this.updatePerformanceMetrics();
    }

    resetPerformanceData() {
        this.performanceData = {
            fps: 0,
            latency: "--",
            cpuUsage: "--",
            memoryUsage: "--",
            accuracy: "--"
        };
        this.updatePerformanceMetrics();
    }

    startPerformanceMonitoring() {
        // Update performance metrics every 3 seconds
        this.performanceInterval = setInterval(() => {
            if (this.isCameraActive || this.isSystemActive) {
                this.performanceData.cpuUsage = `${Math.floor(Math.random() * 10) + (this.isSystemActive ? 15 : 8)}%`;
                this.performanceData.memoryUsage = `${Math.floor(Math.random() * 20) + (this.isSystemActive ? 170 : 120)}MB`;
                this.performanceData.latency = `${Math.floor(Math.random() * 10) + 40}ms`;
                this.performanceData.accuracy = `${Math.floor(Math.random() * 6) + (this.isSystemActive ? 92 : 85)}%`;
                
                this.updatePerformanceMetrics();
            }
        }, 3000);
    }

    simulateExecutableGeneration() {
        const button = document.getElementById('generateExecutable');
        const originalText = button.textContent;
        
        button.textContent = '⏳ Generating...';
        button.disabled = true;
        button.classList.add('loading');
        
        setTimeout(() => {
            button.textContent = '✅ Generated Successfully!';
            setTimeout(() => {
                button.textContent = originalText;
                button.disabled = false;
                button.classList.remove('loading');
            }, 2000);
        }, 3000);
    }

    copyBuildScript() {
        const script = `# HandCursor Pro Build Script
pip install pyinstaller mediapipe pyautogui opencv-python
pyinstaller --onefile --windowed --add-data "assets;assets" --name "HandCursorPro" main.py
echo "Build completed! Check dist/ folder for executable."`;

        navigator.clipboard.writeText(script).then(() => {
            const button = document.getElementById('copyBuildScript');
            const originalText = button.textContent;
            button.textContent = '✅ Copied!';
            setTimeout(() => {
                button.textContent = originalText;
            }, 2000);
        }).catch(() => {
            // Fallback for browsers that don't support clipboard API
            const button = document.getElementById('copyBuildScript');
            const originalText = button.textContent;
            button.textContent = '📋 Script Ready!';
            setTimeout(() => {
                button.textContent = originalText;
            }, 2000);
        });
    }

    openDocumentation() {
        // Simulate opening documentation
        alert('Dokumentasi lengkap akan dibuka di tab baru. Fitur ini akan tersedia dalam versi final aplikasi desktop.');
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new HandCursorApp();
    
    // Add enhanced interactivity
    addEnhancedInteractivity();
});

function addEnhancedInteractivity() {
    // Add hover effects for interactive elements
    const interactiveElements = document.querySelectorAll('.gesture-item, .component-item, .deployment-option, .metric');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
            this.style.transition = 'transform 0.2s ease';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    // Add click feedback to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Create ripple effect
            const rect = this.getBoundingClientRect();
            const ripple = document.createElement('span');
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.cssText = `
                position: absolute;
                border-radius: 50%;
                transform: scale(0);
                animation: ripple 600ms linear;
                background-color: rgba(255, 255, 255, 0.6);
                width: ${size}px;
                height: ${size}px;
                left: ${x}px;
                top: ${y}px;
            `;
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Add CSS for ripple animation
    if (!document.getElementById('ripple-styles')) {
        const style = document.createElement('style');
        style.id = 'ripple-styles';
        style.textContent = `
            @keyframes ripple {
                to {
                    transform: scale(4);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }
}