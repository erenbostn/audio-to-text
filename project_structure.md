# Project Structure Specification

We are building a Python-based desktop application called "GroqWhisper Desktop" for Windows.
The application listens for a global hotkey to toggle recording, shows a modern `customtkinter` overlay, plays a system beep, transcribes audio using Groq API, and simulates keystrokes.

## Directory Tree
Please initialize the project with the following structure:

groq-whisper-desktop/
├── src/
│   ├── main.py              # Entry point (initializes Tray, Listener, Overlay)
│   ├── config.py            # Configuration loader (.env variables)
│   ├── core/
│   │   ├── recorder.py      # Audio recording logic
│   │   ├── transcriber.py   # Groq API interaction logic
│   │   └── input_simulator.py # Keyboard simulation
│   ├── ui/
│   │   ├── overlay.py       # Floating status widget (CustomTkinter CkToplevel)
│   │   ├── settings_window.py # Config UI (CustomTkinter Ctk)
│   │   └── tray.py          # System tray icon (pystray)
│   └── utils/
│       ├── audio_utils.py   # Temporary file management
│       └── sound_feedback.py # Windows system beep logic
├── docs/                    # Documentation specs
├── tests/                   # Unit tests
├── .env.example             # API Key template
├── requirements.txt         # Dependencies (must include customtkinter)
└── README.md