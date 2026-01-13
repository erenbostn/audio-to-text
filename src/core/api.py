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
        # Reload .env to clear cache (handles .env file changes during runtime)
        self._config.reload_env()

        # Get key length without exposing the actual key
        api_key_length = self._config.get_api_key_length()

        return {
            "api_key_exists": api_key_length > 0,
            "api_key_length": api_key_length,
            "input_device_index": self._config.get_input_device(),
            "sound_enabled": self._config.play_beep(),
            "auto_paste_enabled": self._config.auto_paste_enabled(),
            "always_on_top": self._config.always_on_top(),
            "translate_enabled": self._config.translate_enabled(),
            "language": self._config.get_language()
        }

    def save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration from UI."""
        # Sanitize config before logging (remove api_key if present)
        sanitized = {k: v for k, v in config.items() if k != "api_key"}
        print(f"[API] Saving config: {sanitized}")

        # Save API Key (if present)
        if "api_key" in config and config["api_key"]:
            self._config.save_api_key(config["api_key"])
            print("[API] API key updated")

        # Save Sound Setting
        if "sound_enabled" in config:
            self._config.save_beep_setting(config["sound_enabled"])

        # Save Auto-Paste Setting
        if "auto_paste_enabled" in config:
            self._config.save_auto_paste_setting(config["auto_paste_enabled"])

        # Save Always on Top Setting
        if "always_on_top" in config:
            self._config.save_always_on_top_setting(config["always_on_top"])
            # Apply immediately
            self.set_always_on_top(config["always_on_top"])

        # Save Translate Setting
        if "translate_enabled" in config:
            self._config.save_translate_setting(config["translate_enabled"])

        # Save Language
        if "language" in config:
            self._config.save_language(config["language"])

        # Notify app to reload/apply
        self._app.reload_config()

    def set_always_on_top(self, enabled: bool) -> None:
        """Set window always-on-top state."""
        if self._app.dashboard_window:
            self._app.dashboard_window.on_top = enabled

    def save_language(self, language: str) -> None:
        """Save language setting instantly (without full config save)."""
        self._config.save_language(language)
        print(f"[API] Language set to: {language}")

    def save_api_key(self, api_key: str) -> None:
        """Save API key instantly."""
        if not api_key or not api_key.strip():
            print("[API] Invalid API key (empty)")
            return

        if not api_key.startswith("gsk_"):
            print("[API] Warning: API key format may be invalid")

        self._config.save_api_key(api_key)
        print("[API] API key saved successfully")

    def save_microphone(self, device_index: str) -> None:
        """Save microphone selection instantly."""
        self._config.save_input_device(int(device_index))
        print(f"[API] Microphone set to: {device_index}")

    def save_toggle(self, setting: str, value: bool) -> None:
        """Save a toggle setting instantly."""
        if setting == "sound_enabled":
            self._config.save_beep_setting(value)
        elif setting == "auto_paste_enabled":
            self._config.save_auto_paste_setting(value)
        elif setting == "translate_enabled":
            self._config.save_translate_setting(value)
        print(f"[API] {setting} set to: {value}")

    def clear_history(self) -> None:
        """Clear all recording history."""
        self._history.clear_all()
        print("[API] History cleared")

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

    def update_history_text(self, recording_id: str, new_text: str) -> None:
        """Update transcript text for a history item (edit mode)."""
        self._history.update_transcript(recording_id, new_text)
        print(f"[API] Updated history text for {recording_id}")

    def delete_recording(self, recording_id: str) -> bool:
        """Delete a single recording from history."""
        result = self._history.delete_recording(recording_id)
        print(f"[API] Deleted recording: {recording_id}")
        return result

    def create_merged_entry(self, merged_text: str) -> str:
        """Create a new history entry with merged text."""
        import time
        import pyautogui
        from models.recording import SourceType
        
        # Create a new history entry (no file, just text)
        # add_recording returns the actual recording_id it created
        recording_id = self._history.add_recording("merged", source=SourceType.FILE)
        self._history.update_transcript(recording_id, merged_text)
        
        # Copy to clipboard
        pyperclip.copy(merged_text)
        print(f"[API] Created merged entry: {recording_id}")
        
        # Auto-paste if enabled
        if self._config.auto_paste_enabled():
            time.sleep(0.1)
            pyautogui.hotkey('ctrl', 'v')
            print("[API] Merged text auto-pasted")
        
        return recording_id

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

    # === Audio Splitting Endpoints ===

    def check_file_duration(self, filepath: str) -> Dict[str, Any]:
        """
        Check audio file duration to determine if splitting is needed.

        Args:
            filepath: Path to the audio file

        Returns:
            Dict with duration info and should_split flag
        """
        from core.transcriber import GroqTranscriber

        transcriber = GroqTranscriber(self._config.get_api_key())
        duration_seconds = transcriber.get_audio_duration(filepath)

        return {
            "duration_seconds": duration_seconds,
            "duration_minutes": duration_seconds / 60,
            "should_split": duration_seconds > 600,
            "threshold_seconds": 600
        }

    def split_audio_file(self, filepath: str, recording_id: str) -> Dict[str, Any]:
        """
        Split audio file into chunks.

        Args:
            filepath: Path to the audio file
            recording_id: Original recording ID for naming

        Returns:
            Job metadata with chunk information
        """
        from core.audio_splitter import AudioSplitter

        splitter = AudioSplitter(temp_dir="temp")
        job_metadata = splitter.split(filepath, recording_id)

        return job_metadata

    def transcribe_chunk(self, chunk_path: str, language: str = "tr", translate: bool = False) -> str | None:
        """
        Transcribe a single chunk.

        Args:
            chunk_path: Path to the chunk file
            language: Language code for transcription
            translate: If True, translate to English

        Returns:
            Transcribed text or None if failed
        """
        from core.transcriber import GroqTranscriber

        transcriber = GroqTranscriber(self._config.get_api_key())
        result = transcriber.transcribe(chunk_path, language, translate)

        return result

    def start_split_workflow(self, filepath: str) -> None:
        """
        Start the split and transcription workflow for a long audio file.

        Args:
            filepath: Path to the audio file to split and transcribe
        """
        # Run in thread to avoid blocking
        threading.Thread(target=self._app.process_split_transcription_workflow, args=(filepath,), daemon=True).start()

    def save_transcript_to_file(self, text: str, default_filename: str) -> bool:
        """
        Open file dialog to save transcript text.

        Args:
            text: The transcript text to save
            default_filename: Suggested filename (e.g., transcript_2026-01-14.txt)

        Returns:
            True if file was saved, False if user cancelled
        """
        import tkinter as tk
        from tkinter import filedialog

        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)

            file_path = filedialog.asksaveasfilename(
                title="Transcripti Kaydet",
                defaultextension=".txt",
                initialfile=default_filename,
                filetypes=[("Metin Dosyaları", "*.txt"), ("Tüm Dosyalar", "*.*")]
            )

            root.destroy()

            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"[API] Saved transcript to: {file_path}")
                return True
            return False

        except Exception as e:
            print(f"[API] Error saving transcript: {e}")
            return False
