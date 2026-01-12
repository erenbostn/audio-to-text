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

    def transcribe(self, audio_file_path: str) -> Optional[str]:
        """
        Transcribe an audio file using Groq's Whisper API.

        Args:
            audio_file_path: Path to the audio file (.wav, .mp3, etc.)

        Returns:
            Transcribed text as string, or None if transcription failed
        """
        # Validate file exists
        if not Path(audio_file_path).exists():
            print(f"Error: Audio file not found: {audio_file_path}")
            return None

        # Try transcription with retry logic
        for attempt in range(self.MAX_RETRIES):
            try:
                result = self._transcribe_once(audio_file_path)
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

    def _transcribe_once(self, audio_file_path: str) -> str:
        """
        Perform a single transcription attempt.

        Args:
            audio_file_path: Path to the audio file

        Returns:
            Transcribed text

        Raises:
            Exception: If API call fails
        """
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

            # Call Groq API
            transcription = self.client.audio.transcriptions.create(
                file=(filename, audio_file.read()),
                model=self.MODEL,
                response_format="text"
            )

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

    # Check API key
    print("Checking API key...")
    transcriber = GroqTranscriber()

    if transcriber.test_api_key():
        print("✓ API key is valid")
    else:
        print("✗ API key is invalid")
        return

    # Check for test audio file
    test_file = "test_audio.wav"
    if not Path(test_file).exists():
        print(f"\nNo test audio found at: {test_file}")
        print("Place a .wav file there to test transcription.")
        print(f"\nOr run: python src/core/recorder.py")
        return

    # Transcribe
    print(f"\nTranscribing: {test_file}")
    print("(this may take a few seconds...)")

    result = transcriber.transcribe(test_file)

    if result:
        print("\n" + "=" * 40)
        print("Transcription:")
        print("=" * 40)
        print(result)
        print("=" * 40)
    else:
        print("Transcription failed.")


if __name__ == "__main__":
    test_transcriber()
