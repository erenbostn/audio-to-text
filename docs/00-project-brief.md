---

## CURRENT STATE (AI-maintained)

> This section is automatically updated by AI after completed tasks.
> Append-only. Do not rewrite, summarize, or delete previous entries.

- [2026-01-12] Initial Documentation Sync
  - What changed: Synchronized documentation from project specifications (tech_spec.md, project_structure.md, html.md) to docs/ folder
  - Affected area: docs/01-requirements.md, docs/03-architecture.md, docs/04-interfaces-contracts.md, docs/05-backlog.md
  - Notes:
    - Defined 8 functional requirements (FR-001 to FR-008) and 6 non-functional requirements (NFR-001 to NFR-006)
    - Defined 7 interface contracts (HOT-001, REC-001, TRX-001, INJ-001, UI-001, CFG-001, TRAY-001)
    - Added 8 architecture decision log entries covering framework selection, threading model, UI approach, etc.
    - Created 12-task backlog spanning 9 phases (Project Setup → Core → UI → Main → Utilities → Docs/Tests)
    - All documentation follows ai.md protocol (append-only, docs as canonical source)

- [2026-01-12] UI Implementation Phase 1 Complete
  - What changed: Implemented core UI components (overlay, settings window) with customtkinter
  - Affected area: src/ui/overlay.py, src/ui/settings_window.py, src/config.py, src/main.py (placeholder)
  - Notes:
    - TASK-001 (Project Setup): Complete - directory structure, requirements.txt, .env.example created
    - TASK-005 (Overlay): Complete - frameless CTkToplevel with Canvas waveform animation, pulse effect, show/hide methods
    - TASK-006 (Settings Window): Complete - glass effect styling, API key form, mic dropdown, toggles, .env save/load
    - CSS → CTk mapping: html.md CSS values translated to customtkinter properties
    - Design note: Settings window styling to be refined later (user deferred)

- [2026-01-12] Backend Core Modules Complete
  - What changed: Implemented three core backend modules (recorder, transcriber, input_simulator)
  - Affected area: src/core/recorder.py, src/core/transcriber.py, src/core/input_simulator.py
  - Notes:
    - TASK-002 (Audio Recorder): Complete - sounddevice + numpy, non-blocking threading, project_root/temp/ for files
    - TASK-003 (Groq Transcriber): Complete - whisper-large-v3 model, Turkish language support, retry logic
    - TASK-004 (Text Injection): Complete - clipboard-based (pyperclip) for full Unicode including Turkish characters
    - Added pyperclip>=1.8.0 to requirements.txt
    - Created .gitignore for .env, venv/, temp/, *.wav protection
    - Turkish transcription accuracy fix: Added `language="tr"` parameter to Groq API call

- [2026-01-12] Main Application Bootstrap Complete (TASK-007, TASK-008, TASK-010)
  - What changed: Implemented system tray, sound feedback, and main application orchestrator
  - Affected area: src/ui/tray.py, src/utils/sound_feedback.py, src/main.py
  - Notes:
    - TASK-007 (System Tray): Complete - pystray integration with menu (Restore, Quit), programmatically generated mic icon
    - TASK-008 (Main Entry Point): Complete - GroqWhisperApp class with hotkey → recorder → transcriber → injector workflow
    - TASK-010 (Sound Feedback): Complete - winsound-based beep sounds (1000Hz start, 700Hz stop)
    - Global hotkey (Ctrl+Alt+Space) toggles recording
    - API key validation on startup, opens settings if missing
    - Clean shutdown with temp file cleanup
    - All dependencies installed via requirements.txt

- [2026-01-12] UI Bug Fixes & Workflow Changes
  - What changed: Fixed empty window bug, updated hotkey, changed recording workflow
  - Affected area: src/main.py, src/ui/settings_window.py
  - Notes:
    - Fixed: SettingsWindow now IS the main window (was creating two windows before)
    - Hotkey changed: Ctrl+Alt+Space → Ctrl+Alt+K (user preference)
    - Window close now minimizes to tray instead of destroying
    - Settings window opens on startup (UI-first approach)

- [2026-01-12] Recording History & File Upload Features
  - What changed: Added in-memory recording history with batch transcription, file upload support
  - Affected area: src/models/recording.py (NEW), src/core/history_manager.py (NEW), src/ui/settings_window.py, src/main.py, src/config.py
  - Notes:
    - Recording History: Shows list of recordings with checkboxes, transcript preview, file details
    - No auto-transcription: Recordings added to history for user to select manually
    - File Upload: Browse button to transcribe external audio files
    - Beep Bug Fix: Config now updates os.environ directly after save (toggle takes effect immediately)
    - Window size: 450x480 → 450x750 (scrollable main body)
    - Scrollable body: CTkScrollableFrame for content overflow
    - History UI at TOP (first thing user sees)

- [2026-01-12] Save Configuration Button Bug Fix
  - What changed: Fixed Save Configuration button not responding to clicks
  - Affected area: src/ui/settings_window.py
  - Notes:
    - Added missing `command=self._save_config` parameter to save button
    - Button now correctly saves API key, beep setting, and overlay setting to .env file

- [2026-01-12] Project Cleanup
  - What changed: Removed empty tests/ directory
  - Affected area: tests/ directory (deleted)
  - Notes:
    - tests/ contained only __init__.py, no actual tests
    - TASK-012 (Unit Tests) remains in backlog for future implementation
    - All source code verified as actively used
    - All dependencies verified as necessary

- [2026-01-12] File Size Check for Transcription
  - What changed: Added file size validation before Groq API transcription
  - Affected area: src/core/transcriber.py
  - Notes:
    - Added _check_file_size() method to validate audio file size
    - Shows file size info in MB before transcription
    - Warns when file exceeds 20 MB (approaching 25 MB Groq API limit)
    - Blocks transcription when file exceeds 25 MB
    - Helps users understand why long recordings may fail partially

- [2026-01-12] Multi-Language Support
  - What changed: Added language selector dropdown for transcription
  - Affected area: src/config.py, src/core/transcriber.py, src/ui/settings_window.py, .env.example
  - Notes:
    - Added TRANSCRIPTION_LANGUAGE config option (default: tr)
    - Language dropdown in settings: Turkish, English, German, French, Spanish, Italian, Auto-detect
    - Auto-detect option passes None to Whisper API for automatic language detection
    - Language selection persists in .env file
    - Transcriptions now use selected language instead of hardcoded Turkish

---

## KNOWN ISSUES / UNKNOWNS (AI-maintained)

> Open questions, assumptions, or risks discovered during implementation.
> Append-only. Items are removed only when explicitly resolved.

- [2026-01-12] [FIXED] Beep sound toggle not working after save - Fixed by updating os.environ directly
- [2026-01-12] [FIXED] CTkCheckBox unsupported arguments - Changed to hover_color, checkmark_color
- [YYYY-MM-DD] [UNKNOWN] Description of the uncertainty or risk
