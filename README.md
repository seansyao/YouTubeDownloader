# YouTube MP4 Downloader

A simple, user-friendly desktop application to download YouTube videos as MP4 files.

## Features

- **Simple GUI**: Download single YouTube videos with a click
- **MP4 Output**: Automatically converts/merges video and audio to MP4 format
- **Progress Tracking**: Real-time download progress and speed display
- **Error Handling**: Clear error messages for network issues, geo-restricted content, and missing dependencies
- **Customizable Output**: Choose where to save downloaded videos
- **Future Enhancement**: Framework ready for Demucs-based vocal removal (karaoke mode)

## Legal Disclaimer

⚠️ **IMPORTANT**: This tool is designed for downloading content you own or have explicit permission to download.

- **You are responsible** for respecting copyright laws and YouTube's Terms of Service
- Downloading copyrighted content without permission may violate DMCA or local copyright laws
- The author assumes **no liability** for misuse of this software

### Authorized Uses:
✅ Personal backups of your own uploads  
✅ Creative Commons licensed content (verify the license)  
✅ Public domain videos  
✅ Educational and research use (where permitted)  

### Before You Download:
- Verify you have permission to download the content
- Check the video's license and usage restrictions
- Respect creators' intellectual property rights

## Requirements

- **Python 3.8+**
- **FFmpeg** (required for audio/video merging)

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install FFmpeg

**Windows (using Chocolatey):**
```bash
choco install ffmpeg
```

**Windows (Manual):**
1. Download from https://ffmpeg.org/download.html
2. Add FFmpeg's `bin` folder to your system PATH
3. Verify: `ffmpeg -version` in Command Prompt

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

### 3. Run the Application

```bash
python main.py
```

A GUI window will appear. Paste a YouTube URL and click "Download" to start.

## Usage

1. **Open the Application**: Run `python main.py`
2. **Paste URL**: Copy a YouTube URL and paste it into the text field
3. **Choose Folder**: Click "Browse" to select where to save the video
4. **Download**: Click the "Download" button and wait for completion
5. **Success**: Your MP4 file will be saved to the selected folder

### Supported URL Formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`

### Supported Content:
- ✅ Single videos (including videos with custom titles/special characters)
- ✅ Age-restricted videos (may require browser authentication in advanced cases)
- ✅ Long-form content (streams, lectures, etc.)

### Not Supported (MVP):
- ❌ Playlists (one video at a time only)
- ❌ Channels
- ❌ Automatic captions/metadata

## Troubleshooting

### FFmpeg Not Found
**Error**: "FFmpeg not found" or "PostProcessor error"

**Solution**:
1. Install FFmpeg: `choco install ffmpeg` (Windows) or `brew install ffmpeg` (macOS)
2. Verify installation: `ffmpeg -version`
3. Restart the application

### Geo-Restricted Video
**Error**: "Video is not available in your region"

**Solution**: This video is blocked in your region. Some content may require a VPN or browser-based authentication to access.

### Network Timeout
**Error**: "Socket timeout" or connection lost

**Solution**:
1. Check your internet connection
2. Try again; the app will retry automatically
3. For large files (4GB+), ensure stable, fast connection

### Invalid YouTube URL
**Error**: "Invalid URL" or "Cannot fetch video"

**Solution**:
1. Verify the URL is a valid YouTube link (not a playlist, channel, or shortened URL)
2. Copy the full URL from the address bar: `youtube.com/watch?v=...`
3. Try a different video to confirm the app works

### File Already Exists
If a file with the same name exists, yt-dlp will append a number: `My Video.mp4` → `My Video (1).mp4`

## Project Structure

```
YouTubeDownloader/
├── main.py                          # Entry point
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── plan.md                          # Detailed architecture plan
│
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── downloader.py           # yt-dlp wrapper & download logic
│   │   ├── validators.py           # URL, path, filename validation
│   │   ├── config.py               # Configuration persistence
│   │   ├── errors.py               # Normalized exception types
│   │   └── postprocess_base.py     # Extension interface for future enhancements
│   │
│   └── gui/
│       └── main_window.py          # CustomTkinter UI
│
└── tests/
    └── (test files for validators, downloader, etc.)
```

## Development & Testing

### Run Tests (Manual for MVP):
```bash
# Download a small test video
python main.py
# Paste: https://www.youtube.com/watch?v=dQw4w9WgXcQ
# Click Download and verify MP4 appears
```

### Future Enhancement: Vocal Removal (Karaoke)

The codebase is structured to support adding a vocal removal feature later:
- `src/core/postprocess_base.py` defines the extension interface
- A future `VocalRemover` class will plug into the post-download pipeline
- No changes to the GUI or core downloader logic will be required

#### Planned Implementation (Not Yet):
- **Model**: Demucs (source separation) for high-quality karaoke output
- **Output**: Instrumental version saved as separate MP4
- **UI**: Optional "Create Karaoke Version" checkbox after download

## Command-Line Usage (Future)

Currently, the app is GUI-only. Future versions may support:
```bash
python -m src.cli --url "https://..." --output ./videos --karaoke
```

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| customtkinter | 5.2.2 | Modern GUI framework |
| yt-dlp | 2024.04.09 | YouTube downloading (succeeds youtube-dl) |
| Pillow | 10.1.0 | Image handling (if needed for thumbnails) |

## FAQ

**Q: Can I download a playlist?**  
A: Not yet. MVP supports single videos only. Use the app once per video.

**Q: Can I customize the output format?**  
A: Currently, all downloads are MP4. Future versions may offer WebM, MKV, etc.

**Q: Does the app work offline?**  
A: No. YouTube requires internet access. The app will notify you of network errors.

**Q: Can I pause/resume downloads?**  
A: No (MVP limitation). Downloads are atomic; interruptions require a fresh start.

**Q: Will my videos be uploaded anywhere?**  
A: No. All downloads are saved locally to your chosen folder. The app does not transmit files or metadata to external servers.

**Q: How do I uninstall?**  
A: Delete the project folder. No system-wide installation or registry changes.

## Contributing

This is a personal project. Suggestions and bug reports are welcome via GitHub Issues.

## License

MIT License - See LICENSE file for details.

---

**Questions or Issues?** Check the [Troubleshooting](#troubleshooting) section or open a GitHub issue.

**Ready to download?** Run `python main.py` and get started!
