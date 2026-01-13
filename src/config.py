"""
Configuration management for GroqWhisper Desktop.
Loads and saves settings from .env file.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Configuration manager for application settings."""

    def __init__(self, env_path: str = None):
        """
        Initialize configuration.

        Args:
            env_path: Path to .env file. If None, uses default .env in project root.
        """
        if env_path is None:
            # Default to .env in project root (assuming src/ is in project root)
            project_root = Path(__file__).parent.parent
            env_path = project_root / ".env"

        self.env_path = env_path
        load_dotenv(env_path)

    def get_api_key(self) -> str | None:
        """Get Groq API key from environment."""
        return os.getenv("GROQ_API_KEY")

    def save_api_key(self, api_key: str) -> None:
        """
        Save Groq API key to .env file.

        Args:
            api_key: The API key to save.
        """
        # Read existing .env content
        content = ""
        if self.env_path.exists():
            with open(self.env_path, "r", encoding="utf-8") as f:
                content = f.read()

        # Update or add GROQ_API_KEY line
        lines = content.split("\n")
        updated = False
        for i, line in enumerate(lines):
            if line.startswith("GROQ_API_KEY="):
                lines[i] = f"GROQ_API_KEY={api_key}"
                updated = True
                break

        if not updated:
            lines.append(f"GROQ_API_KEY={api_key}")

        # Write back to .env
        with open(self.env_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def get_sample_rate(self) -> int:
        """Get recording sample rate."""
        return int(os.getenv("RECORDING_SAMPLE_RATE", "16000"))

    def get_channels(self) -> int:
        """Get recording channel count."""
        return int(os.getenv("RECORDING_CHANNELS", "1"))

    def get_hotkey(self) -> str:
        """Get default hotkey string."""
        return os.getenv("DEFAULT_HOTKEY", "<ctrl>+<alt>+<space>")

    def show_overlay(self) -> bool:
        """Get overlay visibility preference."""
        return os.getenv("SHOW_OVERLAY", "false").lower() == "true"

    def play_beep(self) -> bool:
        """Get beep sound preference."""
        return os.getenv("PLAY_BEEP_SOUND", "true").lower() == "true"

    def get_language(self) -> str:
        """Get transcription language code."""
        return os.getenv("TRANSCRIPTION_LANGUAGE", "tr")

    def save_language(self, language: str) -> None:
        """
        Save transcription language to .env.

        Args:
            language: Language code (e.g., "tr", "en", "de").
        """
        self._save_env_value("TRANSCRIPTION_LANGUAGE", language)
        os.environ["TRANSCRIPTION_LANGUAGE"] = language

    def reload_env(self) -> None:
        """Reload environment variables from .env file."""
        load_dotenv(self.env_path, override=True)

    def save_beep_setting(self, enabled: bool) -> None:
        """
        Save beep sound setting to .env and update os.environ.

        Args:
            enabled: Whether beep sound is enabled.
        """
        value = "true" if enabled else "false"
        self._save_env_value("PLAY_BEEP_SOUND", value)
        os.environ["PLAY_BEEP_SOUND"] = value

    def save_overlay_setting(self, enabled: bool) -> None:
        """
        Save overlay setting to .env and update os.environ.

        Args:
            enabled: Whether overlay is enabled.
        """
        value = "true" if enabled else "false"
        self._save_env_value("SHOW_OVERLAY", value)
        os.environ["SHOW_OVERLAY"] = value

    def _save_env_value(self, key: str, value: str) -> None:
        """
        Save a key-value pair to .env file.

        Args:
            key: Environment variable name.
            value: Value to set.
        """
        # Read existing .env content
        content = ""
        if self.env_path.exists():
            with open(self.env_path, "r", encoding="utf-8") as f:
                content = f.read()

        # Update or add the key
        lines = content.split("\n")
        updated = False
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}"
                updated = True
                break

        if not updated:
            lines.append(f"{key}={value}")

        # Write back to .env
        with open(self.env_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def get_input_device(self) -> int:
        """Get input device index from .env."""
        try:
            return int(os.getenv("INPUT_DEVICE", "-1"))
        except ValueError:
            return -1

    def save_input_device(self, device_index: int) -> None:
        """
        Save input device index to .env.

        Args:
            device_index: Device index.
        """
        self._save_env_value("INPUT_DEVICE", str(device_index))
        os.environ["INPUT_DEVICE"] = str(device_index)
