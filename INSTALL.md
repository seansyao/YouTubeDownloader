# YouTube MP4 Downloader - Installation Guide

**Quick Start:** Download and run `YouTubeDownloaderSetup.exe` - that's it!

## System Requirements

- **OS:** Windows 10 or Windows 11
- **RAM:** 2GB minimum
- **Disk Space:** 300MB for installation
- **Internet:** For downloading videos

## Installation Steps

### 1. Download
- Get the latest `YouTubeDownloaderSetup.exe` from:
  - GitHub Releases: https://github.com/yourusername/YouTubeDownloader/releases
  - Or direct download link

### 2. Run Installer
1. Double-click `YouTubeDownloaderSetup.exe`
2. Windows may show security warning - click "Run anyway" or "More info" → "Run anyway"
3. Follow the installation wizard:
   - Read and accept the license
   - Choose installation location (default is fine: `C:\Program Files\YouTubeDownloader\`)
   - Choose if you want a Desktop shortcut
   - Click "Install"

### 3. Launch Application
After installation, the app will launch automatically. You can also:
- **Click Desktop shortcut** (if you created one)
- **Start Menu** → Search "YouTube MP4 Downloader" → Open

## First Run Checklist

After launching:
- ✓ Window appears with "YouTube MP4 Downloader" title
- ✓ Paste a YouTube URL
- ✓ Click "Load Video Info & Qualities"
- ✓ Click "Download"
- ✓ Video downloads to your chosen folder

**Done!** 🎉

## Uninstall

To remove the application:
1. **Windows Settings** → **Apps** → **Apps & features**
2. Search "YouTube MP4 Downloader"
3. Click it, then click "Uninstall"
4. Follow the uninstall wizard

**What gets removed:**
- ✓ Application executable
- ✓ FFmpeg tools
- ✓ Shortcuts
- ✓ PATH environment variable
- ✓ Installation directory

**What remains:**
- Downloaded videos (safe in your Videos/Downloads folder)
- Application settings (auto-cleaned on next launch)

## Troubleshooting Installation

### "FFmpeg not found" Error
**Cause:** FFmpeg not installed or PATH not configured
**Solution:**
1. Uninstall the application
2. Reinstall `YouTubeDownloaderSetup.exe` as Administrator
3. Verify installation: Open Command Prompt, type `ffmpeg -version`

### Installation Requires Administrator Rights
**Solution:**
1. Right-click `YouTubeDownloaderSetup.exe`
2. Select "Run as administrator"
3. Click "Yes" when Windows asks for permission

### "Setup files corrupted" Error
**Solution:**
1. Delete the `.exe` file
2. Download a fresh copy
3. Run the installer again

## Legal & Disclaimer

### Before Using
- ⚠️ **Only download content you own or have permission to download**
- Respect copyright laws and YouTube's Terms of Service
- Some content may be geo-restricted or DRM-protected

### What You Can Download
- ✓ Your own videos/content
- ✓ Creative Commons videos
- ✓ Public domain content
- ✓ Content with explicit download permission

### What You Cannot Download
- ✗ Copyrighted music/movies without permission
- ✗ Private videos
- ✗ Live streams (may not work)
- ✗ Premium/membership-only content

## Technical Details

**What's Installed:**
- YouTube downloader application
- FFmpeg (video encoding)
- Python runtime libraries
- Configuration files

**Size:** ~300MB
**Version:** 1.0.0
**License:** MIT (see LICENSE file)

---

**Installation complete!** 🎉

For usage instructions, see **MANUAL.md**
For more info, visit: https://github.com/yourusername/YouTubeDownloader
