"""
Groq Transcriber Module - Speech-to-text conversion using Groq API.
Uses whisper-large-v3 model for high accuracy transcription.
"""

import time
from pathlib import Path
from typing import Optional
from groq import Groq
import sys

# Add parent directory for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import Config


class GroqTranscriber:
    """
    Transcribes audio files using Groq's Whisper API.

    Features:
    - Uses whisper-large-v3 model (best accuracy)
    - Automatic API key loading from .env
    - Retry logic for network failures
    - Turkish language support
    - Error handling for invalid API keys
    """

    # Groq model to use
    MODEL = "whisper-large-v3"

    # Retry configuration
    MAX_RETRIES = 3
    RETRY_DELAY = 1.0  # seconds

    # Groq API file size limit (25 MB)
    MAX_FILE_SIZE_MB = 25
    WARNING_THRESHOLD_MB = 20  # Warn at 20 MB

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the Groq transcriber.

        Args:
            api_key: Groq API key (if None, loads from Config)
        """
        if api_key is None:
            config = Config()
            api_key = config.get_api_key()

        if not api_key:
            raise ValueError(
                "Groq API key not found. Please set GROQ_API_KEY in .env file "
                "or pass api_key parameter."
            )

        self.client = Groq(api_key=api_key)

    def _check_file_size(self, audio_file_path: str) -> bool:
        """
        Check audio file size against Groq API limits.

        Args:
            audio_file_path: Path to the audio file

        Returns:
            True if file size is acceptable, False if too large
        """
        file_size_bytes = Path(audio_file_path).stat().st_size
        file_size_mb = file_size_bytes / (1024 * 1024)

        print(f"[INFO] Audio file size: {file_size_mb:.2f} MB")

        if file_size_mb >= self.MAX_FILE_SIZE_MB:
            print(f"[ERROR] File too large! Groq API limit is {self.MAX_FILE_SIZE_MB} MB.")
            print(f"[ERROR] Your file is {file_size_mb:.2f} MB. Please record a shorter audio.")
            return False

        if file_size_mb >= self.WARNING_THRESHOLD_MB:
            print(f"[WARNING] File is large ({file_size_mb:.2f} MB). Approaching API limit of {self.MAX_FILE_SIZE_MB} MB.")

        return True

    def transcribe(self, audio_file_path: str, language: Optional[str] = "tr") -> Optional[str]:
        """
        Transcribe an audio file using Groq's Whisper API.

        Args:
            audio_file_path: Path to the audio file (.wav, .mp3, etc.)
            language: Language code (default: "tr" for Turkish)

        Returns:
            Transcribed text as string, or None if transcription failed
        """
        # Validate file exists
        if not Path(audio_file_path).exists():
            print(f"Error: Audio file not found: {audio_file_path}")
            return None

        # Check file size before attempting transcription
        if not self._check_file_size(audio_file_path):
            return None

        # Try transcription with retry logic
        for attempt in range(self.MAX_RETRIES):
            try:
                result = self._transcribe_once(audio_file_path, language)
                return result

            except Exception as e:
                error_msg = str(e).lower()

                # API key error - don't retry
                if "unauthorized" in error_msg or "api key" in error_msg or "401" in error_msg:
                    print(f"Error: Invalid Groq API key. Please check your GROQ_API_KEY.")
                    return None

                # Network error - retry with backoff
                if attempt < self.MAX_RETRIES - 1:
                    wait_time = self.RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                    print(f"Network error, retrying in {wait_time}s... (attempt {attempt + 1}/{self.MAX_RETRIES})")
                    time.sleep(wait_time)
                else:
                    print(f"Error: Transcription failed after {self.MAX_RETRIES} attempts: {e}")
                    return None

        return None

    def _transcribe_once(self, audio_file_path: str, language: Optional[str] = "tr") -> str:
        """
        Perform a single transcription attempt.

        Args:
            audio_file_path: Path to the audio file
            language: Language code for transcription

        Returns:
            Transcribed text

        Raises:
            Exception: If API call fails
        """
        print(f"[DEBUG] Transcriber: Processing file: {audio_file_path}")

        # Read audio file
        with open(audio_file_path, "rb") as audio_file:
            # Get file size for validation
            audio_file.seek(0, 2)
            file_size = audio_file.tell()
            audio_file.seek(0)

            if file_size == 0:
                raise ValueError("Audio file is empty")

            # Create filename for API (Groq needs the original filename)
            filename = Path(audio_file_path).name

            # Build API parameters
            api_params = {
                "file": (filename, audio_file.read()),
                "model": self.MODEL,
                "response_format": "text"
            }

            # Only include language parameter if not None (auto-detect)
            if language is not None:
                api_params["language"] = language

            # Call Groq API
            transcription = self.client.audio.transcriptions.create(**api_params)

        return transcription

    def transcribe_with_language(self, audio_file_path: str, language: str = "tr") -> Optional[str]:
        """
        Transcribe with explicit language specification.

        Args:
            audio_file_path: Path to the audio file
            language: Language code (default: "tr" for Turkish)

        Returns:
            Transcribed text, or None if failed
        """
        if not Path(audio_file_path).exists():
            print(f"Error: Audio file not found: {audio_file_path}")
            return None

        try:
            with open(audio_file_path, "rb") as audio_file:
                filename = Path(audio_file_path).name

                transcription = self.client.audio.transcriptions.create(
                    file=(filename, audio_file.read()),
                    model=self.MODEL,
                    response_format="text",
                    language=language
                )

            return transcription

        except Exception as e:
            print(f"Transcription error: {e}")
            return None

    def test_api_key(self) -> bool:
        """
        Test if the API key is valid by making a minimal API call.

        Returns:
            True if API key is valid, False otherwise
        """
        try:
            # Try to list models (minimal API call)
            self.client.models.list()
            return True
        except Exception as e:
            error_msg = str(e).lower()
            if "unauthorized" in error_msg or "api key" in error_msg or "401" in error_msg:
                print(f"API key validation failed: {e}")
                return False
            # Other errors might be temporary network issues
            return True


# Standalone test
def test_transcriber():
    """Test the transcriber standalone."""
    print("Groq Transcriber Test")
    print("=" * 40)

    # Find .env file by going up from current script location
    current_file = Path(__file__).resolve()
    project_root = current_file.parent.parent.parent  # Go up 3 levels: src/core/transcriber.py -> src/core -> src -> project_root

    env_file = project_root / ".env"

    if not env_file.exists():
        print(f"\n✗ Error: .env file not found!")
        print(f"   Expected location: {env_file}")
        print(f"\nPlease create .env file with your Groq API key:")
        print(f"   GROQ_API_KEY=gsk_your_api_key_here")
        print(f"\nYou can copy .env.example to .env:")
        print(f"   cp .env.example .env")
        print(f"   Then edit .env and add your API key.")
        return

    # Check API key
    print("Checking API key...")
    try:
        transcriber = GroqTranscriber()
    except ValueError as e:
        print(f"✗ {e}")
        print("\nPlease add your Groq API key to .env file:")
        print("1. Get your key from: https://console.groq.com/keys")
        print("2. Add this line to .env:")
        print("   GROQ_API_KEY=gsk_...")
        return

    if transcriber.test_api_key():
        print("✓ API key is valid")
    else:
        print("✗ API key validation failed")
        return

    # Check for test audio file (use project_root from above)
    test_file = "test_audio.wav"
    test_file_path = project_root / test_file

    if not test_file_path.exists():
        # Check temp folder for recordings
        temp_dir = project_root / "temp"
        wav_files = list(temp_dir.glob("recording_*.wav")) if temp_dir.exists() else []

        if wav_files:
            # Use most recent recording
            test_file_path = max(wav_files, key=lambda p: p.stat().st_mtime)
            print(f"\nUsing most recent recording: {test_file_path.name}")
        else:
            print(f"\n✗ No test audio found!")
            print(f"   Options:")
            print(f"   1. Run: python src/core/recorder.py")
            print(f"   2. Place a .wav file at: {test_file_path}")
            print(f"   3. Record from temp folder: {temp_dir}")
            return
    else:
        test_file_path = str(test_file_path)

    # Transcribe
    print(f"\nTranscribing: {test_file_path}")
    print("(this may take a few seconds...)")

    result = transcriber.transcribe(str(test_file_path))

    if result:
        print("\n" + "=" * 40)
        print("Transcription:")
        print("=" * 40)
        print(result)
        print("=" * 40)
    else:
        print("✗ Transcription failed.")


if __name__ == "__main__":
    test_transcriber()
