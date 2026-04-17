"""Normalized exception types for YouTube downloader."""


class YouTubeDownloaderError(Exception):
    """Base exception for all downloader-related errors."""

    pass


class YouTubeError(YouTubeDownloaderError):
    """Error extracting or downloading from YouTube."""

    pass


class FFmpegError(YouTubeDownloaderError):
    """FFmpeg is missing or failed during merge/encode."""

    pass


class NetworkError(YouTubeDownloaderError):
    """Network error during download (timeout, connection lost, etc.)."""

    pass


class InvalidURLError(YouTubeDownloaderError):
    """URL is not a valid YouTube URL."""

    pass


class GeoRestrictedError(YouTubeDownloaderError):
    """Video is geo-restricted and cannot be downloaded from this region."""

    pass
