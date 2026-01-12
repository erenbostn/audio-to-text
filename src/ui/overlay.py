"""
Recording Overlay - Floating status widget for GroqWhisper Desktop.
A frameless, always-on-top window showing recording status with animated waveform.
"""

import tkinter as tk
import math
import customtkinter as ctk
from PIL import Image, ImageTk


class RecordingOverlay(ctk.CTkToplevel):
    """
    Floating overlay widget that displays recording status.

    Features:
    - Frameless window (no title bar)
    - Always on top
    - Rounded "pill" shape design
    - Microphone icon with pulse animation
    - Animated waveform visualization
    - Draggable (optional)
    """

    # Color scheme from html.md design
    ACCENT_COLOR = "#FF6B35"      # Orange
    DANGER_COLOR = "#ff3b30"      # Red for recording
    BG_COLOR = "#1a1a1a"          # Dark background
    TEXT_COLOR = "#ffffff"        # White text

    def __init__(self, parent=None, **kwargs):
        """
        Initialize the recording overlay.

        Args:
            parent: Parent window (optional)
            **kwargs: Additional arguments for CTkToplevel
        """
        super().__init__(parent, **kwargs)

        # Window setup for frameless, always-on-top behavior
        self._setup_window()

        # State tracking
        self._is_visible = False
        self._is_recording = False
        self._animation_running = False

        # Animation state
        self._pulse_radius = 20
        self._pulse_expanding = True
        self._waveform_phase = 0.0
        self._waveform_bars = []

        # Create UI components
        self._create_widgets()

        # Position window (top-right corner default)
        self._position_window()

        # Hide initially
        self.withdraw()

    def _setup_window(self):
        """Configure window attributes for frameless, topmost behavior."""
        # Remove window decorations (title bar, borders)
        self.overrideredirect(True)

        # Keep window always on top
        self.attributes("-topmost", True)

        # Set background color (transparent for frameless effect)
        self.configure(fg_color=self.BG_COLOR)

        # Make window background transparent
        self.wm_attributes("-transparentcolor", "")
        self.wm_attributes("-alpha", 0.95)

    def _create_widgets(self):
        """Create and layout all UI components."""
        # Main container frame with rounded corners
        self._container = ctk.CTkFrame(
            self,
            fg_color=self.BG_COLOR,
            corner_radius=25,
            border_color="#2a2a2a",
            border_width=1
        )
        self._container.pack(padx=10, pady=10, fill="both", expand=True)

        # Inner content frame (horizontal layout)
        content_frame = ctk.CTkFrame(self._container, fg_color="transparent")
        content_frame.pack(padx=15, pady=12, fill="both", expand=True)

        # Left side: Mic icon with pulse animation
        self._create_mic_section(content_frame)

        # Spacer
        ctk.CTkLabel(content_frame, text="", width=20).pack(side="left", padx=5)

        # Right side: Waveform animation
        self._create_waveform_section(content_frame)

    def _create_mic_section(self, parent):
        """Create microphone icon with pulse animation canvas."""
        mic_frame = ctk.CTkFrame(parent, fg_color="transparent")
        mic_frame.pack(side="left")

        # Canvas for mic icon and pulse animation
        self._mic_canvas = tk.Canvas(
            mic_frame,
            width=50,
            height=50,
            bg=self.BG_COLOR,
            highlightthickness=0
        )
        self._mic_canvas.pack()

        # Try to load mic icon from assets, fall back to emoji/text
        self._load_mic_icon()

        # Draw initial pulse ring (invisible)
        self._pulse_ring = self._mic_canvas.create_oval(
            15, 15, 35, 35,
            outline=self.DANGER_COLOR,
            width=2,
            state="hidden"
        )

    def _load_mic_icon(self):
        """Load microphone icon from assets or create fallback."""
        try:
            # Try loading from assets folder
            icon_path = "assets/mic_icon.png"
            pil_image = Image.open(icon_path).resize((32, 32), Image.Resampling.LANCZOS)
            self._mic_image = ImageTk.PhotoImage(pil_image)

            # Center the icon on canvas
            self._mic_canvas.create_image(
                25, 25,
                image=self._mic_image,
                tags="mic_icon"
            )
        except Exception:
            # Fallback: Draw a simple microphone using canvas shapes
            self._draw_fallback_mic()

    def _draw_fallback_mic(self):
        """Draw a simple microphone icon using canvas primitives."""
        # Mic body (oval for rounded look)
        self._mic_canvas.create_oval(
            18, 10, 32, 30,
            fill=self.TEXT_COLOR,
            outline="",
            tags="mic_icon"
        )

        # Mic stand
        self._mic_canvas.create_rectangle(
            23, 28, 27, 35,
            fill=self.TEXT_COLOR,
            outline="",
            tags="mic_icon"
        )

        # Mic base (rounded bottom)
        self._mic_canvas.create_oval(
            19, 33, 31, 39,
            fill=self.TEXT_COLOR,
            outline="",
            tags="mic_icon"
        )

    def _create_waveform_section(self, parent):
        """Create animated waveform visualization."""
        waveform_frame = ctk.CTkFrame(parent, fg_color="transparent")
        waveform_frame.pack(side="left")

        # Status text label
        self._status_label = ctk.CTkLabel(
            waveform_frame,
            text="Listening...",
            font=("Segoe UI", 13, "bold"),
            text_color=self.TEXT_COLOR,
            anchor="w"
        )
        self._status_label.pack(side="left", padx=(0, 10))

        # Waveform canvas (5 bars)
        self._waveform_canvas = tk.Canvas(
            waveform_frame,
            width=70,
            height=30,
            bg=self.BG_COLOR,
            highlightthickness=0
        )
        self._waveform_canvas.pack(side="left")

        # Create 5 waveform bars
        bar_width = 6
        bar_spacing = 8
        start_x = 5
        bar_bottom = 25

        for i in range(5):
            x = start_x + (i * (bar_width + bar_spacing))
            bar = self._waveform_canvas.create_rectangle(
                x, bar_bottom,
                x + bar_width, bar_bottom,
                fill=self.ACCENT_COLOR,
                outline=""
            )
            self._waveform_bars.append(bar)

    def _position_window(self, x=None, y=None):
        """
        Position the overlay window.

        Args:
            x: X coordinate (if None, uses screen top-right)
            y: Y coordinate (if None, uses screen top with offset)
        """
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        if x is None:
            # Default: top-right corner
            window_width = 250
            x = screen_width - window_width - 50

        if y is None:
            # Default: top with offset
            y = 80

        self.geometry(f"+{x}+{y}")

    def show(self):
        """Display the overlay window."""
        self.deiconify()
        self._is_visible = True
        self._start_animation()

    def hide(self):
        """Hide the overlay window."""
        self.withdraw()
        self._is_visible = False
        self._stop_animation()

    def set_recording_state(self, is_recording: bool):
        """
        Update the recording state and UI.

        Args:
            is_recording: True if recording is active
        """
        self._is_recording = is_recording

        # Update status text
        if is_recording:
            self._status_label.configure(text="Recording...")
            # Show pulse animation
            self._mic_canvas.itemconfigure(self._pulse_ring, state="normal")
        else:
            self._status_label.configure(text="Listening...")
            # Hide pulse animation
            self._mic_canvas.itemconfigure(self._pulse_ring, state="hidden")

    def _start_animation(self):
        """Start the animation loop."""
        if not self._animation_running:
            self._animation_running = True
            self._animate()

    def _stop_animation(self):
        """Stop the animation loop."""
        self._animation_running = False

    def _animate(self):
        """
        Main animation loop.
        Updates pulse ring and waveform bars.
        """
        if not self._animation_running:
            return

        # Animate pulse ring if recording
        if self._is_recording:
            self._animate_pulse()

        # Always animate waveform
        self._animate_waveform()

        # Schedule next frame (100ms = 10 FPS)
        self.after(100, self._animate)

    def _animate_pulse(self):
        """Animate the expanding pulse ring around the mic icon."""
        # Pulse between radius 20 and 40
        if self._pulse_expanding:
            self._pulse_radius += 1
            if self._pulse_radius >= 40:
                self._pulse_expanding = False
        else:
            self._pulse_radius -= 1
            if self._pulse_radius <= 20:
                self._pulse_expanding = True

        # Update pulse ring coordinates (centered at 25, 25)
        r = self._pulse_radius
        self._mic_canvas.coords(
            self._pulse_ring,
            25 - r, 25 - r,
            25 + r, 25 + r
        )

        # Fade out as it expands
        alpha = max(0, 1 - (r - 20) / 20)
        # Note: Tkinter doesn't support alpha on canvas items directly
        # We simulate fade by changing width
        width = max(1, int(3 * alpha))
        self._mic_canvas.itemconfigure(self._pulse_ring, width=width)

    def _animate_waveform(self):
        """Animate the waveform bars using sinusoidal motion."""
        self._waveform_phase += 0.3

        bar_bottom = 25
        base_height = 6

        for i, bar in enumerate(self._waveform_bars):
            # Each bar has a phase offset for wave effect
            phase_offset = i * 0.5
            # Sinusoidal height variation
            height_factor = (math.sin(self._waveform_phase + phase_offset) + 1) / 2
            bar_height = base_height + int(height_factor * 12)

            # Update bar coordinates
            coords = self._waveform_canvas.coords(bar)
            if coords:
                x1, y1, x2, y2 = coords
                new_y1 = bar_bottom - bar_height
                self._waveform_canvas.coords(bar, x1, new_y1, x2, bar_bottom)

    def is_visible(self) -> bool:
        """Check if overlay is currently visible."""
        return self._is_visible


# Standalone test function
def test_overlay():
    """Test the overlay window standalone."""
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    root.geometry("400x300")
    root.title("Overlay Test")

    # Create overlay
    overlay = RecordingOverlay(root)

    # Control buttons
    def toggle_overlay():
        if overlay.is_visible():
            overlay.hide()
            btn_show.configure(text="Show Overlay")
        else:
            overlay.show()
            btn_show.configure(text="Hide Overlay")

    def toggle_recording():
        is_recording = overlay._is_recording
        overlay.set_recording_state(not is_recording)
        btn_rec.configure(text="Stop Recording" if not is_recording else "Start Recording")

    btn_frame = ctk.CTkFrame(root)
    btn_frame.pack(pady=20)

    btn_show = ctk.CTkButton(btn_frame, text="Show Overlay", command=toggle_overlay)
    btn_show.pack(side="left", padx=10)

    btn_rec = ctk.CTkButton(btn_frame, text="Start Recording", command=toggle_recording)
    btn_rec.pack(side="left", padx=10)

    # Instructions
    label = ctk.CTkLabel(
        root,
        text="Click 'Show Overlay' to display the floating widget.\n"
             "Click 'Start Recording' to see pulse animation.",
        font=("Segoe UI", 12)
    )
    label.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    test_overlay()
