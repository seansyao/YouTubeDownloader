"""Configuration and persistence management."""

import json
from pathlib import Path


class ConfigManager:
    """Manage app settings and persistent state."""

    DEFAULT_CONFIG = {
        "output_dir": str(Path.home() / "Downloads"),
        "theme": "dark",
        "max_retries": 3,
        "socket_timeout": 30,
    }

    def __init__(self, config_file: Path = None):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Path to config.json. Defaults to ~/.ytdl_config.json
        """
        self.config_file = config_file or (Path.home() / ".ytdl_config.json")
        self.config = self.DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        """Load config from file if it exists."""
        if self.config_file.exists():
            try:
                with open(self.config_file, "r") as f:
                    loaded = json.load(f)
                    self.config.update(loaded)
            except Exception:
                # Fallback to defaults on load error
                pass

    def save(self):
        """Persist config to file."""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception:
            pass  # Silent fail on save

    def get(self, key: str, default=None):
        """Get config value."""
        return self.config.get(key, default)

    def set(self, key: str, value):
        """Set config value and persist."""
        self.config[key] = value
        self.save()

    def get_output_dir(self) -> Path:
        """Get output directory as Path object."""
        return Path(self.get("output_dir", str(Path.home() / "Downloads")))

    def set_output_dir(self, path: Path):
        """Set and persist output directory."""
        self.set("output_dir", str(path))

    def get_theme(self) -> str:
        """Get current theme."""
        return self.get("theme", "dark")

    def set_theme(self, theme: str):
        """Set and persist theme (dark or light)."""
        self.set("theme", theme)
