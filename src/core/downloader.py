"""YouTube download manager using yt-dlp backend."""

import shutil
from pathlib import Path
from typing import Callable, Dict, Optional
import yt_dlp

from .errors import (
    FFmpegError,
    GeoRestrictedError,
    NetworkError,
    YouTubeError,
)
from .validators import sanitize_filename, validate_output_directory

# Configuration constants
DEFAULT_SOCKET_TIMEOUT = 30
DEFAULT_RETRIES = 3
DEFAULT_FRAGMENT_RETRIES = 3
OUTPUT_EXTENSIONS = ["mp4", "mkv", "webm", "mov", "avi"]
FFMPEG_ERROR_KEYWORDS = ["ffmpeg", "postprocessor"]
GEO_ERROR_KEYWORDS = ["geo", "georestricted"]
FORMAT_ERROR_KEYWORDS = ["requested format is not available", "format is not available"]


class DownloadManager:
    """Manages YouTube video downloads with progress tracking."""

    def __init__(self, output_dir: Path):
        """
        Initialize download manager.
        
        Args:
            output_dir: Directory to save downloaded videos.
            
        Raises:
            FFmpegError: If FFmpeg is not available.
        """
        self.output_dir = Path(output_dir)
        validate_output_directory(self.output_dir)
        
        # Verify FFmpeg is available
        if not self._has_ffmpeg():
            raise FFmpegError(
                "FFmpeg not found. Please install FFmpeg:\n"
                "  Windows: choco install ffmpeg\n"
                "  Or download from: https://ffmpeg.org/download.html"
            )
        
        self.current_download = None
        self._cancelled = False
        self._progress_callback: Optional[Callable] = None

    @staticmethod
    def _has_ffmpeg() -> bool:
        """Check if FFmpeg is available in PATH."""
        return shutil.which("ffmpeg") is not None

    def _progress_hook(self, d: Dict):
        """
        Handle progress updates from yt-dlp.
        
        Args:
            d: Progress dict from yt-dlp containing status and metrics.
        """
        if self._progress_callback is None:
            return
        
        status = d.get("status")
        
        if status == "downloading":
            self._handle_download_progress(d)
        elif status == "finished":
            self._progress_callback({"status": "merging"})
        elif status == "error":
            self._cancelled = True
            self._progress_callback({"status": "error", "message": d.get("error")})

    def _handle_download_progress(self, d: Dict):
        """
        Process download progress information.
        
        Args:
            d: Progress dict with download metrics.
        """
        progress = {
            "status": "downloading",
            "downloaded": d.get("downloaded_bytes", 0),
            "total": d.get("total_bytes", 0),
            "speed": d.get("speed"),
            "eta": d.get("eta", 0),
        }
        self._progress_callback(progress)

    def fetch_video_info(self, url: str) -> Dict:
        """
        Fetch metadata about a video without downloading.
        
        Args:
            url: YouTube video URL.
        
        Returns:
            Dict containing title, duration, uploader, and available qualities.
        
        Raises:
            YouTubeError: If video metadata cannot be fetched.
            GeoRestrictedError: If video is geo-restricted.
        """
        ydl_opts = self._get_metadata_ydl_options()
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        
        try:
            # Use process=False to skip format validation during metadata extraction
            info = ydl.extract_info(url, download=False, process=False)
            qualities = self._extract_qualities(info.get("formats", []))
            
            return {
                "title": info.get("title", "Unknown"),
                "duration": info.get("duration", 0),
                "uploader": info.get("uploader", "Unknown"),
                "upload_date": info.get("upload_date", "Unknown"),
                "formats_count": len(info.get("formats", [])),
                "qualities": qualities,
            }
        except yt_dlp.utils.ExtractorError as e:
            self._handle_extractor_error(e)
        except yt_dlp.utils.DownloadError as e:
            raise YouTubeError(f"Download error: {e}") from e
        except Exception as e:
            raise YouTubeError(f"Unexpected error fetching video: {e}") from e

    @staticmethod
    def _get_metadata_ydl_options() -> Dict:
        """
        Get YoutubeDL options for metadata extraction.
        
        Returns:
            Dict of YoutubeDL options.
        """
        return {
            "quiet": True,
            "no_warnings": True,
            "socket_timeout": DEFAULT_SOCKET_TIMEOUT,
            "retries": DEFAULT_RETRIES,
        }

    @staticmethod
    def _handle_extractor_error(e: yt_dlp.utils.ExtractorError):
        """
        Handle extractor errors and raise appropriate exception.
        
        Args:
            e: The ExtractorError.
            
        Raises:
            GeoRestrictedError: If video is geo-restricted.
            YouTubeError: For other extractor errors.
        """
        error_str = str(e).lower()
        if any(keyword in error_str for keyword in GEO_ERROR_KEYWORDS):
            raise GeoRestrictedError(
                "This video is not available in your region."
            ) from e
        raise YouTubeError(f"Cannot fetch video info: {e}") from e

    def _extract_qualities(self, formats: list) -> Dict[str, str]:
        """
        Extract available video qualities from format list.
        
        Args:
            formats: List of format dicts from yt-dlp.
        
        Returns:
            Dict mapping quality name (e.g., "1080p") to format string.
            Note: All qualities map to "best" for maximum compatibility.
        """
        heights_found = self._collect_video_heights(formats)
        qualities = self._build_quality_options(heights_found)
        
        # Add "Best (Auto)" option at the start
        return {"Best (Auto)": "best", **qualities}

    @staticmethod
    def _collect_video_heights(formats: list) -> set:
        """
        Collect unique video heights from formats.
        
        Args:
            formats: List of format dicts from yt-dlp.
            
        Returns:
            Set of unique heights found.
        """
        heights = set()
        for fmt in formats:
            height = fmt.get("height")
            # Skip audio-only streams (vcodec=none) and formats without height
            if height and fmt.get("vcodec") != "none":
                heights.add(height)
        return heights

    @staticmethod
    def _build_quality_options(heights: set) -> Dict[str, str]:
        """
        Build quality options from heights.
        
        Args:
            heights: Set of video heights.
            
        Returns:
            Dict mapping quality labels to format strings.
        """
        qualities = {}
        # Sort heights in descending order (1080p first, then 720p, etc.)
        for height in sorted(heights, reverse=True):
            quality_label = f"{height}p"
            # All map to "best" for maximum compatibility
            qualities[quality_label] = "best"
        return qualities

    def download(
        self, url: str, on_progress: Callable[[Dict], None] = None, format_id: str = None
    ) -> str:
        """
        Download a YouTube video as MP4.
        
        Args:
            url: YouTube video URL.
            on_progress: Callback function for progress updates.
            format_id: Specific format string to download.
        
        Returns:
            Path to downloaded file.
        
        Raises:
            YouTubeError: If download fails.
            FFmpegError: If FFmpeg is unavailable.
            NetworkError: If network error occurs.
            GeoRestrictedError: If video is geo-restricted.
        """
        self._cancelled = False
        self._progress_callback = on_progress
        
        download_format = format_id if format_id else "best"
        ydl_opts = self._get_download_ydl_options(download_format)
        
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        ydl.add_progress_hook(self._progress_hook)
        
        try:
            info = ydl.extract_info(url, download=True)
            return self._find_downloaded_file(info)
        
        except yt_dlp.utils.ExtractorError as e:
            self._handle_extractor_error(e)
        except yt_dlp.utils.DownloadError as e:
            self._handle_download_error(e, format_id, url, on_progress)
        except Exception as e:
            self._handle_general_error(e)

    def _get_download_ydl_options(self, format_string: str) -> Dict:
        """
        Get YoutubeDL options for downloading.
        
        Args:
            format_string: Format selector string.
            
        Returns:
            Dict of YoutubeDL options.
        """
        return {
            "format": format_string,
            "merge_output_format": "mp4",
            "outtmpl": str(self.output_dir / "%(title)s.%(ext)s"),
            "quiet": True,
            "noprogress": True,
            "socket_timeout": DEFAULT_SOCKET_TIMEOUT,
            "retries": DEFAULT_RETRIES,
            "fragment_retries": DEFAULT_FRAGMENT_RETRIES,
            "no_warnings": True,
        }

    def _find_downloaded_file(self, info: Dict) -> str:
        """
        Find the downloaded file path.
        
        Args:
            info: Info dict from yt-dlp.
            
        Returns:
            Path to the downloaded file.
        """
        title = info.get("title", "video")
        safe_title = sanitize_filename(title)
        output_file = self.output_dir / f"{safe_title}.mp4"
        
        # If MP4 doesn't exist, search for alternative formats
        if not output_file.exists():
            for ext in OUTPUT_EXTENSIONS:
                potential_file = self.output_dir / f"{safe_title}.{ext}"
                if potential_file.exists():
                    return str(potential_file)
        
        return str(output_file)

    def _handle_download_error(
        self, e: yt_dlp.utils.DownloadError, 
        format_id: str, url: str,
        on_progress: Callable[[Dict], None]
    ):
        """
        Handle download errors and attempt fallback.
        
        Args:
            e: The DownloadError.
            format_id: Original format ID requested.
            url: Video URL.
            on_progress: Progress callback.
            
        Raises:
            FFmpegError: If FFmpeg is missing.
            YouTubeError: For other download errors.
        """
        error_str = str(e).lower()
        
        # Try fallback to "best" if format not available
        if any(keyword in error_str for keyword in FORMAT_ERROR_KEYWORDS):
            if format_id and format_id != "best":
                return self.download(url, on_progress, "best")
        
        # Check for FFmpeg errors
        if any(keyword in error_str for keyword in FFMPEG_ERROR_KEYWORDS):
            raise FFmpegError(
                "FFmpeg error during merge. Please ensure FFmpeg is installed:\n"
                "  choco install ffmpeg"
            ) from e
        
        raise YouTubeError(f"Download error: {e}") from e

    @staticmethod
    def _handle_general_error(e: Exception):
        """
        Handle unexpected errors.
        
        Args:
            e: The exception.
            
        Raises:
            NetworkError: If timeout error.
            YouTubeError: For other errors.
        """
        if "timeout" in str(e).lower():
            raise NetworkError(f"Network timeout: {e}") from e
        raise YouTubeError(f"Download failed: {e}") from e

    def cancel_download(self):
        """Request cancellation of current download."""
        self._cancelled = True

    def cleanup_partial_downloads(self, output_filename: str):
        """
        Clean up partial/failed download files.
        
        Args:
            output_filename: Name of file that failed to download.
        """
        output_path = self.output_dir / output_filename
        
        # Remove the main file if it exists
        if output_path.exists():
            try:
                output_path.unlink()
            except Exception:
                pass
        
        # Remove .part files (yt-dlp temporary files)
        for ext in [".part", ".f*.partial"]:
            for partial in self.output_dir.glob(f"{output_filename}*{ext}"):
                try:
                    partial.unlink()
                except Exception:
                    pass
