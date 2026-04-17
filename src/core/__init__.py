"""Core functionality: downloader, validators, configuration."""

from .errors import (
    YouTubeDownloaderError,
    YouTubeError,
    FFmpegError,
    NetworkError,
    InvalidURLError,
    GeoRestrictedError,
)

__all__ = [
    "YouTubeDownloaderError",
    "YouTubeError",
    "FFmpegError",
    "NetworkError",
    "InvalidURLError",
    "GeoRestrictedError",
]
