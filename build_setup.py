"""
Build script for creating Windows installer.
Bundles Python executable with FFmpeg using PyInstaller.
"""

import subprocess
import sys
from pathlib import Path

# CUSTOMIZE THESE SETTINGS
VERSION = "1.0.0"

def check_dependencies():
    """Check if required build tools are installed."""
    try:
        import PyInstaller
        print("[OK] PyInstaller found")
    except ImportError:
        print("[ERROR] PyInstaller not installed. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable():
    """Build executable using PyInstaller."""
    print("\n" + "="*60)
    print(f"Building executable with PyInstaller v{VERSION}...")
    print("="*60)
    
    cmd = [
        "pyinstaller",
        "--name", "YouTubeDownloader",
        "--windowed",  # No console window
        "--onefile",   # Single executable file
        "--add-data", "src:src",  # Include src directory
        "--clean",
        "main.py",
    ]
    
    # Add icon if it exists
    icon_path = Path(__file__).parent / "assets" / "icon.ico"
    if icon_path.exists():
        cmd.insert(3, icon_path.as_posix())
        cmd.insert(3, "--icon")
        print(f"Using icon: {icon_path}")
    else:
        print("Note: No icon found at assets/icon.ico (optional)")
    
    result = subprocess.run(cmd, cwd=Path(__file__).parent)
    
    if result.returncode == 0:
        print("\n[OK] Executable built successfully!")
        print(f"  Location: dist/YouTubeDownloader.exe")
    else:
        print("\n[ERROR] Build failed")
        sys.exit(1)

if __name__ == "__main__":
    check_dependencies()
    build_executable()
    print("\nNext steps:")
    print("1. Download FFmpeg from: https://ffmpeg.org/download.html")
    print("2. Extract ffmpeg.exe and ffprobe.exe to a 'bin' folder")
    print("3. Use Inno Setup to create installer (see build_installer.iss)")
