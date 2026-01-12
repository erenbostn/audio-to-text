"""
Settings Window - Configuration UI for GroqWhisper Desktop.
A modern dark-themed window with glass effect styling.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Optional, Callable
import sys
from pathlib import Path

# Add parent directory to path for config import
sys.path.insert(0, str(Path(__file__).parent.parent))
from config import Config


class SettingsWindow(ctk.CTk):
    """
    Main settings window for GroqWhisper Desktop.

    Features:
    - Dark theme with glass/acrylic effect
    - API key configuration
    - Microphone selection
    - Hotkey display
    - Toggle switches for preferences
    - Save configuration to .env
    """

    # Color scheme from html.md design
    ACCENT_COLOR = "#FF6B35"          # Orange for buttons/accents
    BG_COLOR = "#0c0c0c"              # Deep charcoal background
    GLASS_BG = ("gray10", "gray15")   # Semi-transparent glass
    TEXT_PRIMARY = "#ffffff"          # White
    TEXT_SECONDARY = "#a0a0a0"        # Gray
    BORDER_COLOR = ("gray20", "gray25")

    def __init__(self, config: Config = None, on_save: Callable = None, **kwargs):
        """
        Initialize the settings window.

        Args:
            config: Configuration object (creates new if None)
            on_save: Callback function when settings are saved
            **kwargs: Additional arguments for CTk
        """
        super().__init__(**kwargs)

        # Initialize config
        self._config = config if config else Config()
        self._on_save_callback = on_save

        # Window setup
        self._setup_window()

        # Create UI
        self._create_ui()

        # Load current settings
        self._load_settings()

    def _setup_window(self):
        """Configure window properties."""
        self.title("GroqWhisper Settings")
        self.geometry("520x500")

        # Center window on screen
        self._center_window()

        # Glass effect (semi-transparent)
        self.attributes("-alpha", 0.95)

        # Window icon (if available)
        try:
            self.iconbitmap("assets/icon.ico")
        except Exception:
            pass

    def _center_window(self):
        """Center the window on the screen."""
        self.update_idletasks()
        width = 520
        height = 500
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _create_ui(self):
        """Create all UI components."""
        # Main container with glass effect
        main_frame = ctk.CTkFrame(
            self,
            fg_color=self.GLASS_BG,
            corner_radius=16,
            border_color=self.BORDER_COLOR,
            border_width=1
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header section
        self._create_header(main_frame)

        # Form section
        self._create_form(main_frame)

        # Save button
        self._create_save_button(main_frame)

    def _create_header(self, parent):
        """Create window header with title and control dots."""
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(20, 20), padx=20)

        # Title label
        title = ctk.CTkLabel(
            header,
            text="GroqWhisper Settings",
            font=("Segoe UI", 18, "bold"),
            text_color=self.TEXT_PRIMARY,
            anchor="w"
        )
        title.pack(side="left", fill="x", expand=True)

        # Control dots (visual only - macOS style)
        dots_frame = ctk.CTkFrame(header, fg_color="transparent")
        dots_frame.pack(side="right")

        # Minimize dot (yellow)
        min_dot = tk.Label(
            dots_frame,
            bg="#ffbd2e",
            width=12,
            height=12,
            cursor="hand2"
        )
        min_dot.pack(side="left", padx=2)
        min_dot.bind("<Button-1>", lambda e: self.iconify())

        # Maximize dot (green)
        max_dot = tk.Label(
            dots_frame,
            bg="#27c93f",
            width=12,
            height=12,
            cursor="hand2"
        )
        max_dot.pack(side="left", padx=2)
        max_dot.bind("<Button-1>", self._toggle_maximize)

        # Close dot (red)
        close_dot = tk.Label(
            dots_frame,
            bg="#ff5f56",
            width=12,
            height=12,
            cursor="hand2"
        )
        close_dot.pack(side="left", padx=2)
        close_dot.bind("<Button-1>", lambda e: self.destroy())

    def _create_form(self, parent):
        """Create the settings form with all input fields."""
        form_frame = ctk.CTkFrame(parent, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # API Key field
        self._create_api_key_field(form_frame)

        # Microphone dropdown
        self._create_mic_dropdown(form_frame)

        # Hotkey display
        self._create_hotkey_field(form_frame)

        # Toggles section
        self._create_toggles(form_frame)

    def _create_api_key_field(self, parent):
        """Create API key input field."""
        # Label
        label = ctk.CTkLabel(
            parent,
            text="Groq API Key",
            font=("Segoe UI", 11),
            text_color=self.TEXT_SECONDARY,
            anchor="w"
        )
        label.pack(fill="x", pady=(0, 8), padx=5)

        # Input container with icon
        input_frame = ctk.CTkFrame(parent, fg_color="transparent")
        input_frame.pack(fill="x", pady=(0, 20))

        # Password entry field
        self._api_key_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="gsk_...",
            show="•",
            font=("Segoe UI", 13),
            height=45,
            corner_radius=8,
            border_color=self.BORDER_COLOR,
            fg_color=("gray15", "gray20"),
            placeholder_text_color=self.TEXT_SECONDARY
        )
        self._api_key_entry.pack(side="left", fill="x", expand=True)

        # Key icon label (visual)
        key_icon = ctk.CTkLabel(
            input_frame,
            text="🔑",
            font=("Segoe UI", 14),
            width=40
        )
        key_icon.pack(side="right", padx=(10, 0))

    def _create_mic_dropdown(self, parent):
        """Create microphone selection dropdown."""
        # Label
        label = ctk.CTkLabel(
            parent,
            text="Input Device",
            font=("Segoe UI", 11),
            text_color=self.TEXT_SECONDARY,
            anchor="w"
        )
        label.pack(fill="x", pady=(0, 8), padx=5)

        # Dropdown
        # Get available microphones
        mic_list = self._get_available_mics()

        self._mic_dropdown = ctk.CTkOptionMenu(
            parent,
            values=mic_list,
            font=("Segoe UI", 13),
            height=45,
            corner_radius=8,
            fg_color=("gray15", "gray20"),
            button_color=self.ACCENT_COLOR,
            button_hover_color="#E55A2B",
            dropdown_font=("Segoe UI", 12)
        )
        self._mic_dropdown.pack(fill="x", pady=(0, 20))

    def _create_hotkey_field(self, parent):
        """Create hotkey display field (read-only)."""
        # Label
        label = ctk.CTkLabel(
            parent,
            text="Activation Hotkey",
            font=("Segoe UI", 11),
            text_color=self.TEXT_SECONDARY,
            anchor="w"
        )
        label.pack(fill="x", pady=(0, 8), padx=5)

        # Read-only display
        input_frame = ctk.CTkFrame(parent, fg_color="transparent")
        input_frame.pack(fill="x", pady=(0, 20))

        self._hotkey_entry = ctk.CTkEntry(
            input_frame,
            font=("Segoe UI", 13),
            height=45,
            corner_radius=8,
            border_color=self.BORDER_COLOR,
            fg_color=("gray17", "gray22")
        )
        self._hotkey_entry.pack(side="left", fill="x", expand=True)
        # Set value and make read-only
        self._hotkey_entry.insert(0, "Ctrl + Alt + Space")
        self._hotkey_entry.configure(state="disabled")

        # Keyboard icon
        kb_icon = ctk.CTkLabel(
            input_frame,
            text="⌨",
            font=("Segoe UI", 14),
            width=40
        )
        kb_icon.pack(side="right", padx=(10, 0))

    def _create_toggles(self, parent):
        """Create toggle switches for preferences."""
        # Section label
        section_label = ctk.CTkLabel(
            parent,
            text="Preferences",
            font=("Segoe UI", 11),
            text_color=self.TEXT_SECONDARY,
            anchor="w"
        )
        section_label.pack(fill="x", pady=(0, 12), padx=5)

        # Beep Sound toggle
        beep_row = ctk.CTkFrame(parent, fg_color="transparent")
        beep_row.pack(fill="x", pady=(0, 12))

        beep_label = ctk.CTkLabel(
            beep_row,
            text="Play Beep Sound",
            font=("Segoe UI", 13),
            text_color=self.TEXT_PRIMARY
        )
        beep_label.pack(side="left")

        self._beep_switch = ctk.CTkSwitch(
            beep_row,
            text="",
            width=50,
            progress_color=self.ACCENT_COLOR,
            button_color=self.TEXT_PRIMARY,
            fg_color=("gray30", "gray35"),
            button_hover_color=self.TEXT_PRIMARY
        )
        self._beep_switch.pack(side="right")

        # Show Overlay toggle
        overlay_row = ctk.CTkFrame(parent, fg_color="transparent")
        overlay_row.pack(fill="x", pady=(0, 12))

        overlay_label = ctk.CTkLabel(
            overlay_row,
            text="Show Floating Overlay",
            font=("Segoe UI", 13),
            text_color=self.TEXT_PRIMARY
        )
        overlay_label.pack(side="left")

        self._overlay_switch = ctk.CTkSwitch(
            overlay_row,
            text="",
            width=50,
            progress_color=self.ACCENT_COLOR,
            button_color=self.TEXT_PRIMARY,
            fg_color=("gray30", "gray35"),
            button_hover_color=self.TEXT_PRIMARY
        )
        self._overlay_switch.pack(side="right")

    def _create_save_button(self, parent):
        """Create save configuration button."""
        btn_frame = ctk.CTkFrame(parent, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 20))

        self._save_button = ctk.CTkButton(
            btn_frame,
            text="Save Configuration",
            font=("Segoe UI", 14, "bold"),
            height=45,
            corner_radius=8,
            fg_color=self.ACCENT_COLOR,
            hover_color="#E55A2B",
            command=self._save_config
        )
        self._save_button.pack(fill="x")

    def _get_available_mics(self) -> list:
        """
        Get list of available microphones.

        Returns:
            List of microphone device names
        """
        # Try to get actual audio devices
        try:
            import sounddevice as sd
            devices = sd.query_devices()
            mics = []
            for i, device in enumerate(devices):
                if device['max_input_channels'] > 0:
                    name = device['name']
                    mics.append(f"{name}")
            return mics if mics else ["Default Microphone"]
        except Exception:
            # Fallback if sounddevice not available
            return ["Default Microphone", "External USB Mic"]

    def _load_settings(self):
        """Load current settings from config."""
        # Load API key
        api_key = self._config.get_api_key()
        if api_key:
            self._api_key_entry.insert(0, api_key)

        # Load toggle states (CTkSwitch uses select()/deselect(), not set())
        if self._config.play_beep():
            self._beep_switch.select()
        else:
            self._beep_switch.deselect()

        if self._config.show_overlay():
            self._overlay_switch.select()
        else:
            self._overlay_switch.deselect()

    def _save_config(self):
        """Save configuration to .env file."""
        # Get values from form
        api_key = self._api_key_entry.get().strip()
        play_beep = self._beep_switch.get()
        show_overlay = self._overlay_switch.get()

        # Validate API key
        if not api_key or api_key == "gsk_...":
            messagebox.showwarning(
                "Invalid API Key",
                "Please enter a valid Groq API Key.\n\nGet your key from: https://console.groq.com/keys"
            )
            return

        # Save to config
        try:
            self._config.save_api_key(api_key)

            # Update .env with toggle values (read and rewrite)
            self._save_toggle_settings(play_beep, show_overlay)

            # Show success feedback
            self._show_save_success()

            # Call callback if provided
            if self._on_save_callback:
                self._on_save_callback()

        except Exception as e:
            messagebox.showerror(
                "Save Error",
                f"Failed to save configuration:\n{str(e)}"
            )

    def _save_toggle_settings(self, play_beep: bool, show_overlay: bool):
        """Save toggle settings to .env file."""
        import os
        from dotenv import load_dotenv

        env_path = self._config.env_path
        load_dotenv(env_path)

        # Read current content
        content = ""
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                content = f.read()

        lines = content.split("\n")
        updated = False

        # Update or add PLAY_BEEP_SOUND
        for i, line in enumerate(lines):
            if line.startswith("PLAY_BEEP_SOUND="):
                lines[i] = f"PLAY_BEEP_SOUND={'true' if play_beep else 'false'}"
                updated = True
                break
        if not updated:
            lines.append(f"PLAY_BEEP_SOUND={'true' if play_beep else 'false'}")

        updated = False
        # Update or add SHOW_OVERLAY
        for i, line in enumerate(lines):
            if line.startswith("SHOW_OVERLAY="):
                lines[i] = f"SHOW_OVERLAY={'true' if show_overlay else 'false'}"
                updated = True
                break
        if not updated:
            lines.append(f"SHOW_OVERLAY={'true' if show_overlay else 'false'}")

        # Write back
        with open(env_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def _show_save_success(self):
        """Show visual feedback for successful save."""
        original_text = self._save_button.cget("text")
        original_color = self._save_button.cget("fg_color")

        self._save_button.configure(
            text="✓ Saved!",
            fg_color="#27c93f"
        )

        # Reset after 1.5 seconds
        self.after(1500, lambda: self._save_button.configure(
            text=original_text,
            fg_color=original_color
        ))

    def _toggle_maximize(self, event=None):
        """Toggle window maximized state."""
        if self.attributes('-zoomed'):
            self.attributes('-zoomed', False)
        else:
            self.attributes('-zoomed', True)


# Standalone test function
def test_settings_window():
    """Test the settings window standalone."""
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")

    # Create config
    config = Config()

    # Create window
    window = SettingsWindow(config)
    window.mainloop()


if __name__ == "__main__":
    test_settings_window()
