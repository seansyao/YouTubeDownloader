# Distribution Checklist & Release Guide

This guide is for developers preparing to release the YouTube MP4 Downloader.

## Pre-Release Preparation

### Code Cleanup
- [ ] All tests pass: `python test_core.py` ✓
- [ ] No syntax errors: `python -m py_compile src/core/*.py src/gui/*.py main.py`
- [ ] No unused imports or variables
- [ ] All docstrings present and accurate
- [ ] Code follows PEP 8 style guidelines

### Version Numbering
- [ ] Update version in:
  - `build_setup.py` (PyInstaller config)
  - `build_installer.iss` (Inno Setup config)
  - `src/__init__.py` (if exists)
  - Consider semantic versioning: MAJOR.MINOR.PATCH

### Documentation
- [ ] `README.md` is current and accurate
- [ ] `SETUP.md` installation instructions work
- [ ] `INSTALL.md` user guide is clear
- [ ] `plan.md` technical documentation updated
- [ ] `LICENSE` file present and correct
- [ ] Code comments updated if needed

### Dependencies
- [ ] `requirements.txt` has all dependencies
- [ ] All versions pinned or compatible versions specified
- [ ] Run: `pip install -r requirements.txt` successfully
- [ ] Test application works with installed versions

## Build Preparation

### Prerequisites Check
- [ ] Windows 10/11 system available for building
- [ ] Python 3.8+ installed: `python --version`
- [ ] PyInstaller installed: `pip install pyinstaller`
- [ ] Inno Setup 6 installed: http://www.jrsoftware.org/isdl.php

### FFmpeg Preparation
- [ ] Download latest FFmpeg Windows build
  - Source: https://ffmpeg.org/download.html
  - Format: Full build (.7z or .zip)
  - Do NOT use shared/static build

- [ ] Extract and verify:
  ```bash
  mkdir bin
  # Copy ffmpeg.exe and ffprobe.exe to bin/
  bin\ffmpeg.exe -version  # Should work
  bin\ffprobe.exe -version # Should work
  ```

- [ ] Note FFmpeg version for release notes

### Project Structure Check
```
YouTubeDownloader/
├── build_setup.py          ✓
├── build_installer.iss     ✓
├── build.bat               ✓
├── main.py                 ✓
├── requirements.txt        ✓
├── README.md               ✓
├── INSTALL.md              ✓
├── SETUP.md                ✓
├── LICENSE                 ✓
├── plan.md                 ✓
├── src/                    ✓
├── test_core.py            ✓
└── bin/                    ✓
    ├── ffmpeg.exe
    └── ffprobe.exe
```

## Build Process

### Step 1: Build Executable
```bash
python build_setup.py
```

**Verify:**
- [ ] No errors during build
- [ ] `dist/YouTubeDownloader.exe` created (~200-250MB)
- [ ] Executable runs: `dist\YouTubeDownloader.exe`
- [ ] All features work in executable

### Step 2: Build Installer
```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" build_installer.iss
```

**Verify:**
- [ ] No errors during compilation
- [ ] `output/YouTubeDownloaderSetup.exe` created (~300MB)
- [ ] File size is reasonable (250-350MB)

### Step 3: Test Installer
On a **clean test system** (or VM), test the installer:

1. **Run installer:**
   - [ ] Double-click `YouTubeDownloaderSetup.exe`
   - [ ] Runs without errors
   - [ ] Installation wizard appears

2. **Installation:**
   - [ ] Can accept license
   - [ ] Can choose installation location
   - [ ] Can choose shortcuts
   - [ ] Installation completes

3. **Post-Installation:**
   - [ ] Desktop shortcut works (if selected)
   - [ ] Start Menu entry created
   - [ ] Application launches
   - [ ] No error messages

4. **FFmpeg:**
   - [ ] Open Command Prompt
   - [ ] Type: `ffmpeg -version` → Works
   - [ ] Type: `ffprobe -version` → Works

5. **Functionality:**
   - [ ] Paste test YouTube URL
   - [ ] Click "Load Video Info"
   - [ ] Video info appears
   - [ ] Can download successfully
   - [ ] Downloaded file is valid MP4

6. **Uninstall:**
   - [ ] Settings → Apps → Uninstall YouTube MP4 Downloader
   - [ ] Uninstaller runs without errors
   - [ ] All files removed
   - [ ] Start Menu entry removed
   - [ ] Desktop shortcut removed
   - [ ] FFmpeg no longer in PATH (verify: `ffmpeg -version` fails)

## Release Preparation

### Create Release Package
```
YouTubeDownloaderSetup-v1.0.0.exe  (main installer)
README.md                           (copy of readme)
INSTALL.md                          (user guide)
SHA256.txt                          (file hash for verification)
```

### Generate File Hash
```bash
certutil -hashfile YouTubeDownloaderSetup.exe SHA256 > SHA256.txt
```

**Include in release:**
```
SHA256: 1a2b3c4d5e6f... [full hash]
```

### Create Release Notes
Document in GitHub release:

**Example:**
```markdown
# YouTube MP4 Downloader v1.0.0

## New Features
- Quality selection dropdown
- Progress tracking with speed/ETA
- Automatic FFmpeg PATH configuration
- Windows installer with uninstall

## Bug Fixes
- Fixed format compatibility for restricted videos
- Improved error messages

## Installation
1. Download YouTubeDownloaderSetup.exe
2. Run installer
3. Follow wizard
4. Launch from Start Menu or Desktop

## System Requirements
- Windows 10 or 11
- 2GB RAM
- 300MB disk space

## Known Issues
- Some geo-blocked videos cannot be downloaded
- Live streams may not work

## Installation Verification
Download: YouTubeDownloaderSetup.exe (300MB)
SHA256: [hash from SHA256.txt]

Verify downloaded file:
Windows: certutil -hashfile YouTubeDownloaderSetup.exe SHA256
Mac/Linux: sha256sum YouTubeDownloaderSetup.exe
```

## GitHub Release Steps

### 1. Create Release on GitHub
```
Releases → Draft new release
Tag: v1.0.0
Title: YouTube MP4 Downloader v1.0.0
```

### 2. Upload Assets
- [ ] YouTubeDownloaderSetup.exe
- [ ] SHA256.txt
- [ ] README.md (optional)
- [ ] INSTALL.md (optional)

### 3. Write Release Notes
- [ ] Describe new features
- [ ] List bug fixes
- [ ] Note breaking changes
- [ ] Link to documentation

### 4. Publish Release
- [ ] Review all details
- [ ] Set as latest release
- [ ] Publish

## Post-Release

### Announce Release
- [ ] Update website/blog
- [ ] Post on social media
- [ ] Submit to software directories:
  - SourceForge
  - FileHippo
  - Softpedia
  - Reddit r/software

### Monitor Feedback
- [ ] Check GitHub issues for bug reports
- [ ] Respond to user questions
- [ ] Track installation issues
- [ ] Collect feature requests

### Plan Next Release
- [ ] Create next version milestone
- [ ] Plan new features
- [ ] Note bugs for fixing
- [ ] Update roadmap

## Maintenance Plan

### Regular Updates
- Update yt-dlp monthly: `pip install --upgrade yt-dlp`
- Test with new YouTube format changes
- Release patch versions as needed

### Long-term Support
- Bug fixes for 6-12 months
- Security updates indefinitely
- Major version every 1-2 years

### Deprecation Policy
- Announce in release notes
- 1-2 version warnings before removing feature
- Clear migration path for users

## Legal Checklist

- [ ] LICENSE file includes proper attribution
- [ ] FFmpeg license (LGPL) acknowledged
- [ ] Dependencies properly credited
- [ ] No GPL code (incompatible with customtkinter)
- [ ] Open source contributions credited

## Performance Optimization

Before release, verify:
- [ ] Startup time < 2 seconds
- [ ] Memory usage < 100MB idle
- [ ] Download speed matches yt-dlp
- [ ] No memory leaks during long downloads
- [ ] File size acceptable (~300MB)

## Rollback Plan

If critical issues found after release:

1. **Hotfix Release (v1.0.1):**
   ```bash
   # Fix bug
   python build_setup.py
   "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" build_installer.iss
   # Release immediately
   ```

2. **Communicate Issue:**
   - Mark previous release as "deprecated"
   - Add note: "Security issue - upgrade immediately"
   - Direct users to new version

3. **Prevent Recurrence:**
   - Add test case
   - Update CI/CD if applicable
   - Review code more carefully

## Version History Template

```
v1.0.0 - Initial Release
- Core download functionality
- Quality selection
- FFmpeg bundled
- Windows installer

v1.0.1 - Bug fixes
- Fixed [issue]
- Improved error handling

v1.1.0 - New features
- [feature]
- [feature]
```

## Success Metrics

Track after release:
- [ ] Downloads per month
- [ ] User feedback/reviews
- [ ] Bug reports received
- [ ] Feature requests
- [ ] Active issues

## Support Contacts

Keep current:
- [ ] GitHub Issues link updated
- [ ] Email support address (if applicable)
- [ ] Discord/Community server (if applicable)
- [ ] FAQ documentation

---

**Release Checklist Complete!** 🚀

You're ready to distribute the YouTube MP4 Downloader to users worldwide.
