"""
Audio Recorder Module - Captures audio from microphone and saves to .wav file.
Uses sounddevice and numpy for non-blocking audio capture.
"""

import sounddevice as sd
import numpy as np
import wave
import tempfile
import threading
from pathlib import Path
from typing import Optional


class AudioRecorder:
    """
    Non-blocking audio recorder using sounddevice and numpy.

    Features:
    - Records in separate thread (non-blocking)
    - Saves to temporary .wav file
    - Configurable sample rate and channels
    - Graceful interruption handling
    """

    def __init__(self, sample_rate: int = 16000, channels: int = 1):
        """
        Initialize the audio recorder.

        Args:
            sample_rate: Audio sample rate in Hz (default: 16000 for Groq compatibility)
            channels: Number of audio channels (1=mono, 2=stereo)
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self._actual_sample_rate = sample_rate  # May differ per device

        # Recording state
        self._is_recording = False
        self._recording_thread: Optional[threading.Thread] = None
        self._recorded_frames = []
        self._audio_file_path: Optional[str] = None

    def start_recording(self, device_index: Optional[int] = None) -> None:
        """
        Start audio recording in a separate thread.

        Args:
            device_index: Microphone device index (None for system default)

        Returns:
            None (returns immediately, recording happens in background)
        """
        if self._is_recording:
            raise RuntimeError("Recording is already in progress")

        self._is_recording = True
        self._recorded_frames = []
        self._audio_file_path = None

        # Start recording thread
        self._recording_thread = threading.Thread(
            target=self._record_thread,
            args=(device_index,),
            daemon=True
        )
        self._recording_thread.start()

    def stop_recording(self) -> Optional[str]:
        """
        Stop recording and save to temporary .wav file.

        Returns:
            Path to the saved .wav file, or None if recording wasn't active
        """
        if not self._is_recording:
            return None

        # Signal thread to stop
        self._is_recording = False

        # Wait for thread to finish
        if self._recording_thread:
            self._recording_thread.join(timeout=5.0)
            self._recording_thread = None

        # Save to WAV file
        if self._recorded_frames:
            self._audio_file_path = self._save_to_wav()

        return self._audio_file_path

    def is_recording(self) -> bool:
        """Check if recording is currently active."""
        return self._is_recording

    def get_last_file(self) -> Optional[str]:
        """Get the path to the most recently recorded file."""
        return self._audio_file_path

    def _record_thread(self, device_index: Optional[int]) -> None:
        """
        Recording loop running in separate thread.

        Args:
            device_index: Microphone device index
        """
        stream = None
        
        try:
            # If specific device is selected, try to use it
            if device_index is not None:
                print(f"Opening stream for device {device_index}...")
                try:
                    stream = sd.InputStream(
                        channels=self.channels,
                        dtype=np.float32,
                        device=device_index,
                        callback=self._audio_callback
                    )
                except Exception as device_error:
                    # Device not found or invalid - fallback to default
                    print(f"Device {device_index} not available: {device_error}")
                    print("Falling back to default system microphone...")
                    stream = sd.InputStream(
                        samplerate=self.sample_rate,
                        channels=self.channels,
                        dtype=np.float32,
                        callback=self._audio_callback
                    )
            else:
                # Use configured sample rate for default device
                stream = sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=self.channels,
                    dtype=np.float32,
                    callback=self._audio_callback
                )
            
            with stream:
                self._actual_sample_rate = int(stream.samplerate)
                print(f"Recording started. Sample rate: {self._actual_sample_rate} Hz")
                
                # Keep recording until stop is signaled
                while self._is_recording:
                    sd.sleep(100)  # Check every 100ms

        except Exception as e:
            print(f"Recording error: {e}")
            self._is_recording = False

    def _audio_callback(self, indata, frames, time, status) -> None:
        """
        Callback function for audio stream.

        Args:
            indata: Audio data chunk (numpy array)
            frames: Number of frames
            time: Timestamp info
            status: Stream status
        """
        if status:
            print(f"Stream status: {status}")

        # Store audio chunk
        if self._is_recording:
            self._recorded_frames.append(indata.copy())

    def _save_to_wav(self) -> str:
        """
        Save recorded audio to temporary WAV file.

        Returns:
            Path to the saved .wav file
        """
        # Create temp directory in project root
        project_root = Path(__file__).parent.parent.parent
        temp_dir = project_root / "temp"
        temp_dir.mkdir(exist_ok=True)

        # Generate unique filename with timestamp
        import time
        timestamp = int(time.time() * 1000)
        temp_file = str(temp_dir / f"recording_{timestamp}.wav")

        # Concatenate all frames
        audio_data = np.concatenate(self._recorded_frames, axis=0)

        # Convert float32 to int16 for WAV compatibility
        audio_int16 = (audio_data * 32767).astype(np.int16)

        # Save as WAV (use actual sample rate from recording)
        with wave.open(temp_file, 'wb') as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2)  # 2 bytes for int16
            wav_file.setframerate(self._actual_sample_rate)
            wav_file.writeframes(audio_int16.tobytes())

        return temp_file

    def cleanup_temp_files(self) -> None:
        """
        Delete all recording files from the temp directory.
        Call this to free up disk space.
        """
        project_root = Path(__file__).parent.parent.parent
        temp_dir = project_root / "temp"

        if temp_dir.exists():
            for file in temp_dir.glob("recording_*.wav"):
                try:
                    file.unlink()
                except Exception as e:
                    print(f"Warning: Could not delete {file}: {e}")

    def get_available_devices(self) -> list:
        """
        Get list of available input devices.

        Returns:
            List of device names
        """
        devices = []
        try:
            device_list = sd.query_devices()
            for i, device in enumerate(device_list):
                if device['max_input_channels'] > 0:
                    devices.append(f"{i}: {device['name']}")
        except Exception as e:
            print(f"Error querying devices: {e}")
            devices = ["Default Device"]

        return devices


# Standalone test
def test_recorder():
    """Test the audio recorder standalone."""
    print("Audio Recorder Test")
    print("=" * 40)

    recorder = AudioRecorder()

    # Show available devices
    devices = recorder.get_available_devices()
    print("\nAvailable audio devices:")
    for device in devices:
        print(f"  {device}")

    print("\nInstructions:")
    print("1. Recording will start for 5 seconds")
    print("2. Speak into your microphone")
    print("3. Recording will stop and save to .wav file")
    print("\nPress Enter to start...")
    input()

    # Start recording
    print("Recording... (speak now!)")
    recorder.start_recording()

    # Record for 5 seconds
    import time
    time.sleep(5)

    # Stop recording
    print("Stopping recording...")
    file_path = recorder.stop_recording()

    if file_path:
        print(f"Audio saved to: {file_path}")
        print(f"File size: {Path(file_path).stat().st_size / 1024:.2f} KB")
    else:
        print("No audio was recorded.")


if __name__ == "__main__":
    test_recorder()
