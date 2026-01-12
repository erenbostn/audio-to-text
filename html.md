<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GroqWhisper - Functional Web Concept</title>
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        /* --- CSS STYLES (Aynen kopyalanmıştır) --- */
        :root {
            --bg-color: #0c0c0c;
            --glass-bg: rgba(255, 255, 255, 0.05);
            --glass-border: rgba(255, 255, 255, 0.1);
            --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
            --text-primary: #ffffff;
            --text-secondary: #a0a0a0;
            --accent-color: #FF6B35;
            --accent-glow: rgba(255, 107, 53, 0.4);
            --danger-color: #ff3b30;
            --input-bg: rgba(0, 0, 0, 0.3);
        }

        body {
            margin: 0;
            padding: 0;
            font-family: 'Inter', 'Segoe UI', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            min-height: 960px;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
        }

        .poster-container {
            width: 720px;
            min-height: 960px;
            position: relative;
            background: radial-gradient(circle at top right, #1a1a2e, #000000);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        /* Grid Texture & Blobs */
        .grid-bg {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px);
            background-size: 40px 40px;
            z-index: 0; pointer-events: none;
        }
        .glow-blob { position: absolute; border-radius: 50%; filter: blur(100px); opacity: 0.4; z-index: 0; }
        .blob-1 { top: -100px; right: -100px; width: 400px; height: 400px; background: #4a2c2c; }
        .blob-2 { bottom: -50px; left: -100px; width: 400px; height: 400px; background: #2c3a4a; }
        .blob-3 { top: 40%; left: 30%; width: 200px; height: 200px; background: var(--accent-color); opacity: 0.15; }

        /* Header */
        .header { padding: 40px 40px 20px; z-index: 2; }
        .brand-tag {
            display: inline-flex; align-items: center; padding: 6px 12px;
            background: rgba(255, 255, 255, 0.05); border-radius: 20px;
            font-size: 12px; font-weight: 600; letter-spacing: 1px; text-transform: uppercase;
            margin-bottom: 16px; border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .brand-tag i { font-size: 14px; margin-right: 6px; color: var(--accent-color); }
        h1 { font-size: 48px; margin: 0; font-weight: 700; letter-spacing: -1px; background: linear-gradient(to right, #fff, #aaa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .subtitle { font-size: 18px; color: var(--text-secondary); margin-top: 8px; font-weight: 300; }

        /* Content */
        .content-area { flex: 1; position: relative; z-index: 2; padding: 20px 40px 40px; display: flex; flex-direction: column; justify-content: center; }

        /* Glass Window */
        .glass-window {
            background: rgba(30, 30, 30, 0.6); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.1); border-top: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 16px; box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6); padding: 0;
            width: 100%; position: relative;
        }
        .window-header { padding: 16px 24px; border-bottom: 1px solid rgba(255, 255, 255, 0.05); display: flex; justify-content: space-between; align-items: center; }
        .window-title { font-size: 14px; font-weight: 500; }
        .window-controls { display: flex; gap: 8px; }
        .control-dot { width: 12px; height: 12px; border-radius: 50%; }
        .close-dot { background: #ff5f56; } .min-dot { background: #ffbd2e; } .max-dot { background: #27c93f; }

        .window-body { padding: 24px; display: flex; flex-direction: column; gap: 20px; }

        /* Form Elements */
        .form-group { display: flex; flex-direction: column; gap: 8px; }
        .form-label { font-size: 12px; color: var(--text-secondary); font-weight: 500; margin-left: 4px; }
        .input-wrapper { position: relative; display: flex; align-items: center; }
        .input-field {
            width: 100%; background: var(--input-bg); border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px; padding: 12px 16px; color: white; font-family: inherit; font-size: 14px;
            outline: none; transition: all 0.2s; box-sizing: border-box;
        }
        .input-field:focus { border-color: var(--accent-color); box-shadow: 0 0 0 2px rgba(255, 107, 53, 0.2); }
        .input-icon { position: absolute; right: 12px; color: var(--text-secondary); font-size: 18px; pointer-events: none; }

        /* Toggles */
        .settings-row { display: flex; justify-content: space-between; align-items: center; padding: 8px 0; }
        .toggle-switch {
            position: relative; width: 44px; height: 24px; background: rgba(255, 255, 255, 0.1);
            border-radius: 12px; cursor: pointer; transition: background 0.3s;
        }
        .toggle-switch.active { background: var(--accent-color); }
        .toggle-thumb {
            position: absolute; top: 2px; left: 2px; width: 20px; height: 20px;
            background: white; border-radius: 50%; transition: transform 0.3s cubic-bezier(0.4, 0.0, 0.2, 1);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }
        .toggle-switch.active .toggle-thumb { transform: translateX(20px); }

        /* Button */
        .btn-save {
            background: var(--accent-color); color: white; border: none; padding: 14px;
            border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; margin-top: 8px;
            box-shadow: 0 4px 15px var(--accent-glow); transition: all 0.2s;
        }
        .btn-save:hover { transform: translateY(-2px); box-shadow: 0 6px 20px var(--accent-glow); }

        /* Floating Overlay */
        .floating-overlay {
            position: absolute; top: 60px; right: 20px; width: 200px;
            background: rgba(20, 20, 20, 0.7); backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.15); border-radius: 50px;
            padding: 10px 20px; display: flex; align-items: center; justify-content: space-between;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5); z-index: 10;
            animation: float 6s ease-in-out infinite; cursor: move; /* Sürüklenebilir */
        }
        @keyframes float { 0% { transform: translateY(0px); } 50% { transform: translateY(-10px); } 100% { transform: translateY(0px); } }

        .mic-container { position: relative; display: flex; align-items: center; justify-content: center; width: 32px; height: 32px; background: rgba(255, 59, 48, 0.15); border-radius: 50%; }
        .mic-icon { color: var(--danger-color); font-size: 18px; z-index: 2; }
        .pulse-ring {
            position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
            width: 100%; height: 100%; border-radius: 50%; border: 2px solid var(--danger-color);
            opacity: 0; animation: pulse 2s infinite;
        }
        @keyframes pulse { 0% { width: 100%; height: 100%; opacity: 0.8; } 100% { width: 200%; height: 200%; opacity: 0; } }

        .status-text { font-size: 13px; font-weight: 500; color: white; margin-right: 8px; }
        .waveform { display: flex; align-items: center; gap: 2px; height: 16px; }
        .bar { width: 3px; background: var(--accent-color); border-radius: 2px; animation: wave 1s ease-in-out infinite; }
        .bar:nth-child(1) { height: 6px; animation-delay: 0.1s; } .bar:nth-child(2) { height: 12px; animation-delay: 0.2s; }
        .bar:nth-child(3) { height: 8px; animation-delay: 0.3s; } .bar:nth-child(4) { height: 14px; animation-delay: 0.1s; }
        .bar:nth-child(5) { height: 6px; animation-delay: 0.4s; }
        @keyframes wave { 0%, 100% { transform: scaleY(1); } 50% { transform: scaleY(1.5); } }

        /* Specs */
        .specs { margin-top: 40px; display: flex; gap: 20px; padding: 20px; background: rgba(255, 255, 255, 0.03); border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.05); }
        .spec-item { flex: 1; }
        .spec-title { font-size: 12px; color: var(--accent-color); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
        .spec-desc { font-size: 13px; color: var(--text-secondary); line-height: 1.4; }

        /* Footer */
        .footer { padding: 20px 40px; display: flex; justify-content: space-between; align-items: flex-end; z-index: 2; border-top: 1px solid rgba(255, 255, 255, 0.05); background: rgba(0,0,0,0.2); backdrop-filter: blur(10px); }
        .designer-info { font-size: 12px; color: var(--text-secondary); }
        .version-badge { background: rgba(255, 255, 255, 0.1); padding: 4px 8px; border-radius: 4px; font-size: 10px; color: white; }
    </style>
</head>
<body>
    <div class="poster-container">
        <div class="grid-bg"></div>
        <div class="glow-blob blob-1"></div>
        <div class="glow-blob blob-2"></div>
        <div class="glow-blob blob-3"></div>

        <div class="header">
            <div class="brand-tag"><i class="material-icons">auto_awesome</i>GroqWhisper Concept</div>
            <h1>Voice to Text<br>Utility</h1>
            <div class="subtitle">Web Concept / Interactive</div>
        </div>

        <div class="content-area">
            
            <!-- Sürüklenebilir Overlay -->
            <div class="floating-overlay" id="floatingOverlay">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div class="mic-container">
                        <i class="material-icons mic-icon">mic</i>
                        <div class="pulse-ring"></div>
                    </div>
                    <span class="status-text" id="statusText">Listening...</span>
                </div>
                <div class="waveform">
                    <div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div>
                </div>
            </div>

            <div class="glass-window">
                <div class="window-header">
                    <span class="window-title">GroqWhisper Settings</span>
                    <div class="window-controls">
                        <div class="control-dot min-dot"></div><div class="control-dot max-dot"></div><div class="control-dot close-dot"></div>
                    </div>
                </div>
                <div class="window-body">
                    <!-- Inputs -->
                    <div class="form-group">
                        <label class="form-label">Groq API Key</label>
                        <div class="input-wrapper">
                            <input type="password" id="apiKey" value="gsk_..." class="input-field">
                            <i class="material-icons input-icon" style="font-size: 16px;">vpn_key</i>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Input Device</label>
                        <div class="input-wrapper">
                            <select class="input-field" style="appearance: none; cursor:pointer;">
                                <option>Default Microphone (Realtek Audio)</option>
                                <option>External USB Mic</option>
                            </select>
                        </div>
                    </div>

                    <div class="form-group">
                        <label class="form-label">Activation Hotkey</label>
                        <div class="input-wrapper">
                            <input type="text" value="Ctrl + Alt + Space" class="input-field" readonly style="cursor: default;">
                            <i class="material-icons input-icon">keyboard</i>
                        </div>
                    </div>

                    <!-- Interactive Toggles -->
                    <div class="settings-row">
                        <span style="font-size: 14px; color: white;">Play Beep Sound</span>
                        <div class="toggle-switch" onclick="toggleSwitch(this)"><div class="toggle-thumb"></div></div>
                    </div>
                    <div class="settings-row">
                        <span style="font-size: 14px; color: white;">Show Floating Overlay</span>
                        <div class="toggle-switch active" onclick="toggleSwitch(this, 'overlay')"><div class="toggle-thumb"></div></div>
                    </div>

                    <button class="btn-save" onclick="saveConfig()">Save Configuration</button>
                </div>
            </div>

            <div class="specs">
                <div class="spec-item">
                    <div class="spec-title">Visual Style</div>
                    <div class="spec-desc">Acrylic material, deep charcoal.</div>
                </div>
                <div class="spec-item">
                    <div class="spec-title">Typography</div>
                    <div class="spec-desc">Inter (Sans-serif), clean hierarchy.</div>
                </div>
            </div>
        </div>

        <div class="footer">
            <div class="designer-info">Designed for Desktop Utility Experience<br><span style="opacity: 0.6;">2026 UI Concept</span></div>
            <div class="version-badge">v2.0.4 Web</div>
        </div>
    </div>

    <!-- INTERACTIVITY SCRIPT -->
    <script>
        // 1. Toggle Switch Mantığı
        function toggleSwitch(element, type) {
            element.classList.toggle('active');
            
            // Overlay Toggle Mantığı
            if(type === 'overlay') {
                const overlay = document.getElementById('floatingOverlay');
                if(element.classList.contains('active')) {
                    overlay.style.opacity = '1';
                    overlay.style.pointerEvents = 'all';
                } else {
                    overlay.style.opacity = '0';
                    overlay.style.pointerEvents = 'none';
                }
            }
        }

        // 2. Save Button Mantığı
        function saveConfig() {
            const btn = document.querySelector('.btn-save');
            const originalText = btn.innerText;
            const apiKey = document.getElementById('apiKey').value;

            btn.innerText = "Saving...";
            btn.style.background = "#4CAF50"; // Yeşil renk

            setTimeout(() => {
                alert(`Configuration Saved!\nAPI Key: ${apiKey}`);
                btn.innerText = originalText;
                btn.style.background = ""; // Rengi geri al
            }, 800);
        }

        // 3. Floating Overlay Sürükleme Mantığı (Drag & Drop)
        const overlay = document.getElementById('floatingOverlay');
        let isDragging = false;
        let startX, startY, initialLeft, initialTop;

        overlay.addEventListener('mousedown', (e) => {
            isDragging = true;
            startX = e.clientX;
            startY = e.clientY;
            
            const rect = overlay.getBoundingClientRect();
            // Offset hesapla (absolute pozisyonlandırma için)
            // Ancak bu yapı 'transform: translateY' kullandığı için suruklemede titreyebilir.
            // Basitlik için CSS'teki 'transform' animasyonunu durduralım.
            overlay.style.animation = 'none';
            
            initialLeft = rect.left;
            initialTop = rect.top;
        });

        document.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            const dx = e.clientX - startX;
            const dy = e.clientY - startY;
            
            // 'top' ve 'right' değerlerini güncellemek yerine left/top kullanacağız
            overlay.style.right = 'auto'; 
            overlay.style.left = `${initialLeft + dx}px`;
            overlay.style.top = `${initialTop + dy}px`;
        });

        document.addEventListener('mouseup', () => {
            isDragging = false;
        });
    </script>
</body>
</html>