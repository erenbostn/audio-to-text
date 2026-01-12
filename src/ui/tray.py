"""
System Tray Module - Background application management using pystray.
Provides tray icon with menu for restore/quit actions.
"""

import threading
import ctypes
import time
from typing import Callable

import pystray
from PIL import Image, ImageDraw


def _force_show_tray_icon():
    """Try to force Windows to show the tray icon by simulating a click."""
    try:
        # Windows shell DLL to interact with notification area
        shell32 = ctypes.windll.shell32
        # Try to refresh notification area (Windows 10+)
        try:
            shell32.SHChangeNotify(0x0800, 0x1000, None, None)
        except:
            pass
    except:
        pass


class SystemTray:
    """
    System tray integration using pystray.

    Features:
    - Tray icon with menu (Restore Settings, Quit)
    - Runs in daemon thread (non-blocking)
    - Thread-safe callbacks to main application
    - Fallback icon generation if asset not found
    """

    def __init__(self, on_restore: Callable, on_quit: Callable):
        """
        Initialize system tray.

        Args:
            on_restore: Callback when "Restore Settings" menu item clicked
            on_quit: Callback when "Quit" menu item clicked
        """
        self._on_restore = on_restore
        self._on_quit = on_quit
        self._icon = None
        self._thread = None

    def run(self) -> None:
        """
        Start the tray icon in a separate thread.

        Non-blocking - returns immediately after starting thread.
        """
        try:
            icon = self._create_icon()
            menu = pystray.Menu(
                pystray.MenuItem("Restore Settings", self._on_restore),
                pystray.MenuItem("Quit", self._on_quit)
            )
            self._icon = pystray.Icon("groqwhisper", icon, "GroqWhisper", menu)
            # Use daemon=True so it doesn't block shutdown
            self._thread = threading.Thread(target=self._icon.run, daemon=True)
            self._thread.start()
            print("System tray icon started.")

            # Force Windows to show the icon
            _force_show_tray_icon()

        except Exception as e:
            print(f"Warning: Could not start system tray icon: {e}")

    def stop(self) -> None:
        """
        Stop the tray icon gracefully.

        Called during application shutdown.
        """
        if self._icon:
            self._icon.stop()

    def update_tooltip(self, text: str) -> None:
        """
        Update the tray icon tooltip text.

        Args:
            text: New tooltip text
        """
        if self._icon:
            self._icon.title = text

    def _create_icon(self) -> Image.Image:
        """
        Create tray icon programmatically.

        Returns a simple microphone icon with orange accent.
        Size: 64x64 pixels (standard tray size).

        Returns:
            PIL Image object for tray icon
        """
        # Create image with dark background
        img = Image.new('RGB', (64, 64), color='#2a2a2e')
        draw = ImageDraw.Draw(img)

        # Draw microphone icon
        # Main body (ellipse)
        draw.ellipse([24, 20, 40, 44], fill='#FF6B35')

        # Stand (rectangle)
        draw.rectangle([30, 44, 34, 48], fill='#FF6B35')

        # Base (rounded rectangle approximation)
        draw.ellipse([26, 48, 38, 52], fill='#FF6B35')

        return img


def test_tray():
    """Test the system tray standalone."""

    def on_restore():
        print("Restore clicked!")

    def on_quit():
        print("Quit clicked!")
        import sys
        sys.exit(0)

    tray = SystemTray(on_restore, on_quit)
    tray.run()

    print("Tray icon running. Press Ctrl+C to exit...")
    try:
        import time
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        tray.stop()


if __name__ == "__main__":
    test_tray()
