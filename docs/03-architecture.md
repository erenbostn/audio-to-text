---

## DECISION LOG (AI-maintained)

- [2026-01-12] UI Framework Selection: customtkinter
  - **Decision:** Use customtkinter (modern wrapper for Tkinter) for all UI components
  - **Rationale:** Provides modern dark theme out-of-box, cross-platform compatibility, cleaner API than raw Tkinter
  - **Alternatives Considered:** PyQt6 (heavier), raw Tkinter (outdated look), Kivy (learning curve)
  - **Impact:** All UI modules (overlay.py, settings_window.py) depend on this library

- [2026-01-12] Overlay Window Implementation
  - **Decision:** Use CTkToplevel with overrideredirect(True) and attributes('-topmost', True)
  - **Rationale:** Frameless floating window that stays above all other applications
  - **Implementation Details:**
    - overrideredirect(True) removes window decorations (title bar, close button)
    - '-topmost' attribute ensures overlay is always visible
    - Hidden/shown based on recording state
  - **Impact:** Core visual feedback mechanism during recording

- [2026-01-12] Threading Model for Audio Recording
  - **Decision:** Run audio recording in separate non-blocking thread
  - **Rationale:** UI must remain responsive during recording; pynput listener also runs in daemon thread
  - **Implementation:** Use threading.Thread with daemon=True for recorder
  - **Impact:** recorder.py module, main.py initialization

- [2026-01-12] System Tray Integration Approach
  - **Decision:** Use pystray with Pillow for tray icon and menu
  - **Rationale:** Windows-only application needs minimize-to-tray capability; main overlay is frameless
  - **Implementation:** Tray icon with "Restore" and "Quit" menu items
  - **Impact:** tray.py module, main.py shutdown logic

- [2026-01-12] Text Injection Library Selection
  - **Decision:** Use pyautogui or keyboard library for Unicode support
  - **Rationale:** Turkish characters (ş, ı, ğ, ö, ç, ü) require proper Unicode handling
  - **Implementation:** Simulate keystrokes at current cursor position
  - **Impact:** input_simulator.py module

- [2026-01-12] Configuration Management Strategy
  - **Decision:** Use python-dotenv with .env file for API key storage
  - **Rationale:** Keeps credentials out of code; standard pattern for secret management
  - **Implementation:** Load GROQ_API_KEY at startup via config.py
  - **Impact:** config.py module, .env.example template

- [2026-01-12] Audio Feedback Mechanism
  - **Decision:** Use winsound (Windows-specific) for beep sounds
  - **Rationale:** Application is Windows-only; winsound is built-in, no external dependency
  - **Implementation:**
    - Start beep: 1000Hz, 200ms
    - Stop beep: 700Hz, 200ms
  - **Impact:** sound_feedback.py module

- [2026-01-12] Visual Design Language
  - **Decision:** Dark theme with glass/acrylic aesthetic per html.md concept
  - **Rationale:** Modern desktop utility aesthetic; matches OS dark mode preferences
  - **Implementation:**
    - set_appearance_mode("Dark")
    - set_default_color_theme("dark-blue")
    - Accent color: #FF6B35 (orange)
  - **Impact:** All UI components styling

---

# Technical Specification

# Technical Specification

## Core Technologies
- **Language:** Python 3.10+
- **OS:** Windows Only
- **UI Framework:** `customtkinter` (Modern UI wrapper for Tkinter)

## Libraries & Modules

### 1. Audio Recording
- **Library:** `sounddevice` and `numpy`.
- **Format:** Record raw stream and save as `.wav`.
- **Logic:** Run recording in a separate non-blocking thread to keep UI responsive.

### 2. User Interface (Modern Overlay & Settings)
- **Library:** `customtkinter`.
- **Theme:** `set_appearance_mode("Dark")`, `set_default_color_theme("dark-blue")`.
- **Overlay Window:**
    - Use `CTkToplevel` class.
    - Attributes: `overrideredirect(True)` (Frameless), `attributes('-topmost', True)` (Always on top).
    - Design: A small, rounded "pill" shape or compact box showing a "Recording..." label or icon.
    - Transparent Background: Use `attributes("-transparentcolor", ...)` if supported, or match the system dark theme background.
- **Settings Window:**
    - Standard `CTk` window for API Key input and Microphone selection.

### 3. System Tray
- **Library:** `pystray` and `Pillow`.
- **Function:** To minimize the app to the tray and allow the user to "Quit" completely since the main overlay is frameless.

### 4. Global Hotkey
- **Library:** `pynput.keyboard`.
- **Preference:** `GlobalHotKeys` listener running in a daemon thread.

### 5. Feedback
- **Audio:** `import winsound`.
    - Start Beep: `winsound.Beep(1000, 200)`
    - Stop Beep: `winsound.Beep(700, 200)`

### 6. API Interaction
- **Client:** `groq` python library.
- **Key Management:** Load `GROQ_API_KEY` from `.env` using `python-dotenv`.

### 7. Text Injection
- **Library:** `pyautogui` or `keyboard`.
- **Handling:** Ensure Unicode support for Turkish characters.
