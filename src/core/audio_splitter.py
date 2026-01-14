"""
Audio Splitter Module - Splits long audio files into chunks for transcription
"""

from pathlib import Path
from typing import Dict, Any
import json
from datetime import datetime
import numpy as np


class AudioSplitter:
    """Split audio files into overlapping chunks for safe API transcription."""

    # Constants
    CHUNK_DURATION_SECONDS = 240  # 4 minutes (reduced from 10 to stay under 25MB)
    OVERLAP_SECONDS = 10
    MAX_PART_DURATION_SECONDS = 900  # 15 minutes (API safety)

    def __init__(self, temp_dir: str = "temp"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def get_audio_duration(self, filepath: str) -> float:
        """Get audio duration in seconds."""
        # Try soundfile first (for wav, mp3, flac, ogg)
        try:
            import soundfile as sf

            with sf.SoundFile(filepath) as audio_file:
                frames = len(audio_file)
                samplerate = audio_file.samplerate
                return frames / samplerate
        except Exception:
            # Fallback to mutagen for m4a and other formats
            try:
                from mutagen.mp4 import MP4

                audio = MP4(filepath)
                return audio.info.length
            except ImportError:
                print(
                    f"[WARNING] mutagen not installed. Cannot get duration for: {filepath}"
                )
                return 0.0
            except Exception as e:
                print(f"[ERROR] Failed to get duration with mutagen: {e}")
                return 0.0

    def should_split(self, filepath: str, threshold_seconds: int = 600) -> bool:
        """Check if audio file should be split (duration > threshold)."""
        duration_seconds = self.get_audio_duration(filepath)
        return duration_seconds > threshold_seconds

    def split(self, filepath: str, recording_id: str) -> Dict[str, Any]:
        """
        Split audio file into chunks.

        Args:
            filepath: Path to original audio file
            recording_id: Original recording ID for naming

        Returns:
            Dict with job metadata
        """
        import soundfile as sf
        import wave

        # Read the audio file
        with sf.SoundFile(filepath) as audio_file:
            samplerate = audio_file.samplerate
            total_frames = len(audio_file)
            audio_data = audio_file.read(dtype="float32")

        # Convert to mono if stereo
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)

        # Calculate durations
        total_duration_seconds = total_frames / samplerate
        chunk_frames = int(self.CHUNK_DURATION_SECONDS * samplerate)
        overlap_frames = int(self.OVERLAP_SECONDS * samplerate)

        chunks = []
        part_number = 1
        current_frame = 0

        while current_frame < total_frames:
            end_frame = min(current_frame + chunk_frames, total_frames)

            # Calculate actual chunk duration
            part_duration_frames = end_frame - current_frame
            part_duration_seconds = part_duration_frames / samplerate

            # Skip if chunk is too small (less than 1 second or too much overlap)
            if part_duration_seconds < 1.0:
                break

            # Check max duration
            if part_duration_seconds > self.MAX_PART_DURATION_SECONDS:
                raise ValueError(
                    f"Part {part_number} exceeds max duration: {part_duration_seconds}s"
                )

            # Extract chunk
            chunk_data = audio_data[current_frame:end_frame]

            # Generate filename
            chunk_filename = f"{Path(filepath).stem}_{part_number:03d}_part.wav"
            chunk_path = self.temp_dir / chunk_filename

            # Write chunk as WAV file
            # Convert float32 (-1 to 1) to int16
            chunk_data_int16 = (chunk_data * 32767).astype(np.int16)

            with wave.open(str(chunk_path), "w") as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 16-bit
                wav_file.setframerate(samplerate)
                wav_file.writeframes(chunk_data_int16.tobytes())

            current_start_seconds = current_frame / samplerate
            current_end_seconds = end_frame / samplerate

            chunks.append(
                {
                    "part": part_number,
                    "filename": chunk_filename,
                    "start_ms": int(current_start_seconds * 1000),
                    "end_ms": int(current_end_seconds * 1000),
                    "start_seconds": current_start_seconds,
                    "end_seconds": current_end_seconds,
                }
            )

            # Move to next chunk (with overlap)
            # CRITICAL: If we reached the end, break to prevent infinite loop
            if end_frame >= total_frames:
                break

            current_frame = end_frame - overlap_frames

            # Safety: If we're not making progress, break
            if current_frame >= end_frame:
                break

            part_number += 1

        # Create job metadata
        job_metadata = {
            "total_parts": len(chunks),
            "chunk_duration_seconds": self.CHUNK_DURATION_SECONDS,
            "overlap_seconds": self.OVERLAP_SECONDS,
            "created_at": datetime.now().isoformat(),
            "original_filename": Path(filepath).name,
            "original_recording_id": recording_id,
            "chunks": chunks,
        }

        # Save job_meta.json
        meta_path = self.temp_dir / f"{recording_id}_job_meta.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(job_metadata, f, indent=2, ensure_ascii=False)

        return job_metadata
