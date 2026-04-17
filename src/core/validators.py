"""Validation utilities for URLs, paths, and filenames."""

import re
from pathlib import Path
from urllib.parse import urlparse

from .errors import InvalidURLError


def is_valid_youtube_url(url: str) -> bool:
    """
    Validate that a URL is a valid YouTube video URL.
    
    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/watch?v=VIDEO_ID&list=... (single video, ignore playlist)
    
    Returns:
        True if valid YouTube URL, False otherwise.
    """
    if not url or not isinstance(url, str):
        return False
    
    url = url.strip()
    
    # Match youtube.com with watch?v=
    if "youtube.com" in url or "youtu.be" in url:
        # Extract video ID from various formats
        patterns = [
            r"(?:youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11}))",
            r"(?:youtu\.be\/([a-zA-Z0-9_-]{11}))",
        ]
        for pattern in patterns:
            if re.search(pattern, url):
                return True
    
    return False


def check_disk_space(path: Path, estimated_size_mb: int) -> bool:
    """
    Check if destination path has sufficient free disk space.
    
    Args:
        path: Destination path (file or directory).
        estimated_size_mb: Estimated file size in MB.
    
    Returns:
        True if sufficient space, False otherwise.
    """
    try:
        import shutil
        
        # Get parent directory if path is a file
        check_path = path.parent if path.is_file() else path
        if not check_path.exists():
            check_path = check_path.parent
        
        stat = shutil.disk_usage(check_path)
        free_bytes = stat.free
        free_mb = free_bytes / (1024 ** 2)
        
        # Add 10% safety margin
        required_mb = estimated_size_mb * 1.1
        return free_mb >= required_mb
    except Exception:
        # If we can't check, assume it's okay and let the download fail gracefully
        return True


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to remove invalid Windows characters.
    
    Replaces: < > : " / \\ | ? *
    with underscore.
    
    Args:
        filename: Original filename (usually video title).
    
    Returns:
        Safe filename for Windows filesystem.
    """
    # Remove/replace invalid Windows characters
    safe = re.sub(r'[<>:"/\\|?*]', "_", filename)
    # Remove trailing dots and spaces
    safe = safe.rstrip(". ")
    # Limit to reasonable length (255 is max for most filesystems, leave room for extension)
    safe = safe[:240]
    return safe if safe else "download"


def validate_output_directory(path: Path) -> bool:
    """
    Validate that output directory is writable.
    
    Args:
        path: Target directory path.
    
    Returns:
        True if directory exists and is writable.
    
    Raises:
        ValueError: If directory doesn't exist or isn't writable.
    """
    if not path.exists():
        try:
            path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise ValueError(f"Cannot create directory {path}: {e}")
    
    if not path.is_dir():
        raise ValueError(f"Path is not a directory: {path}")
    
    # Test write permission
    try:
        test_file = path / ".write_test"
        test_file.touch()
        test_file.unlink()
    except Exception as e:
        raise ValueError(f"Directory is not writable: {path}\nError: {e}")
    
    return True
