# Requirements

This document defines functional and non-functional requirements for GroqWhisper Desktop.

## Functional Requirements (FR)

### FR-001: Global Hotkey Recording Toggle
The application MUST provide a global hotkey (default: `Ctrl+Alt+Space`) that toggles audio recording on/off. The hotkey listener MUST run in a background daemon thread and remain active even when the application window is minimized.

### FR-002: Audio Recording
When recording is active, the application MUST:
- Capture audio from the selected microphone device
- Save the recording as a temporary `.wav` file
- Run recording in a separate non-blocking thread to maintain UI responsiveness

### FR-003: Transcription via Groq API
The application MUST:
- Send the recorded audio file to the Groq API for transcription
- Handle API authentication using `GROQ_API_KEY` from environment configuration
- Return the transcribed text to the user

### FR-004: Text Injection
After successful transcription, the application MUST:
- Simulate keyboard input to inject the transcribed text at the current cursor position
- Support Unicode characters (including Turkish characters: ş, ı, ğ, ö, ç, ü)

### FR-005: Floating Status Overlay
The application MUST display a floating overlay widget when recording is active that:
- Shows a visual "Recording..." indicator with microphone icon
- Displays animated waveform visualization
- Remains always-on-top and frameless
- Can be dismissed/minimized to system tray

### FR-006: Settings Window
The application MUST provide a settings window for configuring:
- Groq API Key entry (password field)
- Input device/microphone selection dropdown
- Activation hotkey configuration
- Toggle for beep sound feedback
- Toggle for floating overlay visibility
- Save/Apply configuration button

### FR-007: System Tray Integration
The application MUST:
- Minimize to system tray instead of closing
- Provide tray icon with context menu (Restore/Quit)
- Allow complete application exit via tray menu

### FR-008: Audio Feedback
When recording state changes, the application MUST:
- Play a beep sound when recording starts (1000Hz, 200ms)
- Play a beep sound when recording stops (700Hz, 200ms)
- Respect the user preference setting for enabling/disabling sounds

## Non-Functional Requirements (NFR)

### NFR-001: Platform Compatibility
- **Target OS:** Windows Only
- **Python Version:** 3.10 or higher (currently using 3.13.2)

### NFR-002: UI Responsiveness
- Audio recording MUST run in a separate thread
- UI overlay MUST remain responsive during recording
- Global hotkey listener MUST be non-blocking

### NFR-003: Unicode Support
- Text injection MUST support full Unicode character set
- MUST properly handle Turkish locale characters

### NFR-004: Visual Design
- MUST use customtkinter framework for modern UI
- MUST use dark theme (`set_appearance_mode("Dark")`)
- MUST use dark-blue color theme (`set_default_color_theme("dark-blue")`)
- MUST follow glass/acrylic visual style as defined in html.md concept

### NFR-005: Configuration Management
- API Key MUST be stored in `.env` file (not hardcoded)
- Configuration MUST load at application startup via `python-dotenv`

### NFR-006: Code Organization
- MUST follow the project structure defined in `project_structure.md`
- Core logic MUST be separated from UI components
- MUST maintain separation of concerns (recorder, transcriber, input_simulator)

---

## CHANGE LOG (AI-maintained)

> Records all requirement changes. Append-only.

- [2026-01-12] Initial requirements definition
  - Derived from: tech_spec.md, project_structure.md, html.md
  - Defined 8 functional requirements (FR-001 to FR-008)
  - Defined 6 non-functional requirements (NFR-001 to NFR-006)
