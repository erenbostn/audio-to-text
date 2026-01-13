"""
GroqWhisper Desktop - Main Entry Point
Integrates all components into a functional desktop application using PyWebview.
"""

import webview
from pynput.keyboard import GlobalHotKeys
import sys
import signal
import os
import threading
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import Config
from core.recorder import AudioRecorder
from core.transcriber import GroqTranscriber
from core.input_simulator import TextInjector
from core.history_manager import HistoryManager
from core.api import Api
from ui.tray import SystemTray
from utils.sound_feedback import SoundFeedback


class GroqWhisperApp:
    """
    Main application orchestrator for GroqWhisper Desktop.
    Uses PyWebview for UI (Dashboard + Overlay).
    """

    def __init__(self):
        """Initialize the application."""
        self.config = Config()
        self._is_recording = False
        self._shutdown_flag = False
        
        # Windows
        self.dashboard_window = None
        self.overlay_window = None

        # Setup core components
        self._setup_components()
        
        # Setup API Bridge
        self.api = Api(self)
        
        # Setup UI
        self._setup_ui()
        
        # Setup Hotkeys
        self._setup_hotkeys()

    def _setup_components(self) -> None:
        """Initialize core application components."""
        self.recorder = AudioRecorder(
            sample_rate=self.config.get_sample_rate(),
            channels=self.config.get_channels()
        )
        self.transcriber = GroqTranscriber()
        self.injector = TextInjector()
        self.history = HistoryManager()
        self.sound = SoundFeedback(self.config.play_beep)
        
        # Reuse existing tray (might need adjustments if it relies on tkinter loop, 
        # but pystray usually has its own loop or runs in thread. 
        # We'll run it in a thread or let pystray handle it)
        # We need to be careful about not blocking the main thread which webview needs.
        # usually tray runs in separate thread.
        self.tray = SystemTray(
            on_restore=self.show_dashboard,
            on_quit=self.shutdown
        )

    def _setup_ui(self) -> None:
        """Initialize PyWebview windows."""
        
        # Path to index.html
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'ui', 'index.html'))
        html_url = f"file://{html_path}"
        
        # Dashboard Window
        self.dashboard_window = webview.create_window(
            'GroqWhisper Desktop', 
            url=html_url,
            width=500,
            height=850,
            resizable=True,
            js_api=self.api,
            on_top=False,
            confirm_close=True
        )
        # Hook into closing event to minimize instead of quit
        self.dashboard_window.events.closing += self._on_dashboard_closing

        # Overlay Window (Hidden initially, frameless, transparent, on top)
        # Note: Transparent windows might have platform specific issues.
        # We use a separate window for the overlay.
        overlay_url = f"{html_url}?view=overlay"
        self.overlay_window = webview.create_window(
            'GroqWhisper Overlay',
            url=overlay_url,
            width=300,
            height=100,
            frameless=True,
            on_top=True,
            transparent=True,
            easy_drag=True,
            js_api=self.api,
            x=0, y=0 # Initial position, maybe update later
        )
        
        # We hide overlay initially.
        # Pywebview doesn't have a direct 'hide()' in create options for all platforms, 
        # but we can try to hide it after load or position it off-screen.
        # Best bet: Minimize / Hide.
        # We'll use a timer to hide it once loaded or just rely on CSS 'hidden' if transparent allows simple click-through?
        # No, window presence blocks clicks. We need to hide the window itself.
        # We will hide it in the `run` method after a short delay or rely on API.
        
    def _on_dashboard_closing(self):
        """Handle dashboard close event (quit app)."""
        if self._shutdown_flag:
            return True
            
        # Shutdown application
        self.shutdown()
        return True

    def _setup_hotkeys(self) -> None:
        """Setup global hotkey listener."""
        recording_hotkey = '<ctrl>+<alt>+k' # Could be configurable
        try:
            hotkeys = {
                recording_hotkey: self.toggle_recording,
                '<ctrl>+<alt>+q': self.shutdown_wrapper,
            }
            self.hotkey_listener = GlobalHotKeys(hotkeys)
            self.hotkey_listener.start()
            print(f"Hotkeys registered: {recording_hotkey}")
        except Exception as e:
            print(f"Warning: Could not register hotkeys: {e}")

    def toggle_recording(self) -> None:
        """Toggle recording state."""
        if not self._is_recording:
            self._start_recording()
        else:
            self._stop_recording()

    def _start_recording(self) -> None:
        """Start audio recording."""
        print("Starting recording...")
        self._is_recording = True
        self.sound.play_start_beep()
        
        # Show overlay
        if self.config.show_overlay() and self.overlay_window:
            self.overlay_window.show()
            
        # Get configured input device
        device_index = self.config.get_input_device()
        if device_index == -1:
            device_index = None
            
        print(f"Recording using device index: {device_index}")
        
        # Start recording
        try:
            self.recorder.start_recording(device_index=device_index)
            self.tray.update_tooltip("Recording...")
            self._update_ui_recording_state(True)
        except Exception as e:
            print(f"Error starting recorder: {e}")
            self._is_recording = False
            self.tray.update_tooltip("Error")
            self._update_ui_recording_state(False)

    def _stop_recording(self) -> None:
        """Stop recording and process."""
        print("Stopping recording...")
        audio_file = self.recorder.stop_recording()
        self._is_recording = False
        
        # Hide overlay
        if self.overlay_window:
            self.overlay_window.hide()
            
        self.sound.play_stop_beep()
        
        if audio_file:
            # Add to history
            recording_id = self.history.add_recording(audio_file)
            
            # Update History UI
            self._update_history_ui()
            
            # Transcribe (Async)
            threading.Thread(target=self._process_transcription, args=(recording_id,), daemon=True).start()
        
        self.tray.update_tooltip("Ready")
        self._update_ui_recording_state(False)

    def _process_transcription(self, recording_id):
        """Handle transcription in background."""
        recording = self.history.get_recording(recording_id)
        if not recording:
            return
            
        lang = self.config.get_language()
        if lang == "auto":
            lang = None
            
        text = self.transcriber.transcribe(recording.filepath, language=lang)
        
        if text:
            self.history.update_transcript(recording_id, text)
            self.injector.inject_text(text)
            self._update_history_ui()
        else:
             print("Transcription failed.")

    def process_file_transcription(self, filepath):
        """Handle file transcription (called from API)."""
        print(f"Processing file: {filepath}")
        
        # Add to history as FILE source
        # Note: HistoryManager.add_recording default is SourceType.RECORDING.
        # We need to import SourceType or use string/bool if HM supports it.
        # Let's check history manager again or just pass filepath and update later.
        # Ideally we update add_recording to accept source. 
        # For now, let's just add it.
        
        # Check source type support in history manager
        from models.recording import SourceType
        recording_id = self.history.add_recording(filepath, source=SourceType.FILE)
        
        self._update_history_ui()
        
        # Transcribe
        lang = self.config.get_language()
        if lang == "auto":
            lang = None
            
        text = self.transcriber.transcribe(filepath, language=lang)
        
        if text:
            self.history.update_transcript(recording_id, text)
            self.injector.inject_text(text)
            self._update_history_ui()
        else:
            print("File transcription failed.")

    def _update_ui_recording_state(self, is_recording):
        """Notify JS about state."""
        code = f"toggleRecordingState({str(is_recording).lower()})"
        if self.dashboard_window:
            self.dashboard_window.evaluate_js(code)
        if self.overlay_window:
            self.overlay_window.evaluate_js(code)

    def _update_history_ui(self):
        """Push history update to UI."""
        history_data = self.api.get_history()
        # We need to serialize for JS
        import json
        json_str = json.dumps(history_data)
        code = f"updateHistory({json_str})"
        
        if self.dashboard_window:
            # evaluate_js calls are thread-safe in pywebview usually, but if called from thread, 
            # might need to ensure window is ready.
            try:
                self.dashboard_window.evaluate_js(code)
            except Exception as e:
                print(f"Error updating UI: {e}")

    def reload_config(self):
        """Reload configuration called from API."""
        self.config.reload_env()
        print("Config reloaded.")

    def show_dashboard(self):
        """Show dashboard window."""
        if self.dashboard_window:
            self.dashboard_window.show()
            self.dashboard_window.restore()

    def shutdown_wrapper(self):
        """Wrapper for hotkey shutdown."""
        # Use simple thread to not block hotkey listener
        threading.Thread(target=self.shutdown).start()

    def shutdown(self):
        """Clean shutdown."""
        if self._shutdown_flag:
            return
        self._shutdown_flag = True
        print("Shutting down...")
        
        if hasattr(self, 'hotkey_listener') and self.hotkey_listener:
            self.hotkey_listener.stop()
            
        if hasattr(self, 'tray'):
            self.tray.stop()
            
        if hasattr(self, 'recorder'):
            self.recorder.cleanup_temp_files()
            
        # Pywebview windows close automatically on sys.exit usually, or we can explicit destroy
        if self.dashboard_window:
            self.dashboard_window.destroy()
        if self.overlay_window:
            self.overlay_window.destroy()
            
        sys.exit(0)

    def run(self):
        """Run the application."""
        print("GroqWhisper Desktop - Starting Webview...")
        
        # Start Tray in background thread
        threading.Thread(target=self.tray.run, daemon=True).start()

        # Start Webview loop (Blocker)
        # Since we created windows already, just calling start() works.
        # We should hide overlay initially after a brief delay ensuring it's created.
        
        def initial_hide():
            time.sleep(0.5)
            if self.overlay_window:
                self.overlay_window.hide()
                
        webview.start(func=initial_hide, debug=False)

def main():
    app = GroqWhisperApp()
    app.run()

if __name__ == "__main__":
    main()
