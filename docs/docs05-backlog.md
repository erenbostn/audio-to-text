## Backlog Item Template

**ID:** TASK-XXX  
**Type:** Feature | Bug | Chore  
**Priority:** P0 | P1 | P2  
**Status:** Todo | In Progress | Done

### Description

Clear and concise description of the task or problem.

### Acceptance Criteria

- [ ] Behavior implemented as described
- [ ] Verification completed (build / lint / test / manual)
- [ ] Docs updated per `.ai/AI.md` doc update matrix
- [ ] No unrelated refactors or scope creep

### Backlog Status Rules

- A task is marked **Done** only after:
  - Acceptance criteria are fully satisfied
  - Verification has been executed
  - Required documentation updates are completed
- If verification is not possible, a follow-up item must be added.

---

## Project Backlog

### Phase 1: Project Setup

**TASK-001 | Initial Project Structure | Priority: P0 | Status: Done**

Setup the directory structure and Python environment as defined in `project_structure.md`.

**Acceptance Criteria:**
- [x] Create `src/` directory with subdirectories: `core/`, `ui/`, `utils/`
- [x] Create `tests/` directory
- [x] Create `.env.example` file with GROQ_API_KEY template
- [x] Create `requirements.txt` with all dependencies:
  - customtkinter
  - sounddevice
  - numpy
  - pystray
  - Pillow
  - pynput
  - groq
  - python-dotenv
  - pyautogui (or keyboard)
- [x] Create empty `__init__.py` files in each package directory
- [x] Verify venv is activated and dependencies are installable

---

### Phase 2: Core - Audio Recording

**TASK-002 | Audio Recorder Module | Priority: P0 | Status: Done**

Implement `src/core/recorder.py` for audio capture and .wav file generation.

**Acceptance Criteria:**
- [x] Recorder class with `start_recording()` and `stop_recording()` methods
- [x] Uses sounddevice and numpy for audio capture
- [x] Saves to temporary .wav file with unique identifier
- [x] Runs in separate non-blocking thread
- [x] Handles recording interruption gracefully
- [x] Returns file path on stop
- [x] Temp files saved to project_root/temp/ directory
- [x] cleanup_temp_files() method for disk management

---

### Phase 3: Core - Transcription

**TASK-003 | Groq Transcriber Module | Priority: P0 | Status: Done**

Implement `src/core/transcriber.py` for speech-to-text conversion via Groq API.

**Acceptance Criteria:**
- [x] Transcriber class with `transcribe(audio_file_path)` method
- [x] Loads GROQ_API_KEY from .env via config.py
- [x] Sends audio file to Groq API
- [x] Returns transcribed text as string
- [x] Handles API errors (invalid key, network failure)
- [x] Returns None or raises exception on failure
- [x] Turkish language support via `language="tr"` parameter

---

### Phase 4: Core - Input Simulation

**TASK-004 | Text Injection Module | Priority: P1 | Status: Done**

Implement `src/core/input_simulator.py` for keyboard text injection.

**Acceptance Criteria:**
- [x] Injector class with `inject_text(text)` method
- [x] Uses pyautogui or keyboard library
- [x] Supports Unicode characters (ş, ı, ğ, ö, ç, ü)
- [x] Types at natural speed (configurable delay)
- [x] Respects current cursor position
- [x] Clipboard-based injection (pyperclip) for full Unicode support
- [x] Clipboard backup/restore to preserve user's clipboard

---

### Phase 5: UI - Overlay

**TASK-005 | Floating Status Overlay | Priority: P0 | Status: Done**

Implement `src/ui/overlay.py` - frameless recording status widget per html.md design.

**Acceptance Criteria:**
- [x] CTkToplevel with overrideredirect(True) and attributes('-topmost', True)
- [x] Shows/hides based on recording state
- [x] Contains:
  - Microphone icon with pulse animation
  - "Recording..." status text
  - Animated waveform bars (5 bars)
- [x] Dark theme with glass/acrylic styling
- [x] Accent color #FF6B35 for active elements
- [x] Optionally draggable

---

### Phase 6: UI - Settings Window

**TASK-006 | Settings Configuration Window | Priority: P1 | Status: Done**

Implement `src/ui/settings_window.py` per html.md design and CFG-001 contract.

**Acceptance Criteria:**
- [x] CTk main window with dark theme
- [x] Form fields:
  - API Key (password entry, masked)
  - Microphone dropdown (populated from system devices)
  - Hotkey display (read-only text: "Ctrl + Alt + Space")
  - Beep sound toggle (CTkSwitch)
  - Overlay visibility toggle (CTkSwitch)
- [x] Save button that writes to .env
- [x] Glass window styling per html.md (CSS values mapped to CTk)

---

### Phase 7: UI - System Tray

**TASK-007 | System Tray Integration | Priority: P1 | Status: Done**

Implement `src/ui/tray.py` for background application management per TRAY-001 contract.

**Acceptance Criteria:**
- [x] Uses pystray with Pillow for icon generation
- [x] Tray icon menu items:
  - "Restore" / "Show Settings"
  - "Quit"
- [x] "Restore" opens settings window
- [x] "Quit" cleanly exits application
- [x] Minimizes to tray (don't close on X)
- [x] Hotkey listener remains active when in tray

---

### Phase 8: Main Entry Point

**TASK-008 | Main Application Bootstrap | Priority: P0 | Status: Done**

Implement `src/main.py` and `src/config.py` for application initialization.

**config.py Acceptance Criteria:**
- [x] Loads GROQ_API_KEY from .env using python-dotenv
- [x] Provides `get_api_key()` function
- [x] Provides `save_api_key(key)` function
- [x] Handles missing .env gracefully

**main.py Acceptance Criteria:**
- [x] Initializes customtkinter (dark mode, dark-blue theme)
- [x] Loads configuration via config.py
- [x] Creates system tray icon
- [x] Starts global hotkey listener (daemon thread)
- [x] Creates overlay window (hidden initially)
- [x] Connects hotkey → recorder → transcriber → injector flow
- [x] Handles application shutdown (tray quit)

---

### Phase 9: Utilities

**TASK-009 | Audio Utilities | Priority: P2 | Status: Todo**

Implement `src/utils/audio_utils.py` for temporary file management.

**Acceptance Criteria:**
- [ ] `generate_temp_filename()` function
- [ ] `cleanup_temp_files()` function
- [ ] Uses tempfile module or custom temp directory
- [ ] Handles file cleanup on application exit

---

**TASK-010 | Sound Feedback Utilities | Priority: P2 | Status: Done**

Implement `src/utils/sound_feedback.py` for beep sounds per NFR-008.

**Acceptance Criteria:**
- [x] `play_start_beep()` function (1000Hz, 200ms)
- [x] `play_stop_beep()` function (700Hz, 200ms)
- [x] Uses winsound (Windows-specific)
- [x] Respects user preference setting (enable/disable)

---

### Documentation & Testing

**TASK-011 | README.md | Priority: P2 | Status: Todo**

Create user-facing documentation.

**Acceptance Criteria:**
- [ ] Project overview
- [ ] Installation instructions
- [ ] Configuration guide (.env setup)
- [ ] Usage instructions (hotkey, settings)
- [ ] Requirements summary

---

**TASK-012 | Unit Tests | Priority: P3 | Status: Todo**

Implement tests in `tests/` directory.

**Acceptance Criteria:**
- [ ] Test config loading
- [ ] Test recorder start/stop
- [ ] Test transcriber error handling
- [ ] Test input simulator (mock)
- [ ] Test overlay show/hide logic

---

### Phase 10: Advanced Features (Post-MVP)

**TASK-013 | Recording History Feature | Priority: P1 | Status: Done**

Implement in-memory recording history with batch transcription.

**Acceptance Criteria:**
- [x] Create `src/models/recording.py` - Recording dataclass with properties
- [x] Create `src/core/history_manager.py` - HistoryManager class for in-memory storage
- [x] History UI in settings window (at TOP - first thing user sees):
  - [x] Scrollable list with checkboxes for each recording
  - [x] Shows filename, timestamp, file size, status (Ready/Done)
  - [x] Transcript preview below transcribed items (truncated if long)
  - [x] "Transcribe Selected" and "Delete Selected" buttons
- [x] No auto-transcription: Recordings added to history for manual selection
- [x] Window resize: 450x480 → 450x750 for new content
- [x] Scrollable main body: CTkScrollableFrame for content overflow

---

**TASK-014 | File Upload Feature | Priority: P1 | Status: Done**

Implement file upload for transcribing external audio files.

**Acceptance Criteria:**
- [x] "Transcribe from File" section in settings window
- [x] Browse button opens file dialog (WAV, MP3, OGG, FLAC)
- [x] File entry shows selected path
- [x] Transcribe File button processes selected file
- [x] Integration with existing transcriber and injector

---

**TASK-015 | Beep Sound Toggle Bug Fix | Priority: P0 | Status: Done**

Fix beep sound toggle not taking effect after save.

**Acceptance Criteria:**
- [x] Config.reload_env() method to reload .env
- [x] Config.save_beep_setting() updates both .env and os.environ
- [x] Config.save_overlay_setting() updates both .env and os.environ
- [x] Settings window uses new config methods
- [x] Toggle takes effect immediately after save

---

**TASK-016 | UI Bug Fixes | Priority: P0 | Status: Done**

Fix empty window bug and improve window behavior.

**Acceptance Criteria:**
- [x] Fix: SettingsWindow IS the main window (was creating two windows)
- [x] Window close minimizes to tray instead of destroying
- [x] Settings window opens on startup (UI-first)
- [x] Hotkey display updated: Ctrl+Alt+Space → Ctrl+Alt+K
- [x] CTkCheckBox fixed: hover_color, checkmark_color (was using unsupported arguments)

---

- [2026-01-12] Initial backlog creation
  - Added 12 tasks covering all project phases
  - All tasks derived from project_structure.md
  - Status: All tasks set to "Todo"

- [2026-01-12] Phase 10 tasks added (Advanced Features)
  - TASK-013: Recording History - In-memory storage, batch transcription, UI at top
  - TASK-014: File Upload - External audio file transcription
  - TASK-015: Beep Bug Fix - os.environ update for immediate effect
  - TASK-016: UI Bug Fixes - Empty window, close behavior, hotkey display
  - All Phase 10 tasks: Status = Done
