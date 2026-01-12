---

## DECISION LOG (AI-maintained)

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
