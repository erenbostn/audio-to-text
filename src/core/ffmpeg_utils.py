"""
FFmpeg Utilities Module - Optional FFmpeg integration for format conversion.

This module provides utilities to:
- Check if FFmpeg is installed on the system
- Convert unsupported formats (M4A, AAC) to WAV for processing
- Get audio duration via ffprobe for formats not supported by soundfile
"""

import subprocess
import shutil
from pathlib import Path
from typing import Optional, Tuple


def is_ffmpeg_available() -> bool:
    """
    Check if FFmpeg is installed and accessible in system PATH.
    
    Returns:
        True if FFmpeg is available, False otherwise.
    """
    try:
        # Use shutil.which for cross-platform PATH lookup
        if shutil.which("ffmpeg") is None:
            return False
        
        # Verify it actually runs
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def is_ffprobe_available() -> bool:
    """
    Check if ffprobe is installed and accessible in system PATH.
    
    Returns:
        True if ffprobe is available, False otherwise.
    """
    try:
        if shutil.which("ffprobe") is None:
            return False
        
        result = subprocess.run(
            ["ffprobe", "-version"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def convert_to_wav(input_path: str, output_path: str) -> Tuple[bool, str]:
    """
    Convert any audio/video file to WAV format using FFmpeg.
    
    Args:
        input_path: Path to the input audio/video file.
        output_path: Path where the WAV file will be saved.
    
    Returns:
        Tuple of (success: bool, message: str).
        On success, message is empty. On failure, message contains error details.
    """
    if not is_ffmpeg_available():
        return False, "FFmpeg bulunamadı. Kurulum: https://ffmpeg.org/download.html"
    
    try:
        # FFmpeg command for conversion:
        # -i: input file
        # -vn: disable video (extract audio only)
        # -acodec pcm_s16le: 16-bit PCM audio (standard WAV)
        # -ar 16000: 16kHz sample rate (optimal for Whisper)
        # -ac 1: mono channel
        # -y: overwrite output without asking
        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            "-y",
            output_path
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=300  # 5 minute timeout for large files
        )
        
        if result.returncode == 0:
            # Verify output file was created
            if Path(output_path).exists() and Path(output_path).stat().st_size > 0:
                return True, ""
            else:
                return False, "Dönüştürme başarılı görünüyor ama çıktı dosyası oluşmadı."
        else:
            error_msg = result.stderr.decode("utf-8", errors="ignore")
            # Extract meaningful part of error
            if "No such file or directory" in error_msg:
                return False, f"Dosya bulunamadı: {input_path}"
            elif "Invalid data" in error_msg:
                return False, "Dosya formatı tanınmadı veya bozuk."
            else:
                return False, f"FFmpeg hatası: {error_msg[:200]}"
                
    except subprocess.TimeoutExpired:
        return False, "Dönüştürme zaman aşımına uğradı (>5 dakika)."
    except Exception as e:
        return False, f"Beklenmeyen hata: {str(e)}"


def convert_wav_to_mp3(wav_path: str, mp3_path: str) -> Tuple[bool, str]:
    """
    Convert WAV file to MP3 for disk space savings.
    
    Args:
        wav_path: Path to the input WAV file.
        mp3_path: Path where the MP3 file will be saved.
    
    Returns:
        Tuple of (success: bool, message: str).
    """
    if not is_ffmpeg_available():
        return False, "FFmpeg bulunamadı"
    
    try:
        cmd = [
            "ffmpeg",
            "-i", wav_path,
            "-acodec", "libmp3lame",
            "-ab", "128k",  # 128 kbps - good quality for speech
            "-ar", "16000", # Keep 16kHz sample rate
            "-ac", "1",     # Mono
            "-y",
            mp3_path
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=60
        )
        
        if result.returncode == 0:
            if Path(mp3_path).exists() and Path(mp3_path).stat().st_size > 0:
                return True, ""
            else:
                return False, "MP3 dosyası oluşturulamadı"
        else:
            return False, "FFmpeg dönüştürme hatası"
                
    except subprocess.TimeoutExpired:
        return False, "Dönüştürme zaman aşımı"
    except Exception as e:
        return False, str(e)


def get_duration_ffprobe(filepath: str) -> Optional[float]:
    """
    Get audio duration in seconds using ffprobe.
    
    This is a fallback for formats not supported by soundfile/mutagen.
    
    Args:
        filepath: Path to the audio file.
    
    Returns:
        Duration in seconds, or None if ffprobe is unavailable or fails.
    """
    if not is_ffprobe_available():
        return None
    
    try:
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            filepath
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=30
        )
        
        if result.returncode == 0:
            duration_str = result.stdout.decode("utf-8").strip()
            return float(duration_str)
        return None
        
    except (subprocess.TimeoutExpired, ValueError, Exception):
        return None


def get_ffmpeg_version() -> Optional[str]:
    """
    Get FFmpeg version string for display.
    
    Returns:
        Version string (e.g., "6.1.1") or None if unavailable.
    """
    if not is_ffmpeg_available():
        return None
    
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"],
            capture_output=True,
            timeout=5
        )
        
        if result.returncode == 0:
            # Parse first line: "ffmpeg version 6.1.1 Copyright..."
            first_line = result.stdout.decode("utf-8").split("\n")[0]
            parts = first_line.split()
            if len(parts) >= 3 and parts[0] == "ffmpeg" and parts[1] == "version":
                return parts[2]
        return None
        
    except Exception:
        return None


# Supported formats that require FFmpeg for conversion
FFMPEG_REQUIRED_FORMATS = {".m4a", ".aac", ".mp4", ".mkv", ".webm", ".wma", ".opus"}

# Formats natively supported by soundfile (no FFmpeg needed)  
NATIVE_FORMATS = {".wav", ".mp3", ".flac", ".ogg"}


def needs_ffmpeg_conversion(filepath: str) -> bool:
    """
    Check if a file format requires FFmpeg for conversion.
    
    Args:
        filepath: Path to the audio file.
    
    Returns:
        True if FFmpeg is needed, False if format is natively supported.
    """
    ext = Path(filepath).suffix.lower()
    return ext in FFMPEG_REQUIRED_FORMATS


# Output format configurations for converter
OUTPUT_FORMATS = {
    "mp3": {"ext": ".mp3", "codec": "libmp3lame", "extra": ["-ab", "192k"]},
    "wav": {"ext": ".wav", "codec": "pcm_s16le", "extra": []},
    "flac": {"ext": ".flac", "codec": "flac", "extra": []},
    "ogg": {"ext": ".ogg", "codec": "libvorbis", "extra": ["-aq", "5"]},
    "aac": {"ext": ".aac", "codec": "aac", "extra": ["-ab", "192k"]},
    "m4a": {"ext": ".m4a", "codec": "aac", "extra": ["-ab", "192k"]},
    "opus": {"ext": ".opus", "codec": "libopus", "extra": ["-ab", "128k"]},
    "wma": {"ext": ".wma", "codec": "wmav2", "extra": ["-ab", "192k"]},
}


def convert_audio(input_path: str, output_path: str, output_format: str) -> Tuple[bool, str]:
    """
    Convert audio file to specified format using FFmpeg.
    
    Args:
        input_path: Path to the input audio file.
        output_path: Path where the converted file will be saved.
        output_format: Target format key (e.g., "mp3", "wav", "flac").
    
    Returns:
        Tuple of (success: bool, message: str).
    """
    if not is_ffmpeg_available():
        return False, "FFmpeg kurulu değil. Kurulum: ffmpeg.org/download.html"
    
    if output_format not in OUTPUT_FORMATS:
        return False, f"Desteklenmeyen format: {output_format}"
    
    format_config = OUTPUT_FORMATS[output_format]
    
    try:
        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-vn",  # No video
            "-acodec", format_config["codec"],
        ]
        
        # Add format-specific options
        cmd.extend(format_config["extra"])
        
        # Add output path
        cmd.extend(["-y", output_path])
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            timeout=600  # 10 minute timeout
        )
        
        if result.returncode == 0:
            if Path(output_path).exists() and Path(output_path).stat().st_size > 0:
                return True, ""
            else:
                return False, "Dönüştürme başarısız - çıktı dosyası oluşmadı"
        else:
            error_msg = result.stderr.decode("utf-8", errors="ignore")
            return False, f"FFmpeg hatası: {error_msg[:200]}"
                
    except subprocess.TimeoutExpired:
        return False, "Dönüştürme zaman aşımına uğradı (>10 dakika)"
    except Exception as e:
        return False, f"Hata: {str(e)}"


def get_supported_output_formats() -> list:
    """Get list of supported output formats for UI."""
    return list(OUTPUT_FORMATS.keys())

