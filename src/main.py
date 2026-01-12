"""
GroqWhisper Desktop - Main Entry Point
Integrates all components into a functional desktop application.
"""

import customtkinter as ctk
from pynput.keyboard import GlobalHotKeys
import sys
import signal
import atexit
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from core.recorder import AudioRecorder
from core.transcriber import GroqTranscriber
from core.input_simulator import TextInjector
from ui.overlay import RecordingOverlay
from ui.settings_window import SettingsWindow
from ui.tray import SystemTray
from utils.sound_feedback import SoundFeedback


class GroqWhisperApp:
    """
    Main application orchestrator for GroqWhisper Desktop.

    Manages:
    - Global hotkey listener for recording toggle
    - Audio recording workflow
    - Transcription via Groq API
    - Text injection to active window
    - System tray integration
    - Settings window
    """

    # Class variable to track running state
    _running = False

    def __init__(self):
        """Initialize the application."""
        # Initialize customtkinter
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        # Load configuration
        self.config = Config()

        # Recording state
        self._is_recording = False
        self._settings_window = None
        self._shutdown_flag = False

        # Setup core components (before UI)
        self._setup_components()

        # Create SettingsWindow FIRST - it becomes the main root window
        self._settings_window = SettingsWindow(self.config, on_close=self._on_settings_close, app=self)
        self.root = self._settings_window  # Reference to main window

        # Setup remaining components (overlay needs the root)
        self._setup_remaining_components()
        self._setup_hotkeys()

    def _setup_components(self) -> None:
        """Initialize core application components (before UI)."""
        # Core modules
        self.recorder = AudioRecorder(
            sample_rate=self.config.get_sample_rate(),
            channels=self.config.get_channels()
        )
        self.transcriber = GroqTranscriber()
        self.injector = TextInjector()

        # Utilities
        self.sound = SoundFeedback(self.config.play_beep)
        self.tray = SystemTray(
            on_restore=self._show_settings,
            on_quit=self.shutdown
        )

    def _setup_remaining_components(self) -> None:
        """Initialize UI components that need the root window."""
        # UI components (overlay needs the root)
        self.overlay = RecordingOverlay(self.root)

    def _setup_hotkeys(self) -> None:
        """Setup global hotkey listener."""
        # User requested: Ctrl+Alt+K for recording
        recording_hotkey = '<ctrl>+<alt>+k'

        try:
            # pynput format: modifiers need to be in angle brackets, key doesn't
            hotkeys = {
                recording_hotkey: self._on_hotkey_pressed,
                '<ctrl>+<alt>+q': self._quit_wrapper,  # Quit hotkey
            }
            self.hotkey_listener = GlobalHotKeys(hotkeys)
            self.hotkey_listener.start()
            print(f"Hotkeys registered:")
            print(f"  {recording_hotkey} - Toggle recording")
            print(f"  <ctrl>+<alt>+q - Quit application")
        except Exception as e:
            print(f"Warning: Could not register hotkeys: {e}")
            print("The application will start but hotkey functionality may not work.")
            self.hotkey_listener = None

    def _quit_wrapper(self) -> None:
        """Wrapper for shutdown from hotkey."""
        print("Quit hotkey pressed...")
        self.root.after(0, self.shutdown)

    def _validate_api_key(self) -> None:
        """Validate API key on startup, show settings if missing."""
        api_key = self.config.get_api_key()
        if not api_key:
            print("No API key found. Opening settings...")
            self.root.after(100, self._show_settings)

    def _on_hotkey_pressed(self) -> None:
        """Handle global hotkey press (toggle recording)."""
        if not self._is_recording:
            self._start_recording()
        else:
            self._stop_recording()

    def _start_recording(self) -> None:
        """Start audio recording."""
        self._is_recording = True
        self.sound.play_start_beep()

        if self.config.show_overlay():
            self.overlay.show()

        self.recorder.start_recording()
        self.tray.update_tooltip("Recording...")

        # Update settings button if visible
        if self._settings_window:
            self.root.after(0, self._settings_window._update_recording_button)

    def _stop_recording(self) -> None:
        """Stop recording and transcribe."""
        # Stop recording and get audio file
        audio_file = self.recorder.stop_recording()

        if not audio_file:
            print("No audio file recorded.")
            self._reset_state()
            return

        self._is_recording = False
        self.overlay.hide()
        self.tray.update_tooltip("Processing...")

        # Update settings button if visible
        if self._settings_window:
            self.root.after(0, self._settings_window._update_recording_button)

        # Transcribe
        try:
            text = self.transcriber.transcribe(audio_file, language="tr")
            if text:
                self.sound.play_stop_beep()
                self.injector.inject_text(text)
            else:
                print("Transcription returned empty result.")
        except Exception as e:
            print(f"Error during transcription: {e}")
        finally:
            self.tray.update_tooltip("Ready")

    def _reset_state(self) -> None:
        """Reset recording state after error."""
        self._is_recording = False
        self.overlay.hide()
        self.tray.update_tooltip("Ready")

    def _show_settings(self) -> None:
        """Show the settings window."""
        print("Opening settings...")
        try:
            # Use root.after() for thread-safe GUI update
            self.root.after(0, self._show_settings_impl)
        except Exception as e:
            print(f"Error opening settings: {e}")

    def _show_settings_impl(self) -> None:
        """Implementation of showing settings (runs on main thread)."""
        try:
            # SettingsWindow IS the main window - just show it
            if self._settings_window and self._settings_window.winfo_exists():
                print("Bringing settings window to front...")
                self._settings_window.lift()
                self._settings_window.focus_set()
                self._settings_window.deiconify()
            else:
                print("Settings window not found - this shouldn't happen")
        except Exception as e:
            print(f"Error in settings impl: {e}")

    def _on_settings_close(self) -> None:
        """Handle settings window close - minimize to tray."""
        # The window is already withdrawn/hidden by SettingsWindow._on_window_close
        print("Settings window minimized to tray.")

    def run(self) -> None:
        """Start the application main loop."""
        print("GroqWhisper Desktop - Starting...")
        print("Settings window will open on startup.")
        print("=" * 50)

        # Setup signal handlers for graceful shutdown
        def signal_handler(sig, frame):
            print("\nShutdown signal received...")
            self.shutdown()

        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Start tray icon
        self.tray.run()

        # Run tkinter mainloop
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received...")
            self.shutdown()

    def shutdown(self) -> None:
        """Clean shutdown of all components."""
        if self._shutdown_flag:
            return  # Already shutting down

        self._shutdown_flag = True
        print("\nGroqWhisper Desktop - Shutting down...")

        try:
            # Stop hotkey listener first
            if hasattr(self, 'hotkey_listener') and self.hotkey_listener:
                try:
                    self.hotkey_listener.stop()
                except:
                    pass

            # Stop tray icon
            if hasattr(self, 'tray'):
                try:
                    self.tray.stop()
                except:
                    pass

            # Cleanup temp files
            if hasattr(self, 'recorder'):
                try:
                    self.recorder.cleanup_temp_files()
                except:
                    pass

            # Quit tkinter mainloop
            try:
                self.root.quit()
            except:
                pass

        except Exception as e:
            print(f"Error during shutdown: {e}")
        finally:
            # Force exit if still running
            import os
            os._exit(0)

    def _cleanup(self) -> None:
        """Cleanup callback for atexit."""
        try:
            self.recorder.cleanup_temp_files()
        except:
            pass


def main():
    """Main application entry point."""
    app = GroqWhisperApp()
    app.run()


if __name__ == "__main__":
    main()
