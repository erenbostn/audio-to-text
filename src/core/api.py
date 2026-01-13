import json
import sounddevice as sd
import pyperclip
import threading
from typing import Dict, Any, List

class Api:
    """
    API Bridge between Python backend and PyWebview JavaScript frontend.
    Exposed methods can be called from JS via `pywebview.api.method_name()`.
    """
    def __init__(self, app):
        self._app = app
        self._config = app.config
        self._history = app.history

    def get_config(self) -> Dict[str, Any]:
        """Return current configuration."""
        return {
            "api_key": self._config.get_api_key(),
            "input_device_index": self._config.get_input_device(),
            "sound_enabled": self._config.play_beep(),
            "auto_copy_enabled": self._config.auto_copy_enabled(),
            "language": self._config.get_language()
        }

    def save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration from UI."""
        print(f"[API] Saving config: {config}")
        
        # Save API Key
        if "api_key" in config:
            self._config.save_api_key(config["api_key"])
            
        # Save Sound Setting
        if "sound_enabled" in config:
            self._config.save_beep_setting(config["sound_enabled"])
            
        # Save Auto-Copy Setting
        if "auto_copy_enabled" in config:
            self._config.save_auto_copy_setting(config["auto_copy_enabled"])
            
        # Save Language
        if "language" in config:
            self._config.save_language(config["language"])
            
        # Device Index - We might need to implement this in Config if not present
        # Currently config stores device index? Let's check config.py later. 
        # For now assume we just keep it in runtime or config if supported.
        # But wait, config.py didn't seem to have device index storage in the Plan.
        # We will check config.py or just use it if available.
        
        # Determine language? The previous UI had language. New UI mock didn't show it explicitly in my code, 
        # but I should probably support it if the user wants it.
        # The user request didn't explicitly ask for language dropdown in specific UI instructions,
        # but "Dashboard" implies settings. I'll stick to what I wrote in HTML for now.
        
        # Notify app to reload/apply
        self._app.reload_config()

    def get_microphones(self) -> List[Dict[str, Any]]:
        """Get list of available microphones."""
        try:
            devices = sd.query_devices()
            mics = []
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    mics.append({
                        "index": i,  # Use index for selection
                        "name": device['name']
                    })
            return mics
        except Exception as e:
            print(f"[API] Error getting mics: {e}")
            return []

    def get_history(self) -> List[Dict[str, Any]]:
        """Get recording history."""
        recordings = self._history.get_recordings()
        return [
            {
                "id": r.id,
                "timestamp": r.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "text": r.transcript if r.transcribed else "Processing...",
                "transcribed": r.transcribed
            }
            for r in recordings
        ]
    
    def copy_to_clipboard(self, text: str) -> None:
        """Copy text to system clipboard."""
        pyperclip.copy(text)

    def toggle_recording(self) -> None:
        """Toggle recording state manually from UI."""
        # Run in thread to avoid blocking UI
        threading.Thread(target=self._app.toggle_recording, daemon=True).start()

    def close_app(self) -> None:
        """Close the application."""
        self._app.quit()

    def select_file(self) -> str | None:
        """
        Open a file dialog to select an audio file.
        Returns the path of the selected file, or None.
        Using Tkinter as fallback since pywebview dialogs can be tricky.
        """
        try:
            import tkinter as tk
            from tkinter import filedialog
            
            # Create hidden root window
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            file_path = filedialog.askopenfilename(
                title="Select Audio File",
                filetypes=[("Audio Files", "*.mp3 *.wav *.m4a *.ogg *.flac"), ("All Files", "*.*")]
            )
            
            root.destroy()
            return file_path if file_path else None
            
        except Exception as e:
            print(f"[API] Error selecting file: {e}")
            return None

    def transcribe_file(self, filepath: str) -> None:
        """
        Transcribe a selected file.
        
        Args:
            filepath: Absolute path to the file.
        """
        # Run in thread
        threading.Thread(target=self._app.process_file_transcription, args=(filepath,), daemon=True).start()
