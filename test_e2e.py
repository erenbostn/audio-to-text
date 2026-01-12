#!/usr/bin/env python3
"""
End-to-End Test - Record → Transcribe → Inject
Tests the complete workflow.
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from core.recorder import AudioRecorder
from core.transcriber import GroqTranscriber
from core.input_simulator import TextInjector


def test_full_workflow():
    """Test the complete record → transcribe → inject workflow."""
    print("=" * 50)
    print("GroqWhisper Desktop - End-to-End Test")
    print("=" * 50)

    # 1. Audio Recording
    print("\n[1/3] Audio Recording")
    print("   This will record for 10 seconds.")
    print("   Speak clearly into your microphone...")
    print("\n   Press Enter to start recording...")
    input()

    recorder = AudioRecorder()

    print("\n   Recording for 10 seconds...")
    print("   SPEAK NOW: Merhaba, bu bir test kaydıdır.")
    recorder.start_recording()

    for i in range(10, 0, -1):
        print(f"   {i} seconds remaining...", end="\r")
        time.sleep(1)

    print("\n   Stopping recording...")
    audio_file = recorder.stop_recording()

    if audio_file and Path(audio_file).exists():
        print(f"   ✓ Audio saved: {Path(audio_file).name}")
        print(f"   Size: {Path(audio_file).stat().st_size / 1024:.1f} KB")
    else:
        print("   ✗ Recording failed")
        return

    # 2. Transcription
    print("\n[2/3] Transcription (Groq API)")
    print("   Sending to Whisper Large V3...")
    print("   This may take 10-30 seconds depending on audio length...")

    transcriber = GroqTranscriber()
    result = transcriber.transcribe(audio_file)

    if result:
        print("\n   ✓ Transcription successful!")
        print("   " + "-" * 46)
        print(f"   {result}")
        print("   " + "-" * 46)
    else:
        print("   ✗ Transcription failed")
        return

    # 3. Text Injection
    print("\n[3/3] Text Injection Test")
    print("   The transcribed text will be typed where your cursor is.")
    print("\n   Instructions:")
    print("   1. Open Notepad or any text editor")
    print("   2. Click where you want the text to appear")
    print("   3. Press Enter below...")
    input()

    print(f"\n   Injecting in 3 seconds...")
    print(f"   Make sure your text editor is focused!")
    time.sleep(3)

    injector = TextInjector()
    if injector.inject_text(result):
        print("   ✓ Text injected successfully!")
    else:
        print("   ✗ Text injection failed")

    # Cleanup
    print("\n[Cleanup]")
    cleanup = input("   Delete temp audio file? (y/n): ").lower().strip()
    if cleanup == 'y':
        Path(audio_file).unlink()
        print(f"   ✓ Deleted: {Path(audio_file).name}")

    print("\n" + "=" * 50)
    print("Test complete!")
    print("=" * 50)


if __name__ == "__main__":
    test_full_workflow()
