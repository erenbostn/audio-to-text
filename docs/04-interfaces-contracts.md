# Interfaces & Contracts

This document defines **external behavior contracts**.
These contracts are binding and must not be changed implicitly.

If a task requires changing any contract:

- The change must be documented here FIRST (append-only)
- The impact must be explicitly stated
- Backward compatibility must be considered

## CONTRACT CHANGE LOG (AI-maintained)

> Records all intentional changes to external behavior.
> Append-only. Do not rewrite or remove previous entries.

- [YYYY-MM-DD] [Short change title]
  - Change type: (Route / Query param / Response shape / SEO / Other)
  - Previous behavior:
  - New behavior:
  - Compatibility notes: (breaking / backward-compatible / migration notes)

---

## Interface Contracts

### HOT-001: Global Hotkey Interface
**Purpose:** Toggle recording state via global keyboard combination

**Contract:**
- **Default Hotkey:** `Ctrl+Alt+K` (changed from Ctrl+Alt+Space)
- **Listener Type:** Global daemon thread (pynput.keyboard.GlobalHotKeys)
- **Behavior:**
  - Press once: Start recording (if idle)
  - Press again: Stop recording (if recording)
  - Toggle only: No hold-to-record behavior

**Output:**
- Triggers state change in recorder module
- Activates/deactivates floating overlay
- Plays beep sound (1000Hz start, 700Hz stop)

---

### REC-001: Audio Recording Interface
**Purpose:** Capture and save audio from selected device

**Contract:**
- **Input Device:** User-selected microphone (default system mic)
- **Output Format:** `.wav` file (temporary location)
- **Threading:** Non-blocking separate thread
- **State Management:** Recording state persisted across hotkey presses

**Requirements:**
- MUST maintain UI responsiveness during recording
- MUST handle recording interruption gracefully
- MUST save to temp file with unique identifier

---

### TRX-001: Groq API Transcription Interface
**Purpose:** Send audio for speech-to-text conversion

**Contract:**
- **API Client:** groq Python library
- **Model:** whisper-large-v3
- **Authentication:** `GROQ_API_KEY` from .env file
- **Input:** Temporary .wav file path, language code (default: "tr" for Turkish)
- **Output:** Transcribed text (string)
- **Retry Logic:** 3 attempts with exponential backoff for network errors

**Error Handling:**
- API failure: Display error to user, do not inject text
- Invalid API key: Prompt user to configure in settings
- Network error: Retry up to 3 times with exponential backoff

---

### INJ-001: Text Injection Interface
**Purpose:** Simulate keyboard input to insert transcribed text

**Contract:**
- **Method:** pyautogui or keyboard library
- **Input:** Transcribed text string
- **Target:** Current cursor position (system-wide)

**Requirements:**
- MUST support Unicode characters (ş, ı, ğ, ö, ç, ü, etc.)
- MUST respect active application focus
- MUST inject at natural typing speed (configurable)

---

### UI-001: Floating Overlay Interface
**Purpose:** Display recording status to user

**Contract:**
- **Window Type:** CTkToplevel (customtkinter)
- **Attributes:**
  - `overrideredirect(True)` - Frameless window
  - `attributes('-topmost', True)` - Always on top
- **Visibility:** Shown when recording, hidden when idle
- **Position:** Floating, draggable (optional)
- **Content:**
  - Microphone icon with pulse animation
  - "Recording..." status text
  - Waveform visualization bars

---

### CFG-001: Settings Window Interface
**Purpose:** User configuration and preferences

**Contract:**
- **Window Type:** CTk (customtkinter main window)
- **Fields:**
  - API Key (password entry, masked)
  - Microphone dropdown (system audio devices)
  - Hotkey display (read-only, configurable future)
  - Beep sound toggle (on/off)
  - Overlay visibility toggle (on/off)
- **Actions:**
  - Save: Apply changes to .env/config
  - Cancel/Close: Discard unsaved changes

---

### TRAY-001: System Tray Interface
**Purpose:** Background application management

**Contract:**
- **Library:** pystray with Pillow for icon
- **Menu Items:**
  - "Restore" / "Show Settings": Open settings window
  - "Quit": Exit application completely
- **Behavior:**
  - Minimize to tray (don't close)
  - Tray icon visible when settings window hidden
  - Hotkey listener remains active in background

---

- [2026-01-12] Initial interface contracts definition
  - Change type: New contracts
  - Previous behavior: Undefined
  - New behavior: Defined 7 interface contracts (HOT-001, REC-001, TRX-001, INJ-001, UI-001, CFG-001, TRAY-001)
  - Compatibility notes: N/A (initial definition)

- [2026-01-12] TRX-001: Turkish Language Support
  - Change type: Response shape / API parameter
  - Previous behavior: Language not specified, default Whisper auto-detection
  - New behavior: Explicit `language="tr"` parameter passed to Groq API for improved Turkish transcription accuracy
  - Compatibility notes: Backward-compatible (parameter defaults to "tr")
