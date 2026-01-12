"""
Settings Window - Configuration UI for GroqWhisper Desktop.
Based on html.md glass/acrylic design - CSS values mapped to CTk.
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from typing import Callable
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import Config


class SettingsWindow(ctk.CTk):
    """
    Main settings window - CSS design from html.md.

    CSS Variables → CTk:
    --bg-color: #0c0c0c
    --glass-bg: rgba(30, 30, 30, 0.6)
    --glass-border: rgba(255, 255, 255, 0.1)
    --accent-color: #FF6B35
    --input-bg: rgba(0, 0, 0, 0.3)
    """

    # CSS :root variables
    BG_COLOR = "#0c0c0c"
    GLASS_BG = ("#2a2a2e", "#323238")  # rgba(30,30,30,0.6) approximation
    GLASS_BORDER = ("#3a3a3e", "#4a4a4e")  # rgba(255,255,255,0.1)
    ACCENT_COLOR = "#FF6B35"
    ACCENT_GLOW = ("#E55A25", "#FF6B35")  # rgba(255,107,53,0.4) glow
    TEXT_PRIMARY = "#ffffff"
    TEXT_SECONDARY = "#a0a0a0"
    INPUT_BG = ("#1a1a1a", "#222222")  # rgba(0,0,0,0.3)
    INPUT_BORDER = ("#2a2a2a", "#333333")  # rgba(255,255,255,0.1)
    DANGER_COLOR = "#ff3b30"

    def __init__(self, config: Config = None, on_save: Callable = None, on_close: Callable = None, app=None, **kwargs):
        super().__init__(**kwargs)

        self._config = config if config else Config()
        self._on_save_callback = on_save
        self._on_close_callback = on_close  # Callback when window is closed
        self._app = app  # Reference to GroqWhisperApp for recording control

        self._setup_window()
        self._create_ui()
        self._load_settings()

        # Handle window close button (X)
        self.protocol("WM_DELETE_WINDOW", self._on_window_close)

    def _setup_window(self):
        """Configure window - CSS body styling."""
        self.title("GroqWhisper Settings")
        self.geometry("450x480")

        # Deep background --bg-color: #0c0c0c
        self.configure(fg_color=self.BG_COLOR)

        # Center
        self._center_window()

    def _center_window(self):
        self.update_idletasks()
        width, height = 450, 480
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

    def _create_ui(self):
        """Glass window from CSS .glass-window"""
        # Main glass frame
        # background: rgba(30, 30, 30, 0.6)
        # border: 1px solid rgba(255, 255, 255, 0.1)
        # border-radius: 16px
        # box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6)
        glass_frame = ctk.CTkFrame(
            self,
            fg_color=self.GLASS_BG,
            corner_radius=16,
            border_color=self.GLASS_BORDER,
            border_width=1
        )
        glass_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Window header - .window-header { padding: 16px 24px }
        self._create_header(glass_frame)

        # Window body - .window-body { padding: 24px; gap: 20px }
        body_frame = ctk.CTkFrame(glass_frame, fg_color="transparent")
        body_frame.pack(fill="both", expand=True, padx=24, pady=(0, 24))

        # Form groups with gap: 20px
        self._create_api_key_field(body_frame)
        self._create_mic_dropdown(body_frame)
        self._create_hotkey_field(body_frame)
        self._create_toggles(body_frame)
        self._create_recording_button(body_frame)
        self._create_save_button(body_frame)

    def _create_header(self, parent):
        """Window header with title and dots - .window-header"""
        # Header container
        header = ctk.CTkFrame(parent, fg_color="transparent")
        header.pack(fill="x", pady=(16, 0))

        # Title - .window-title { font-size: 14px; font-weight: 500 }
        title = ctk.CTkLabel(
            header,
            text="GroqWhisper Settings",
            font=("Inter", 14, "normal"),
            text_color=self.TEXT_PRIMARY
        )
        title.pack(side="left")

        # Control dots - .control-dot { width: 12px; height: 12px }
        dots_frame = ctk.CTkFrame(header, fg_color="transparent")
        dots_frame.pack(side="right")

        # Gap: 8px between dots
        gap = 8
        dot_size = 12

        # Close - #ff5f56
        self._create_dot(dots_frame, "#ff5f56", dot_size, lambda e: self._on_window_close(), gap)
        # Minimize - #ffbd2e
        self._create_dot(dots_frame, "#ffbd2e", dot_size, lambda e: self.iconify(), gap)
        # Maximize - #27c93f
        self._create_dot(dots_frame, "#27c93f", dot_size, lambda e: self._toggle_maximize(), 0)

        # Border bottom - border-bottom: 1px solid rgba(255, 255, 255, 0.05)
        border = ctk.CTkFrame(parent, fg_color=("#1a1a1a", "#222222"), height=1)
        border.pack(fill="x", pady=(16, 0))

    def _on_window_close(self):
        """Handle window close button (X)."""
        if self._on_close_callback:
            # If running as part of GroqWhisperApp, minimize to tray
            self.withdraw()
        else:
            # If running standalone, destroy normally
            self.destroy()

    def _create_dot(self, parent, color, size, command, padx):
        """Create control dot - .control-dot"""
        frame = ctk.CTkFrame(parent, fg_color="transparent", width=size, height=size)
        if padx > 0:
            frame.pack(side="left", padx=padx)
        else:
            frame.pack(side="left")

        canvas = tk.Canvas(
            frame,
            width=size,
            height=size,
            bg="#1e1e1e",
            highlightthickness=0
        )
        canvas.pack()
        canvas.create_oval(0, 0, size, size, fill=color, outline="")
        canvas.bind("<Button-1>", command)

    def _create_api_key_field(self, parent):
        """API Key field - .form-group with .input-field"""
        # Form group - gap: 8px
        form_frame = ctk.CTkFrame(parent, fg_color="transparent")
        form_frame.pack(fill="x", pady=(0, 20))

        # Label - .form-label { font-size: 12px; color: var(--text-secondary) }
        label = ctk.CTkLabel(
            form_frame,
            text="Groq API Key",
            font=("Inter", 12, "normal"),
            text_color=self.TEXT_SECONDARY,
            anchor="w"
        )
        label.pack(fill="x", pady=(0, 8))

        # Input wrapper
        input_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        input_frame.pack(fill="x")

        # Input field - CSS: background: var(--input-bg), border: 1px solid rgba(255,255,255,0.1)
        self._api_key_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="gsk_...",
            show="•",
            font=("Inter", 14, "normal"),
            height=45,  # padding: 12px 16px ≈ 45px
            corner_radius=8,
            border_color=self.INPUT_BORDER,
            border_width=1,
            fg_color=self.INPUT_BG,
            placeholder_text_color=self.TEXT_SECONDARY,
            text_color=self.TEXT_PRIMARY
        )
        self._api_key_entry.pack(side="left", fill="x", expand=True)

        # Icon - .input-icon { right: 12px; font-size: 18px }
        icon = ctk.CTkLabel(
            input_frame,
            text="🔑",
            font=("Segoe UI", 16),
            width=30
        )
        icon.pack(side="right", padx=(8, 0))

    def _create_mic_dropdown(self, parent):
        """Microphone dropdown"""
        form_frame = ctk.CTkFrame(parent, fg_color="transparent")
        form_frame.pack(fill="x", pady=(0, 20))

        label = ctk.CTkLabel(
            form_frame,
            text="Input Device",
            font=("Inter", 12, "normal"),
            text_color=self.TEXT_SECONDARY,
            anchor="w"
        )
        label.pack(fill="x", pady=(0, 8))

        mic_list = self._get_available_mics()
        self._mic_dropdown = ctk.CTkOptionMenu(
            form_frame,
            values=mic_list,
            font=("Inter", 14, "normal"),
            height=45,
            corner_radius=8,
            fg_color=self.INPUT_BG,
            button_color=self.ACCENT_COLOR,
            button_hover_color=self.ACCENT_GLOW,
            dropdown_font=("Inter", 13),
            dropdown_fg_color=self.GLASS_BG,
            dropdown_hover_color=self.ACCENT_COLOR,
            dropdown_text_color=self.TEXT_PRIMARY,
            text_color=self.TEXT_PRIMARY,
            anchor="w"
        )
        self._mic_dropdown.pack(fill="x")

    def _create_hotkey_field(self, parent):
        """Hotkey display - read-only"""
        form_frame = ctk.CTkFrame(parent, fg_color="transparent")
        form_frame.pack(fill="x", pady=(0, 20))

        label = ctk.CTkLabel(
            form_frame,
            text="Activation Hotkey",
            font=("Inter", 12, "normal"),
            text_color=self.TEXT_SECONDARY,
            anchor="w"
        )
        label.pack(fill="x", pady=(0, 8))

        input_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        input_frame.pack(fill="x")

        self._hotkey_entry = ctk.CTkEntry(
            input_frame,
            font=("Inter", 14, "normal"),
            height=45,
            corner_radius=8,
            border_color=self.INPUT_BORDER,
            border_width=1,
            fg_color=self.INPUT_BG,
            text_color="#666666"
        )
        self._hotkey_entry.pack(side="left", fill="x", expand=True)
        self._hotkey_entry.insert(0, "Ctrl + Alt + Space")
        self._hotkey_entry.configure(state="disabled")

        icon = ctk.CTkLabel(
            input_frame,
            text="⌨",
            font=("Segoe UI", 16),
            width=30
        )
        icon.pack(side="right", padx=(8, 0))

    def _create_toggles(self, parent):
        """Toggle switches - .toggle-switch CSS"""
        form_frame = ctk.CTkFrame(parent, fg_color="transparent")
        form_frame.pack(fill="x", pady=(0, 20))

        # Section label
        label = ctk.CTkLabel(
            form_frame,
            text="Preferences",
            font=("Inter", 12, "normal"),
            text_color=self.TEXT_SECONDARY,
            anchor="w"
        )
        label.pack(fill="x", pady=(0, 8))

        # Beep Sound - .settings-row
        beep_row = ctk.CTkFrame(form_frame, fg_color="transparent")
        beep_row.pack(fill="x", pady=(8, 0))

        beep_label = ctk.CTkLabel(
            beep_row,
            text="Play Beep Sound",
            font=("Inter", 14, "normal"),
            text_color=self.TEXT_PRIMARY
        )
        beep_label.pack(side="left")

        # Toggle - width: 44px, height: 24px, background: rgba(255,255,255,0.1)
        self._beep_switch = ctk.CTkSwitch(
            beep_row,
            text="",
            width=44,
            height=24,
            progress_color=self.ACCENT_COLOR,
            button_color=self.TEXT_PRIMARY,
            button_hover_color=self.TEXT_PRIMARY,
            fg_color=("#333333", "#404040"),  # rgba(255,255,255,0.1)
            corner_radius=12,
            switch_width=44,
            switch_height=24
        )
        self._beep_switch.pack(side="right")

        # Show Overlay
        overlay_row = ctk.CTkFrame(form_frame, fg_color="transparent")
        overlay_row.pack(fill="x", pady=(8, 0))

        overlay_label = ctk.CTkLabel(
            overlay_row,
            text="Show Floating Overlay",
            font=("Inter", 14, "normal"),
            text_color=self.TEXT_PRIMARY
        )
        overlay_label.pack(side="left")

        self._overlay_switch = ctk.CTkSwitch(
            overlay_row,
            text="",
            width=44,
            height=24,
            progress_color=self.ACCENT_COLOR,
            button_color=self.TEXT_PRIMARY,
            button_hover_color=self.TEXT_PRIMARY,
            fg_color=("#333333", "#404040"),
            corner_radius=12,
            switch_width=44,
            switch_height=24
        )
        self._overlay_switch.pack(side="right")

    def _create_recording_button(self, parent):
        """Create prominent recording button."""
        # Recording button container
        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
        button_frame.pack(fill="x", pady=(20, 10))

        # Recording button - large and prominent
        self._record_button = ctk.CTkButton(
            button_frame,
            text="🎙 START RECORDING",
            font=("Inter", 16, "bold"),
            height=60,
            corner_radius=12,
            fg_color=self.ACCENT_COLOR,
            hover_color=self.ACCENT_GLOW,
            text_color=self.TEXT_PRIMARY,
            command=self._toggle_recording
        )
        self._record_button.pack(fill="x")

        # Hotkey hint
        hint_label = ctk.CTkLabel(
            button_frame,
            text="or press Ctrl+Alt+K",
            font=("Inter", 11),
            text_color=self.TEXT_SECONDARY
        )
        hint_label.pack(pady=(5, 0))

    def _create_save_button(self, parent):
        """Save button - .btn-save CSS"""
        # background: var(--accent-color)
        # box-shadow: 0 4px 15px rgba(255, 107, 53, 0.4)
        # padding: 14px, border-radius: 8px
        self._save_button = ctk.CTkButton(
            parent,
            text="Save Configuration",
            font=("Inter", 14, "bold"),
            height=48,  # padding: 14px top/bottom
            corner_radius=8,
            fg_color=self.ACCENT_COLOR,
            hover_color=self.ACCENT_GLOW,
            text_color=self.TEXT_PRIMARY,
            border_width=0
        )
        self._save_button.pack(fill="x", pady=(8, 0))

    def _get_available_mics(self) -> list:
        try:
            import sounddevice as sd
            devices = sd.query_devices()
            mics = []
            for device in devices:
                if device['max_input_channels'] > 0:
                    mics.append(device['name'])
            return mics if mics else ["Default Microphone"]
        except Exception:
            return ["Default Microphone"]

    def _load_settings(self):
        api_key = self._config.get_api_key()
        if api_key:
            self._api_key_entry.insert(0, api_key)

        if self._config.play_beep():
            self._beep_switch.select()
        else:
            self._beep_switch.deselect()

        if self._config.show_overlay():
            self._overlay_switch.select()
        else:
            self._overlay_switch.deselect()

    def _save_config(self):
        api_key = self._api_key_entry.get().strip()
        play_beep = self._beep_switch.get()
        show_overlay = self._overlay_switch.get()

        if not api_key or api_key == "gsk_...":
            messagebox.showwarning(
                "Invalid API Key",
                "Please enter a valid Groq API Key.\n\nGet your key from: https://console.groq.com/keys"
            )
            return

        try:
            self._config.save_api_key(api_key)
            self._save_toggle_settings(play_beep, show_overlay)
            self._show_save_success()

            if self._on_save_callback:
                self._on_save_callback()

        except Exception as e:
            messagebox.showerror(
                "Save Error",
                f"Failed to save configuration:\n{str(e)}"
            )

    def _save_toggle_settings(self, play_beep: bool, show_overlay: bool):
        import os
        from dotenv import load_dotenv

        env_path = self._config.env_path
        load_dotenv(env_path)

        content = ""
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                content = f.read()

        lines = content.split("\n")

        for i, line in enumerate(lines):
            if line.startswith("PLAY_BEEP_SOUND="):
                lines[i] = f"PLAY_BEEP_SOUND={'true' if play_beep else 'false'}"
                break
        else:
            lines.append(f"PLAY_BEEP_SOUND={'true' if play_beep else 'false'}")

        for i, line in enumerate(lines):
            if line.startswith("SHOW_OVERLAY="):
                lines[i] = f"SHOW_OVERLAY={'true' if show_overlay else 'false'}"
                break
        else:
            lines.append(f"SHOW_OVERLAY={'true' if show_overlay else 'false'}")

        with open(env_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

    def _show_save_success(self):
        original_text = self._save_button.cget("text")
        original_color = self._save_button.cget("fg_color")

        self._save_button.configure(
            text="✓ Saved!",
            fg_color="#27c93f"
        )

        self.after(1500, lambda: self._save_button.configure(
            text=original_text,
            fg_color=original_color
        ))

    def _toggle_maximize(self, event=None):
        if self.attributes('-zoomed'):
            self.attributes('-zoomed', False)
        else:
            self.attributes('-zoomed', True)

    def _toggle_recording(self) -> None:
        """Toggle recording state when button is pressed."""
        if self._app:
            self._app._on_hotkey_pressed()
            self._update_recording_button()

    def _update_recording_button(self) -> None:
        """Update recording button text and color based on recording state."""
        if self._app and hasattr(self._app, '_is_recording'):
            if self._app._is_recording:
                self._record_button.configure(
                    text="⏹ STOP RECORDING",
                    fg_color="#ff3b30"  # Red when recording
                )
            else:
                self._record_button.configure(
                    text="🎙 START RECORDING",
                    fg_color=self.ACCENT_COLOR
                )


def test_settings_window():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")

    config = Config()
    window = SettingsWindow(config)
    window.mainloop()


if __name__ == "__main__":
    test_settings_window()
