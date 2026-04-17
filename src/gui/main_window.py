"""Main GUI window for YouTube downloader."""

import threading
import webbrowser
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext
import customtkinter as ctk

from ..core.config import ConfigManager
from ..core.downloader import DownloadManager
from ..core.errors import (
    FFmpegError,
    GeoRestrictedError,
    InvalidURLError,
    NetworkError,
    YouTubeDownloaderError,
    YouTubeError,
)
from ..core.validators import is_valid_youtube_url, validate_output_directory

# UI Configuration Constants
WINDOW_TITLE = "YouTube MP4 Downloader"
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 600
DEFAULT_PADDING = 15
SECTION_PADDING = 15
SMALL_PADDING = 5

# Font Constants
FONT_TITLE = ("Arial", 18, "bold")
FONT_HEADING = ("Arial", 11, "bold")
FONT_DEFAULT = ("Arial", 10)
FONT_SMALL = ("Arial", 9)
FONT_MONO = ("Courier", 9)

# Color Constants
COLOR_TEXT_GRAY = "gray"
COLOR_SUCCESS = "green"
COLOR_ERROR = "red"
COLOR_INFO = "white"

# Messages and Help Text
GITHUB_REPO = "https://github.com/seansyao/YouTubeDownloader"
MSG_LEGAL_DISCLAIMER = (
    "⚠️ Only download content you own or have permission to download.\n"
    "Respect copyright laws and YouTube's Terms of Service."
)
MSG_ENTER_URL = "Please enter a YouTube URL"
MSG_INVALID_URL_HELP = (
    "Please enter a valid YouTube URL:\n"
    "  • https://www.youtube.com/watch?v=VIDEO_ID\n"
    "  • https://youtu.be/VIDEO_ID"
)
MSG_FFMPEG_MISSING = "FFmpeg must be installed. Windows: choco install ffmpeg"

# UI Status Messages
STATUS_READY = "Ready"
STATUS_FETCHING = "Fetching video info..."
STATUS_DOWNLOADING = "Downloading..."
STATUS_MERGING = "Merging audio & video..."
STATUS_COMPLETE = "Complete!"
STATUS_ERROR = "Error"
STATUS_GEO_RESTRICTED = "Geo-Restricted"
STATUS_FFMPEG_ERROR = "FFmpeg Error"
STATUS_NETWORK_ERROR = "Network Error"
STATUS_DOWNLOAD_FAILED = "Download Failed"


class MainWindow(ctk.CTk):
    """Main application window."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        self.title(WINDOW_TITLE)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.resizable(True, True)
        
        # Configuration
        self.config_manager = ConfigManager()
        self.current_output_dir = self.config_manager.get_output_dir()
        self.download_manager = None
        self.download_thread = None
        self._is_downloading = False
        self.available_qualities = {}  # Maps quality name to format_id
        
        # Theme setup
        ctk.set_appearance_mode(self.config_manager.get_theme())
        ctk.set_default_color_theme("blue")
        
        self._build_ui()

    def _build_ui(self):
        """Construct the complete UI layout."""
        # Create menu bar
        self._build_menu_bar()
        
        # Main container
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=DEFAULT_PADDING, pady=DEFAULT_PADDING)
        
        # Build each UI section
        self._build_title_section(main_frame)
        self._build_url_input_section(main_frame)
        self._build_quality_section(main_frame)
        self._build_output_dir_section(main_frame)
        self._build_download_section(main_frame)
        self._build_progress_section(main_frame)
        self._build_log_section(main_frame)
        self._build_footer_section(main_frame)

    def _build_menu_bar(self):
        """Build menu bar with Help options."""
        import tkinter as tk
        
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="Getting Started", command=self._show_getting_started)
        help_menu.add_command(label="User Manual", command=self._show_user_manual)
        help_menu.add_separator()
        help_menu.add_command(label="GitHub Repository", command=self._open_github)
        help_menu.add_separator()
        help_menu.add_command(label="About", command=self._show_about)

    def _build_title_section(self, parent: ctk.CTkFrame):
        """Build title and disclaimer section."""
        title = ctk.CTkLabel(parent, text=WINDOW_TITLE, font=FONT_TITLE)
        title.pack(pady=(0, SMALL_PADDING))
        
        disclaimer = ctk.CTkLabel(
            parent,
            text=MSG_LEGAL_DISCLAIMER,
            font=FONT_SMALL,
            text_color=COLOR_TEXT_GRAY,
        )
        disclaimer.pack(pady=(0, SECTION_PADDING))

    def _build_url_input_section(self, parent: ctk.CTkFrame):
        """Build URL input section."""
        url_label = ctk.CTkLabel(parent, text="YouTube URL:", font=FONT_HEADING)
        url_label.pack(anchor="w", pady=(0, SMALL_PADDING))
        
        self.url_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Paste YouTube URL here (e.g., https://www.youtube.com/watch?v=...)",
        )
        self.url_entry.pack(fill="x", pady=(0, SMALL_PADDING))
        self.url_entry.bind("<Return>", lambda e: self._on_fetch_video_info())
        
        fetch_btn = ctk.CTkButton(
            parent,
            text="Load Video Info & Qualities",
            font=FONT_DEFAULT,
            height=28,
            command=self._on_fetch_video_info,
        )
        fetch_btn.pack(fill="x", pady=(0, SECTION_PADDING))

    def _build_quality_section(self, parent: ctk.CTkFrame):
        """Build quality selection section."""
        quality_frame = ctk.CTkFrame(parent)
        quality_frame.pack(fill="x", pady=(0, SECTION_PADDING))
        
        quality_label = ctk.CTkLabel(
            quality_frame, 
            text="Available Qualities (Info Only):", 
            font=FONT_HEADING
        )
        quality_label.pack(anchor="w", pady=(0, SMALL_PADDING))
        
        self.quality_var = ctk.StringVar(value="Best (Auto)")
        self.quality_dropdown = ctk.CTkComboBox(
            quality_frame,
            variable=self.quality_var,
            values=["Best (Auto)"],
            state="normal",
            font=FONT_DEFAULT,
        )
        self.quality_dropdown.pack(fill="x")

    def _build_output_dir_section(self, parent: ctk.CTkFrame):
        """Build output directory selection section."""
        dir_frame = ctk.CTkFrame(parent)
        dir_frame.pack(fill="x", pady=(0, SECTION_PADDING))
        
        dir_label = ctk.CTkLabel(dir_frame, text="Save to:", font=FONT_HEADING)
        dir_label.pack(anchor="w", pady=(0, SMALL_PADDING))
        
        dir_input_frame = ctk.CTkFrame(dir_frame)
        dir_input_frame.pack(fill="x")
        
        self.dir_entry = ctk.CTkEntry(dir_input_frame, state="readonly")
        self.dir_entry.pack(side="left", fill="x", expand=True, padx=(0, SMALL_PADDING))
        self._update_dir_display()
        
        browse_btn = ctk.CTkButton(
            dir_input_frame,
            text="Browse",
            width=80,
            command=self._on_browse_clicked,
        )
        browse_btn.pack(side="right")

    def _build_download_section(self, parent: ctk.CTkFrame):
        """Build download button section."""
        self.download_btn = ctk.CTkButton(
            parent,
            text="Download",
            font=("Arial", 12, "bold"),
            command=self._on_download_clicked,
            height=40,
        )
        self.download_btn.pack(fill="x", pady=(0, SECTION_PADDING))

    def _build_progress_section(self, parent: ctk.CTkFrame):
        """Build progress bar and status section."""
        self.progress_bar = ctk.CTkProgressBar(parent)
        self.progress_bar.pack(fill="x", pady=(0, SMALL_PADDING))
        self.progress_bar.set(0)
        
        self.status_label = ctk.CTkLabel(
            parent,
            text=STATUS_READY,
            text_color=COLOR_TEXT_GRAY,
            font=FONT_DEFAULT,
        )
        self.status_label.pack(anchor="w", pady=(0, SECTION_PADDING))

    def _build_log_section(self, parent: ctk.CTkFrame):
        """Build log display section."""
        log_label = ctk.CTkLabel(parent, text="Log:", font=FONT_HEADING)
        log_label.pack(anchor="w", pady=(0, SMALL_PADDING))
        
        self.log_display = scrolledtext.ScrolledText(
            parent,
            height=10,
            font=FONT_MONO,
            state="disabled",
        )
        self.log_display.pack(fill="both", expand=True)

    def _build_footer_section(self, parent: ctk.CTkFrame):
        """Build footer section."""
        footer_frame = ctk.CTkFrame(parent)
        footer_frame.pack(fill="x", pady=(SECTION_PADDING, 0))
        
        footer_text = ctk.CTkLabel(
            footer_frame,
            text=MSG_FFMPEG_MISSING,
            font=FONT_SMALL,
            text_color=COLOR_TEXT_GRAY,
        )
        footer_text.pack()

    def _update_dir_display(self):
        """Update directory display field."""
        self.dir_entry.configure(state="normal")
        self.dir_entry.delete(0, "end")
        self.dir_entry.insert(0, str(self.current_output_dir))
        self.dir_entry.configure(state="readonly")

    def _on_browse_clicked(self):
        """Handle Browse button click."""
        folder = filedialog.askdirectory(initialdir=str(self.current_output_dir))
        if folder:
            self.current_output_dir = Path(folder)
            self._update_dir_display()

    def _on_fetch_video_info(self):
        """Fetch video info and populate quality dropdown."""
        url = self.url_entry.get().strip()
        
        if not self._validate_url(url):
            return
        
        # Start fetching in background thread
        self.download_btn.configure(state="disabled")
        self.quality_dropdown.configure(state="disabled")
        self._update_status(STATUS_FETCHING)
        
        fetch_thread = threading.Thread(
            target=self._fetch_info_worker,
            args=(url,),
            daemon=True,
        )
        fetch_thread.start()

    def _validate_url(self, url: str) -> bool:
        """
        Validate YouTube URL.
        
        Args:
            url: URL to validate.
            
        Returns:
            True if valid, False otherwise (shows error dialog).
        """
        if not url:
            messagebox.showerror("Error", MSG_ENTER_URL)
            return False
        
        if not is_valid_youtube_url(url):
            messagebox.showerror("Invalid URL", MSG_INVALID_URL_HELP)
            return False
        
        return True

    def _fetch_info_worker(self, url: str):
        """
        Fetch video info in background thread.
        
        Args:
            url: YouTube video URL.
        """
        try:
            self._log(f"Fetching info for: {url}")
            self.download_manager = DownloadManager(self.current_output_dir)
            info = self.download_manager.fetch_video_info(url)
            
            self._log_video_info(info)
            
            # Store qualities and update UI
            self.available_qualities = info.get("qualities", {"Best (Auto)": "best"})
            self.after(0, self._update_quality_dropdown)
            self.after(
                0, 
                lambda: self._update_status(f"Ready to download: {info['title']}")
            )
        
        except YouTubeDownloaderError as e:
            self._log(f"✗ Error fetching video: {e}")
            self.after(
                0, 
                lambda: messagebox.showerror("Error", f"Could not fetch video info:\n{e}")
            )
            self.after(0, lambda: self._update_status(STATUS_ERROR, COLOR_ERROR))
        
        finally:
            self.after(0, lambda: self.download_btn.configure(state="normal"))
            self.after(0, lambda: self.quality_dropdown.configure(state="normal"))

    def _log_video_info(self, info: dict):
        """
        Log video information to UI.
        
        Args:
            info: Video info dict from download manager.
        """
        title = info.get("title", "Unknown")
        duration = info.get("duration", 0)
        duration_str = self._format_duration(duration)
        uploader = info.get("uploader", "Unknown")
        resolutions = ", ".join(
            k for k in self.available_qualities.keys() 
            if k != "Best (Auto)"
        )
        
        self._log(f"✓ Title: {title}")
        self._log(f"  Duration: {duration_str}")
        self._log(f"  Uploader: {uploader}")
        self._log(f"  Available resolutions: {resolutions}")
        self._log("  Note: Downloads use yt-dlp's best format for maximum compatibility")

    def _update_quality_dropdown(self):
        """Update quality dropdown with available options."""
        if not self.available_qualities:
            self.available_qualities = {"Best (Auto)": "best"}
        
        quality_names = list(self.available_qualities.keys())
        self.quality_dropdown.configure(values=quality_names)
        
        # Select "Best (Auto)" by default
        if "Best (Auto)" in quality_names:
            self.quality_var.set("Best (Auto)")
        elif quality_names:
            self.quality_var.set(quality_names[0])
        
        self.quality_dropdown.configure(state="normal")

    def _on_download_clicked(self):
        """Handle Download button click."""
        url = self.url_entry.get().strip()
        
        # Validate inputs
        if not self._validate_url(url):
            return
        
        if not self._validate_output_dir():
            return
        
        # Get selected quality and start download
        selected_quality = self.quality_var.get()
        format_id = self.available_qualities.get(selected_quality, "bestvideo+bestaudio/best")
        
        self._start_download(url, format_id)

    def _validate_output_dir(self) -> bool:
        """
        Validate output directory.
        
        Returns:
            True if valid, False otherwise (shows error dialog).
        """
        try:
            validate_output_directory(self.current_output_dir)
            return True
        except ValueError as e:
            messagebox.showerror("Invalid Directory", str(e))
            return False

    def _start_download(self, url: str, format_id: str):
        """
        Start download in background thread.
        
        Args:
            url: YouTube URL to download.
            format_id: Format ID to use for download.
        """
        self._is_downloading = True
        self.download_btn.configure(state="disabled")
        self.url_entry.configure(state="disabled")
        self.quality_dropdown.configure(state="disabled")
        
        self.download_thread = threading.Thread(
            target=self._download_worker,
            args=(url, format_id),
            daemon=True,
        )
        self.download_thread.start()

    def _download_worker(self, url: str, format_id: str = None):
        """
        Download worker thread (runs in background).
        
        Args:
            url: YouTube URL to download.
            format_id: Specific format ID to use.
        """
        try:
            self._log("Initializing download manager...")
            if not self.download_manager:
                self.download_manager = DownloadManager(self.current_output_dir)
            
            self._log("Starting download...")
            self._update_status(STATUS_DOWNLOADING)
            
            # Download with progress callback
            output_file = self.download_manager.download(url, self._on_progress, format_id)
            
            self._log(f"✓ Download complete!")
            self._log(f"Saved to: {output_file}")
            self._update_status(STATUS_COMPLETE, COLOR_SUCCESS)
            
            # Show completion dialog
            self.after(
                0,
                lambda: messagebox.showinfo(
                    "Success",
                    f"Video downloaded successfully!\n\nSaved to:\n{output_file}",
                ),
            )
        
        except FFmpegError as e:
            self._handle_ffmpeg_error(e)
        except GeoRestrictedError as e:
            self._handle_geo_restricted_error(e)
        except NetworkError as e:
            self._handle_network_error(e)
        except YouTubeError as e:
            self._handle_youtube_error(e)
        except Exception as e:
            self._handle_unexpected_error(e)
        
        finally:
            self._is_downloading = False
            self.after(0, self._reset_ui)

    def _handle_ffmpeg_error(self, e: FFmpegError):
        """Handle FFmpeg errors."""
        self._log(f"✗ FFmpeg Error: {e}")
        self._update_status(STATUS_FFMPEG_ERROR, COLOR_ERROR)
        self.after(
            0,
            lambda: messagebox.showerror(
                "FFmpeg Missing",
                f"{e}\n\nPlease install FFmpeg and try again.",
            ),
        )

    def _handle_geo_restricted_error(self, e: GeoRestrictedError):
        """Handle geo-restriction errors."""
        self._log(f"✗ Geo-Restricted: {e}")
        self._update_status(STATUS_GEO_RESTRICTED, COLOR_ERROR)
        self.after(
            0,
            lambda: messagebox.showerror("Not Available", str(e)),
        )

    def _handle_network_error(self, e: NetworkError):
        """Handle network errors."""
        self._log(f"✗ Network Error: {e}")
        self._update_status(STATUS_NETWORK_ERROR, COLOR_ERROR)
        self.after(
            0,
            lambda: messagebox.showerror(
                "Network Error",
                f"{e}\n\nPlease check your connection and try again.",
            ),
        )

    def _handle_youtube_error(self, e: YouTubeError):
        """Handle YouTube API errors."""
        self._log(f"✗ Download Error: {e}")
        self._update_status(STATUS_DOWNLOAD_FAILED, COLOR_ERROR)
        self.after(
            0,
            lambda: messagebox.showerror("Download Failed", str(e)),
        )

    def _handle_unexpected_error(self, e: Exception):
        """Handle unexpected errors."""
        self._log(f"✗ Unexpected Error: {e}")
        self._update_status(STATUS_ERROR, COLOR_ERROR)
        self.after(
            0,
            lambda: messagebox.showerror(
                "Unexpected Error", 
                f"{type(e).__name__}: {e}"
            ),
        )

    def _on_progress(self, progress: dict):
        """
        Handle progress updates from download manager.
        
        Args:
            progress: Progress dict with status and metrics.
        """
        status = progress.get("status")
        
        if status == "downloading":
            self._handle_downloading_progress(progress)
        elif status == "merging":
            self.after(0, self._update_status, STATUS_MERGING)
            self.after(0, self.progress_bar.set, 0.95)
        elif status == "error":
            message = progress.get("message", "Unknown error")
            self._log(f"Progress error: {message}")

    def _handle_downloading_progress(self, progress: dict):
        """
        Update UI with download progress.
        
        Args:
            progress: Progress dict with download metrics.
        """
        downloaded = progress.get("downloaded", 0)
        total = progress.get("total", 0)
        speed = progress.get("speed")
        
        # Update progress bar
        if total > 0:
            fraction = downloaded / total
            self.after(0, self.progress_bar.set, fraction)
        
        # Update status text
        downloaded_mb = downloaded / (1024 ** 2)
        total_mb = total / (1024 ** 2)
        speed_str = self._format_speed(speed) if speed else "?"
        status_text = f"Downloading: {downloaded_mb:.1f}MB / {total_mb:.1f}MB @ {speed_str}"
        self.after(0, self._update_status, status_text)

    def _reset_ui(self):
        """Reset UI controls after download completes."""
        self.download_btn.configure(state="normal")
        self.url_entry.configure(state="normal")
        self.quality_dropdown.configure(state="normal")
        self.progress_bar.set(0)

    def _update_dir_display(self):
        """Update directory display field."""
        self.dir_entry.configure(state="normal")
        self.dir_entry.delete(0, "end")
        self.dir_entry.insert(0, str(self.current_output_dir))
        self.dir_entry.configure(state="readonly")

    def _on_browse_clicked(self):
        """Handle Browse button click."""
        folder = filedialog.askdirectory(initialdir=str(self.current_output_dir))
        if folder:
            self.current_output_dir = Path(folder)
            self._update_dir_display()

    def _update_quality_dropdown(self):
        """Update quality dropdown with available options."""
        if not self.available_qualities:
            self.available_qualities = {"Best (Auto)": "best"}
        
        quality_names = list(self.available_qualities.keys())
        self.quality_dropdown.configure(values=quality_names)
        
        # Select "Best (Auto)" by default
        if "Best (Auto)" in quality_names:
            self.quality_var.set("Best (Auto)")
        elif quality_names:
            self.quality_var.set(quality_names[0])
        
        self.quality_dropdown.configure(state="normal")

    def _update_status(self, message: str, color: str = COLOR_INFO):
        """Update status label."""
        self.status_label.configure(text=message, text_color=color)

    def _log(self, message: str):
        """Append message to log display."""
        self.log_display.configure(state="normal")
        self.log_display.insert("end", message + "\n")
        self.log_display.see("end")
        self.log_display.configure(state="disabled")

    @staticmethod
    def _format_duration(seconds: int) -> str:
        """
        Format duration in seconds to human-readable format.
        
        Args:
            seconds: Duration in seconds.
            
        Returns:
            Formatted string like "1h 30m 45s" or "45m 30s".
        """
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m {secs}s"
        return f"{minutes}m {secs}s"

    @staticmethod
    def _format_speed(speed: float) -> str:
        """
        Format download speed in human-readable format.
        
        Args:
            speed: Speed in bytes per second.
            
        Returns:
            Formatted string like "5.2MB/s".
        """
        if speed is None:
            return "?"
        mb_per_sec = speed / (1024 ** 2)
        return f"{mb_per_sec:.1f}MB/s"

    def _show_getting_started(self):
        """Show Getting Started help dialog."""
        self._show_help_dialog(
            "Getting Started",
            "README.md",
            "Installation & Project Information"
        )

    def _show_user_manual(self):
        """Show User Manual help dialog."""
        self._show_help_dialog(
            "User Manual",
            "MANUAL.md",
            "How to Use the Application"
        )

    def _show_help_dialog(self, title: str, filename: str, description: str):
        """
        Show help dialog with file content.
        
        Args:
            title: Dialog title.
            filename: Name of markdown file to load.
            description: File description.
        """
        import tkinter as tk
        
        # Try to load the markdown file
        filepath = Path(__file__).parent.parent.parent / filename
        
        if not filepath.exists():
            messagebox.showwarning(
                title,
                f"Could not find {filename}\n\nPlease check that documentation files are installed."
            )
            return
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror(title, f"Error reading {filename}:\n{e}")
            return
        
        # Create dialog window
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry("800x600")
        
        # Header frame
        header_frame = tk.Frame(dialog)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        header_label = tk.Label(
            header_frame,
            text=description,
            font=("Arial", 12, "bold")
        )
        header_label.pack(anchor="w")
        
        # Text display
        text_frame = tk.Frame(dialog)
        text_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")
        
        text_widget = tk.Text(
            text_frame,
            wrap="word",
            yscrollcommand=scrollbar.set,
            font=("Courier", 9),
            bg="white",
            fg="black"
        )
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)
        
        # Insert content
        text_widget.insert("1.0", content)
        text_widget.configure(state="disabled")
        
        # Button frame
        button_frame = tk.Frame(dialog)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        close_btn = tk.Button(
            button_frame,
            text="Close",
            command=dialog.destroy,
            width=15
        )
        close_btn.pack(side="right")

    def _open_github(self):
        """Open GitHub repository in default browser."""
        try:
            webbrowser.open(GITHUB_REPO)
        except Exception as e:
            messagebox.showinfo(
                "GitHub Repository",
                f"Visit the GitHub repository:\n\n{GITHUB_REPO}\n\n"
                f"(Could not open browser: {e})"
            )

    def _show_about(self):
        """Show About dialog."""
        about_text = f"""{WINDOW_TITLE}
Version 1.0.0

Download YouTube videos as MP4 files.

Features:
• Download videos in multiple quality options
• Automatic FFmpeg integration
• Fast and reliable downloading
• User-friendly interface
• Built-in Help menu and documentation

Technologies:
• Python 3.x
• CustomTkinter (Modern GUI)
• yt-dlp (YouTube extraction)
• FFmpeg (Media processing)

Support & More:
• Help → Getting Started
• Help → User Manual
• Help → GitHub Repository
• {GITHUB_REPO}

Legal:
Only download content you own or have 
permission to download. Respect copyright 
laws and YouTube Terms of Service.

Version: 1.0.0
License: MIT
"""
        messagebox.showinfo("About", about_text)


def main():
    """Launch the application."""
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    main()
