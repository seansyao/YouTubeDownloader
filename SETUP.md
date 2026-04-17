# Installation Package Setup Guide

This guide explains how to build and distribute the YouTube MP4 Downloader as a professional Windows installer.

## Overview

The installer package includes:
- ✓ YouTube MP4 Downloader executable (bundled Python app)
- ✓ FFmpeg with ffprobe
- ✓ Automatic PATH configuration
- ✓ Desktop shortcuts
- ✓ Documentation files (README.md, MANUAL.md, plan.md)
- ✓ Built-in Help menu with documentation viewer
- ✓ Uninstall support with cleanup

## Prerequisites

You'll need to install these tools (one-time setup):

### 1. PyInstaller (converts Python → Windows executable)
```bash
pip install pyinstaller
```

### 2. Inno Setup (creates Windows installer)
- Download from: http://www.jrsoftware.org/isdl.php
- Install to default location: `C:\Program Files (x86)\Inno Setup 6\`

## Step-by-Step Build Process

### Step 1: Prepare FFmpeg

1. Download FFmpeg from: https://ffmpeg.org/download.html
   - Choose: **Windows** → **Full** build (recommended)
   - File format: `.7z` or `.zip`

2. Extract the files:
   ```
   YouTubeDownloader/
   ├── build_setup.py
   ├── build_installer.iss
   └── bin/                 ← Create this folder
       ├── ffmpeg.exe       ← Copy here
       └── ffprobe.exe      ← Copy here
   ```

3. Verify FFmpeg works:
   ```bash
   bin\ffmpeg.exe -version
   ```

### Step 2: Build Executable with PyInstaller

```bash
cd c:\Users\admin\Projects\YouTubeDownloader
python build_setup.py
```

This creates:
```
dist/
└── YouTubeDownloader.exe  (single executable, ~200MB with dependencies)
```

**Expected output:**
```
✓ Executable built successfully!
  Location: dist/YouTubeDownloader.exe
```

### Step 3: Create Windows Installer

**Option A: Using Inno Setup GUI (Recommended for first-time)**

1. Open Inno Setup 6 IDE
   - Start Menu → Inno Setup 6 → Inno Setup Compiler
2. File → Open → select `build_installer.iss`
3. Click "Compile" button
4. Installer created: `output/YouTubeDownloaderSetup.exe`

**Option B: Command Line (Automated)**

```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" build_installer.iss
```

### Step 4: Test the Installer

1. Run the installer:
   ```
   output/YouTubeDownloaderSetup.exe
   ```

2. Follow wizard:
   - Accept license
   - Choose install location (default: `C:\Program Files\YouTubeDownloader`)
   - Select shortcut options
   - Review and install

3. Verify installation:
   - Desktop shortcut created ✓
   - Program installed in `C:\Program Files\YouTubeDownloader` ✓
   - FFmpeg in PATH: Open Command Prompt, type `ffmpeg -version` ✓

4. Launch application:
   - Double-click desktop shortcut or
   - Start Menu → YouTube MP4 Downloader

### Step 5: Distribute

The installer is ready to share! 

**Distribution methods:**
- GitHub Releases: https://github.com/yourusername/YouTubeDownloader/releases
- Direct download link
- Software distribution sites

**File:**
```
YouTubeDownloaderSetup.exe  (~250-300 MB)
```

## What the Installer Does

### Installation:
1. ✓ Extracts application to `C:\Program Files\YouTubeDownloader\`
2. ✓ Installs FFmpeg executables to `bin\` subdirectory
3. ✓ Adds `C:\Program Files\YouTubeDownloader\bin\` to Windows PATH
4. ✓ Creates Start Menu shortcuts
5. ✓ Creates Desktop shortcut (optional)
6. ✓ Copies documentation (README.md, plan.md)

### PATH Configuration:
- Automatically adds FFmpeg to system PATH
- Requires admin privileges (requested during install)
- FFmpeg accessible from any command prompt
- Survives Windows updates

### Uninstallation:
1. ✓ Removes application and FFmpeg
2. ✓ Removes from PATH automatically
3. ✓ Removes shortcuts
4. ✓ Cleans up installation directory

## Customization

### Change App Details

Edit `build_installer.iss`:

```ini
[Setup]
AppName=YouTube MP4 Downloader
AppVersion=1.0.0
AppPublisher=Your Name
AppPublisherURL=https://github.com/yourusername/YouTubeDownloader
```

### Change Installation Directory

```ini
[Setup]
DefaultDirName={autopf}\YouTubeDownloader
```

- `{autopf}` = Program Files (auto 32/64-bit)
- `{pf}` = Program Files
- `{pf64}` = Program Files (64-bit)
- `{sd}` = System drive (C:)

### Add Application Icon

1. Create/find a `.ico` file (256×256 pixels recommended)
2. Place in project: `assets/icon.ico`
3. Update `build_setup.py`:
   ```python
   "--icon", "assets/icon.ico",
   ```

### Add License Agreement

1. Create file: `LICENSE.txt` (plain text)
2. Update `build_installer.iss`:
   ```ini
   [Setup]
   LicenseFile=LICENSE.txt
   ```

## Troubleshooting

### "FFmpeg not found" during build
- Ensure `bin/ffmpeg.exe` and `bin/ffprobe.exe` exist
- Copy from FFmpeg download to `bin/` folder

### Installer won't run
- Check Windows Defender/antivirus isn't blocking it
- Right-click → Properties → Unblock (if available)
- Try running as Administrator

### PATH not working after install
- Restart Command Prompt or system
- Verify in: Settings → Environment Variables → System → PATH
- Should contain: `C:\Program Files\YouTubeDownloader\bin\`

### "Admin privileges required" error
- Run installer as Administrator
- Some corporate networks require admin approval

### Build fails with PyInstaller
- Ensure all requirements installed: `pip install -r requirements.txt`
- Try clean build: `rm -r build/ dist/` then rebuild
- Check Python version: `python --version` (3.8+ required)

## Advanced: Unattended Installation

Users can install silently without wizard:

```bash
YouTubeDownloaderSetup.exe /SILENT /NORESTART
```

Common flags:
- `/SILENT` = Silent mode (no wizard)
- `/VERYSILENT` = Very silent (minimal UI)
- `/NORESTART` = Don't auto-restart
- `/DIR="C:\MyApp"` = Custom install location

Example:
```bash
YouTubeDownloaderSetup.exe /SILENT /NORESTART /DIR="D:\Apps\YouTubeDownloader"
```

## File Structure After Installation

```
C:\Program Files\YouTubeDownloader\
├── YouTubeDownloader.exe    (main application)
├── bin/
│   ├── ffmpeg.exe           (video encoder)
│   └── ffprobe.exe          (media analyzer)
├── README.md                (user guide)
├── plan.md                  (technical docs)
└── LICENSE                  (license)
```

## Version Updates

To create an updated installer:

1. Update version in `build_setup.py` and `build_installer.iss`
2. Rebuild executable
3. Rebuild installer
4. Old installation will be uninstalled and replaced

## Legal

- Ensure you have rights to distribute FFmpeg (LGPL license)
- Include license notices for all components
- See [FFmpeg Legal](https://ffmpeg.org/legal.html)

## Support

For issues with the installer:
- GitHub Issues: https://github.com/yourusername/YouTubeDownloader/issues
- FFmpeg Help: https://ffmpeg.org/
- Inno Setup Help: http://www.jrsoftware.org/ishelp/

## Next Steps

1. ✓ Ensure `bin/` folder has FFmpeg executables
2. ✓ Run `python build_setup.py`
3. ✓ Use Inno Setup to compile `build_installer.iss`
4. ✓ Test `output/YouTubeDownloaderSetup.exe`
5. ✓ Share installer with users!
