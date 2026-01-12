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

**TASK-002 | Audio Recorder Module | Priority: P0 | Status: Todo**

Implement `src/core/recorder.py` for audio capture and .wav file generation.

**Acceptance Criteria:**
- [ ] Recorder class with `start_recording()` and `stop_recording()` methods
- [ ] Uses sounddevice and numpy for audio capture
- [ ] Saves to temporary .wav file with unique identifier
- [ ] Runs in separate non-blocking thread
- [ ] Handles recording interruption gracefully
- [ ] Returns file path on stop

---

### Phase 3: Core - Transcription

**TASK-003 | Groq Transcriber Module | Priority: P0 | Status: Todo**

Implement `src/core/transcriber.py` for speech-to-text conversion via Groq API.

**Acceptance Criteria:**
- [ ] Transcriber class with `transcribe(audio_file_path)` method
- [ ] Loads GROQ_API_KEY from .env via config.py
- [ ] Sends audio file to Groq API
- [ ] Returns transcribed text as string
- [ ] Handles API errors (invalid key, network failure)
- [ ] Returns None or raises exception on failure

---

### Phase 4: Core - Input Simulation

**TASK-004 | Text Injection Module | Priority: P1 | Status: Todo**

Implement `src/core/input_simulator.py` for keyboard text injection.

**Acceptance Criteria:**
- [ ] Injector class with `inject_text(text)` method
- [ ] Uses pyautogui or keyboard library
- [ ] Supports Unicode characters (ş, ı, ğ, ö, ç, ü)
- [ ] Types at natural speed (configurable delay)
- [ ] Respects current cursor position

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

**TASK-007 | System Tray Integration | Priority: P1 | Status: Todo**

Implement `src/ui/tray.py` for background application management per TRAY-001 contract.

**Acceptance Criteria:**
- [ ] Uses pystray with Pillow for icon generation
- [ ] Tray icon menu items:
  - "Restore" / "Show Settings"
  - "Quit"
- [ ] "Restore" opens settings window
- [ ] "Quit" cleanly exits application
- [ ] Minimizes to tray (don't close on X)
- [ ] Hotkey listener remains active when in tray

---

### Phase 8: Main Entry Point

**TASK-008 | Main Application Bootstrap | Priority: P0 | Status: Todo**

Implement `src/main.py` and `src/config.py` for application initialization.

**config.py Acceptance Criteria:**
- [ ] Loads GROQ_API_KEY from .env using python-dotenv
- [ ] Provides `get_api_key()` function
- [ ] Provides `save_api_key(key)` function
- [ ] Handles missing .env gracefully

**main.py Acceptance Criteria:**
- [ ] Initializes customtkinter (dark mode, dark-blue theme)
- [ ] Loads configuration via config.py
- [ ] Creates system tray icon
- [ ] Starts global hotkey listener (daemon thread)
- [ ] Creates overlay window (hidden initially)
- [ ] Connects hotkey → recorder → transcriber → injector flow
- [ ] Handles application shutdown (tray quit)

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

**TASK-010 | Sound Feedback Utilities | Priority: P2 | Status: Todo**

Implement `src/utils/sound_feedback.py` for beep sounds per NFR-008.

**Acceptance Criteria:**
- [ ] `play_start_beep()` function (1000Hz, 200ms)
- [ ] `play_stop_beep()` function (700Hz, 200ms)
- [ ] Uses winsound (Windows-specific)
- [ ] Respects user preference setting (enable/disable)

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

- [2026-01-12] Initial backlog creation
  - Added 12 tasks covering all project phases
  - All tasks derived from project_structure.md
  - Status: All tasks set to "Todo"
