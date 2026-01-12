"""
Sound Feedback Module - Audio cues for recording state changes.
Uses Windows-native winsound for beep sounds.
"""

import sys
from typing import Callable


class SoundFeedback:
    """
    Windows sound feedback using winsound.

    Features:
    - Start beep: 1000Hz, 200ms
    - Stop beep: 700Hz, 200ms
    - Respects user preference setting
    - Gracefully handles errors (non-blocking)
    """

    # Audio constants
    START_BEEP_FREQ = 1000  # Hz
    START_BEEP_DURATION = 200  # ms
    STOP_BEEP_FREQ = 700  # Hz
    STOP_BEEP_DURATION = 200  # ms

    def __init__(self, enabled_check: Callable[[], bool]):
        """
        Initialize sound feedback.

        Args:
            enabled_check: Callable that returns True if beep sounds are enabled
        """
        self._enabled = enabled_check

    def play_start_beep(self) -> None:
        """
        Play start recording beep sound.

        High-pitched beep (1000Hz) to indicate recording has started.
        Only plays if user has enabled beep sounds and platform is Windows.
        """
        if not self._enabled():
            return

        if sys.platform != 'win32':
            return

        try:
            import winsound
            winsound.Beep(self.START_BEEP_FREQ, self.START_BEEP_DURATION)
        except Exception:
            # Silently fail if sound device unavailable
            pass

    def play_stop_beep(self) -> None:
        """
        Play stop recording beep sound.

        Lower-pitched beep (700Hz) to indicate recording has stopped.
        Only plays if user has enabled beep sounds and platform is Windows.
        """
        if not self._enabled():
            return

        if sys.platform != 'win32':
            return

        try:
            import winsound
            winsound.Beep(self.STOP_BEEP_FREQ, self.STOP_BEEP_DURATION)
        except Exception:
            # Silently fail if sound device unavailable
            pass

    def is_enabled(self) -> bool:
        """
        Check if beep sounds are enabled.

        Returns:
            True if enabled, False otherwise
        """
        return self._enabled()
