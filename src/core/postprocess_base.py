"""Extension point interface for post-processing (future Demucs karaoke)."""

from abc import ABC, abstractmethod
from pathlib import Path


class PostProcessorBase(ABC):
    """Base class for post-processors like vocal removal."""

    def __init__(self, output_dir: Path):
        """
        Initialize post-processor.
        
        Args:
            output_dir: Directory where processed files will be saved.
        """
        self.output_dir = Path(output_dir)

    @abstractmethod
    def process(self, video_path: Path) -> Path:
        """
        Process a downloaded video.
        
        Args:
            video_path: Path to downloaded MP4 file.
        
        Returns:
            Path to processed output file.
        """
        pass

    def is_available(self) -> bool:
        """Check if required dependencies (models, libraries) are available."""
        return False


class NoOpPostProcessor(PostProcessorBase):
    """Placeholder post-processor that does nothing."""

    def process(self, video_path: Path) -> Path:
        """Return input path unchanged."""
        return video_path

    def is_available(self) -> bool:
        """Always available (does nothing)."""
        return True
