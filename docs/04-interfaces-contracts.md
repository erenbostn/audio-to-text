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

### HIST-001: Recording History Interface
**Purpose:** In-memory recording management and batch transcription

**Contract:**
- **Storage:** In-memory dictionary (id → Recording)
- **Lifecycle:** Recordings persist during app session, cleared on shutdown
- **Recording Object:**
  - id: Timestamp-based unique identifier
  - filepath: Path to temp .wav file
  - created_at: Datetime of recording
  - transcribed: Boolean flag
  - transcript: Transcribed text (None if not transcribed)
- **Methods:**
  - add_recording(filepath): Returns recording ID
  - get_recordings(): List of recordings (newest first)
  - update_transcript(id, text): Updates transcription result
  - delete_recording(id): Removes from history
  - clear_all(): Clears all recordings

**UI Requirements:**
- History list at TOP of settings window
- Checkbox per recording for selection
- Shows: filename, timestamp, file size, status (Ready/Done)
- Transcript preview below transcribed items (truncated)
- "Transcribe Selected" button for batch transcription
- "Delete Selected" button to remove items

---

### FILE-001: File Upload Interface
**Purpose:** Transcribe external audio files not created by recorder

**Contract:**
- **File Dialog:** tkinter.filedialog.askopenfilename
- **Supported Formats:** WAV, MP3, OGG, FLAC, All files
- **UI Components:**
  - File entry showing selected path
  - Browse button to open file dialog
  - Transcribe File button to process
- **Behavior:**
  - User selects file via dialog
  - Path stored in `_selected_file` variable
  - Transcribe button calls transcriber.transcribe(file_path)
  - Result injected via TextInjector

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

- [2026-01-12] HOT-001: Hotkey Combination Changed
  - Change type: Configuration value
  - Previous behavior: Ctrl+Alt+Space
  - New behavior: Ctrl+Alt+K (user preference)
  - Compatibility notes: Breaking change for users who memorized previous hotkey

- [2026-01-12] HIST-001: Recording History Interface (NEW)
  - Change type: New feature
  - Previous behavior: No history, auto-transcription on recording stop
  - New behavior: In-memory history, manual selection, batch transcription
  - Compatibility notes: User-visible workflow change

- [2026-01-12] FILE-001: File Upload Interface (NEW)
  - Change type: New feature
  - Previous behavior: Only record-through-microphone supported
  - New behavior: External audio files can be transcribed via file dialog
  - Compatibility notes: Backward-compatible (recording still works)
