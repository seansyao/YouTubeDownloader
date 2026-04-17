"""Quick validation tests for core modules."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.validators import is_valid_youtube_url, sanitize_filename, check_disk_space
from src.core.errors import (
    InvalidURLError,
    YouTubeError,
    FFmpegError,
)


def test_validators():
    """Test URL validation and filename sanitization."""
    print("Testing URL Validators...")
    
    # Valid URLs
    assert is_valid_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    assert is_valid_youtube_url("https://youtube.com/watch?v=dQw4w9WgXcQ")
    assert is_valid_youtube_url("https://youtu.be/dQw4w9WgXcQ")
    assert is_valid_youtube_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=PLxxx")  # with playlist param
    print("  ✓ Valid URLs pass")
    
    # Invalid URLs
    assert not is_valid_youtube_url("https://example.com")
    assert not is_valid_youtube_url("not-a-url")
    assert not is_valid_youtube_url("")
    assert not is_valid_youtube_url("youtube.com/watch")  # missing video ID
    print("  ✓ Invalid URLs rejected")
    
    # Filename sanitization
    assert sanitize_filename("My: Video <2024>") == "My_ Video _2024_"
    assert sanitize_filename("Bad/Path\\File|Name") == "Bad_Path_File_Name"
    assert sanitize_filename("normal_filename.txt") == "normal_filename.txt"
    print("  ✓ Filenames sanitized correctly")
    
    # Disk space check
    result = check_disk_space(Path.home(), 100)
    assert isinstance(result, bool)
    print("  ✓ Disk space check works")


def test_error_hierarchy():
    """Test error class hierarchy."""
    print("\nTesting Error Classes...")
    
    errors = [
        YouTubeError("test"),
        FFmpegError("test"),
        InvalidURLError("test"),
    ]
    
    for err in errors:
        assert isinstance(err, Exception)
    
    print("  ✓ All error classes properly defined")


def test_imports():
    """Test that all modules can be imported."""
    print("\nTesting Module Imports...")
    
    try:
        from src.core.config import ConfigManager
        from src.core.downloader import DownloadManager
        from src.core.postprocess_base import PostProcessorBase, NoOpPostProcessor
        from src.gui.main_window import MainWindow
        print("  ✓ All modules import successfully")
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        raise


def test_downloader_quality_extraction():
    """Test quality extraction from mock formats."""
    print("\nTesting Quality Extraction...")
    
    from src.core.downloader import DownloadManager
    
    manager = DownloadManager(Path.home() / "Downloads")
    
    # Mock formats like yt-dlp would return
    mock_formats = [
        {"format_id": "137", "height": 1080, "vcodec": "h264", "acodec": "aac", "fps": 30},
        {"format_id": "136", "height": 720, "vcodec": "h264", "acodec": "aac", "fps": 30},
        {"format_id": "135", "height": 480, "vcodec": "h264", "acodec": "aac", "fps": 30},
        {"format_id": "140", "height": None, "vcodec": "none", "acodec": "aac"},  # audio only
    ]
    
    qualities = manager._extract_qualities(mock_formats)
    
    # Should have auto + extracted qualities
    assert "Best (Auto)" in qualities
    # All qualities should use "best" format for safety
    for quality_name, format_string in qualities.items():
        assert format_string == "best", f"Quality {quality_name} should map to 'best', got {format_string}"
    
    assert any("1080p" in q for q in qualities.keys())
    assert any("720p" in q for q in qualities.keys())
    assert any("480p" in q for q in qualities.keys())
    
    print("  ✓ Qualities extracted correctly (all using 'best' format)")
    print("    Available qualities:", list(qualities.keys()))


if __name__ == "__main__":
    print("=" * 50)
    print("YouTube Downloader - Unit Tests")
    print("=" * 50)
    
    test_validators()
    test_error_hierarchy()
    test_imports()
    test_downloader_quality_extraction()
    
    print("\n" + "=" * 50)
    print("All tests passed! ✓")
    print("=" * 50)
    print("\nNext steps:")
    print("  1. Paste YouTube URL and click 'Load Video Info & Qualities'")
    print("  2. Select quality from dropdown")
    print("  3. Click 'Download'")
    print("  4. Video will be saved to your chosen folder")
