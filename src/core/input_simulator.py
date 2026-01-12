"""
Text Injector Module - Injects text at cursor position using clipboard.
Uses pyperclip for full Unicode support including Turkish characters.
"""

import time
import pyperclip
import pyautogui
from typing import Optional


class TextInjector:
    """
    Injects text into the active application using clipboard.

    Features:
    - Full Unicode support (ş, ı, ğ, ö, ç, ü, etc.)
    - Clipboard backup/restore to preserve user's clipboard
    - Configurable typing delay
    - Works in any application with text input focus
    """

    # Default delay after paste (ms)
    DEFAULT_PASTE_DELAY = 100

    def __init__(self, paste_delay_ms: int = DEFAULT_PASTE_DELAY):
        """
        Initialize the text injector.

        Args:
            paste_delay_ms: Delay after Ctrl+V in milliseconds
        """
        self.paste_delay = paste_delay_ms / 1000.0  # Convert to seconds

    def inject_text(self, text: str) -> bool:
        """
        Inject text at the current cursor position using clipboard.

        Args:
            text: The text to inject

        Returns:
            True if successful, False otherwise

        Process:
        1. Backup current clipboard
        2. Copy new text to clipboard
        3. Paste with Ctrl+V
        4. Restore original clipboard
        """
        if not text:
            return False

        try:
            # Backup current clipboard
            original_clipboard = self._get_clipboard()

            # Copy new text to clipboard
            pyperclip.copy(text)

            # Small delay to ensure clipboard is ready
            time.sleep(0.05)

            # Paste using Ctrl+V
            pyautogui.hotkey("ctrl", "v")

            # Wait for paste to complete
            time.sleep(self.paste_delay)

            # Restore original clipboard
            self._restore_clipboard(original_clipboard)

            return True

        except Exception as e:
            print(f"Text injection error: {e}")
            return False

    def inject_text_direct(self, text: str, char_delay: float = 0.01) -> bool:
        """
        Inject text by simulating keystrokes (fallback method).

        Note: This method has limited Unicode support.
        Use inject_text() for full Unicode support.

        Args:
            text: The text to type
            char_delay: Delay between keystrokes in seconds

        Returns:
            True if successful, False otherwise
        """
        try:
            # Type each character
            for char in text:
                pyautogui.typewrite(char, interval=char_delay)
            return True
        except Exception as e:
            print(f"Direct type error: {e}")
            return False

    def _get_clipboard(self) -> str:
        """
        Get current clipboard content safely.

        Returns:
            Current clipboard text (empty string if unavailable)
        """
        try:
            return pyperclip.paste()
        except Exception:
            return ""

    def _restore_clipboard(self, content: str) -> None:
        """
        Restore clipboard to previous content.

        Args:
            content: The clipboard content to restore
        """
        try:
            if content:  # Only restore if there was content
                pyperclip.copy(content)
        except Exception as e:
            print(f"Clipboard restore warning: {e}")

    def test_clipboard(self) -> bool:
        """
        Test if clipboard operations are working.

        Returns:
            True if clipboard is accessible, False otherwise
        """
        try:
            test_text = "Clipboard Test - Türkçe şışğıöçÜ"
            pyperclip.copy(test_text)
            result = pyperclip.paste()
            return result == test_text
        except Exception as e:
            print(f"Clipboard test failed: {e}")
            return False


# Standalone test
def test_injector():
    """Test the text injector standalone."""
    print("Text Injector Test")
    print("=" * 40)

    injector = TextInjector()

    # Test clipboard
    print("\n1. Testing clipboard...")
    if injector.test_clipboard():
        print("✓ Clipboard is working")
    else:
        print("✗ Clipboard test failed")
        return

    # Test Unicode support
    print("\n2. Testing Unicode support...")
    test_text = "Merhaba! Türkçe karakterler: şışğıöçÜ"
    print(f"   Test text: {test_text}")

    if injector.test_clipboard():
        print("✓ Unicode clipboard working")

    # Live injection test
    print("\n3. Live Injection Test")
    print("   Instructions:")
    print("   - Open Notepad or any text editor")
    print("   - Click where you want text to appear")
    print("   - Press Enter when ready...")
    input()

    print("\n   Injecting in 3 seconds...")
    print("   (Make sure your text editor is focused!)")
    time.sleep(1)
    print("   Injecting in 2 seconds...")
    time.sleep(1)
    print("   Injecting in 1 second...")
    time.sleep(1)

    test_message = "This is a test! Türkçe: şışğıöçÜ 🎤"
    injector.inject_text(test_message)

    print(f"\n✓ Injected: {test_message}")


if __name__ == "__main__":
    test_injector()
