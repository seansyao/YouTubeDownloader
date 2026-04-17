# YouTube MP4 Downloader - Architecture & Implementation Plan

## Overview

This is a lightweight, user-friendly Python desktop application for downloading YouTube videos as MP4 files using a modern GUI (CustomTkinter) and reliable backend (yt-dlp + FFmpeg).

**Key Design Goal**: Clean separation of concerns to enable future vocal removal (karaoke) enhancement without touching GUI or core downloader.

## Architecture

### High-Level Flow

```
User Input (URL + Folder)
        ↓
[GUI] Validate Input
        ↓
[Core] Download Manager
    ├─ Fetch Video Metadata
    ├─ Download Video + Audio (parallel streams)
    ├─ Emit Progress Updates
    └─ Merge via FFmpeg → MP4
        ↓
[GUI] Display Status / Error Handling
```

### Module Organization

#### `src/core/` - Core Business Logic (No UI Dependency)

| Module | Responsibility |
|--------|-----------------|
| `downloader.py` | yt-dlp wrapper, download orchestration, progress events |
| `validators.py` | URL validation, path/filename safety, disk space checks |
| `config.py` | Persistent settings (output folder, theme, retries) |
| `errors.py` | Normalized exception types (FFmpegError, GeoRestrictedError, etc.) |
| `postprocess_base.py` | **Extension interface** for future post-processing (e.g., vocal removal) |

**Design Principle**: Core modules have zero dependency on GUI framework. They can be tested in isolation or reused in CLI/server contexts.

#### `src/gui/` - User Interface

| Module | Responsibility |
|--------|-----------------|
| `main_window.py` | CustomTkinter main window, event handlers, threading |

**Design Principle**: GUI receives events from `DownloadManager` (progress, errors) via callbacks. All blocking operations run in background threads to keep UI responsive.

#### `main.py` - Application Entry Point

Simple bootstrap that imports and launches the GUI.

---

## Implementation Details

### 1. Download Manager (`src/core/downloader.py`)

**Class: `DownloadManager`**

```python
class DownloadManager:
    def __init__(self, output_dir: Path) -> None
    def fetch_video_info(self, url: str) -> Dict  # Metadata without download
    def download(self, url: str, on_progress: Callable) -> str  # Download & return path
    def cancel_download(self) -> None  # Request cancellation
    def cleanup_partial_downloads(self, filename: str) -> None  # Clean failed files
```

**Key Features:**

- **Format Selection**: `bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/...`
  - Prioritizes best quality video + best audio in MP4 container
  - Falls back to best single-stream if separate video/audio unavailable
  - yt-dlp automatically invokes FFmpeg to merge streams

- **Progress Callback**: YoutubeDL hook emits dict:
  ```python
  {
      'status': 'downloading',
      'downloaded_bytes': X,
      'total_bytes': Y,
      'speed': Z,
      'eta': T,
  }
  ```

- **Error Normalization**: Raw yt-dlp exceptions mapped to domain types:
  - `YouTubeError` (generic extraction/download failure)
  - `FFmpegError` (missing or failed postprocessor)
  - `GeoRestrictedError` (regional block detected)
  - `NetworkError` (timeout, connection loss)

- **FFmpeg Requirement**: Checked at init time. Clear error message if missing.

### 2. Validators (`src/core/validators.py`)

**Functions:**

```python
is_valid_youtube_url(url: str) -> bool
    # Regex match for youtube.com/watch?v=ID or youtu.be/ID

check_disk_space(path: Path, estimated_size_mb: int) -> bool
    # Verify free space + 10% safety margin

sanitize_filename(filename: str) -> str
    # Replace Windows-invalid chars (< > : " / \ | ? *)

validate_output_directory(path: Path) -> bool
    # Ensure directory writable; create if missing
```

**Why Separate?**: Testable logic independent of download/UI.

### 3. Configuration (`src/core/config.py`)

**Class: `ConfigManager`**

Persistent JSON-based settings:
```json
{
  "output_dir": "/home/user/Downloads",
  "theme": "dark",
  "max_retries": 3,
  "socket_timeout": 30
}
```

**Benefits:**
- Remembers last output folder (convenience without forcing it)
- Allows future UI settings panel
- Graceful fallback to defaults on load error

### 4. GUI Main Window (`src/gui/main_window.py`)

**Class: `MainWindow(ctk.CTk)`**

**Layout:**
```
┌─────────────────────────────────────┐
│  YouTube MP4 Downloader             │
│                                     │
│  ⚠️ Legal disclaimer (brief)       │
│                                     │
│  URL Input: [________________________] │
│                                     │
│  Save to: [__________] [Browse...]  │
│                                     │
│  [         Download              ]  │
│                                     │
│  Progress: [===========  50%   ]    │
│  Status: Downloading 50MB/100MB     │
│                                     │
│  Log:                               │
│  ├ Fetching video info...           │
│  ├ Title: Example Video             │
│  └ Starting download...             │
│                                     │
│  FFmpeg install reminder (footer)   │
└─────────────────────────────────────┘
```

**Threading Model:**

```
Main Thread (Tkinter Event Loop)
    ├─ Handle button clicks
    ├─ Update UI (label, progress bar)
    └─ Show dialogs (errors, success)

Background Thread (DownloadManager)
    ├─ Download video
    ├─ Emit progress callbacks
    └─ Handle errors
    
[Thread-Safe] Callback Queue
    ├ Progress updates → after(0, update_progress)
    └ Errors → after(0, show_error)
```

**Key Patterns:**

- **Disable/Enable Controls**: During download, URL entry and Download button disabled (prevent double-click, accidental input changes)
- **Safe Callbacks**: All GUI updates via `self.after(0, func, args)` from background thread to avoid race conditions
- **Error Dialogs**: Native `messagebox.showerror()` with actionable guidance

### 5. Extension Interface for Future Enhancements

**Class: `PostProcessorBase` (`src/core/postprocess_base.py`)**

```python
class PostProcessorBase(ABC):
    @abstractmethod
    def process(self, video_path: Path) -> Path:
        """Apply post-processing (e.g., vocal removal)."""
        pass
    
    def is_available(self) -> bool:
        """Check if dependencies are available."""
        return False
```

**Future Integration** (not implemented in MVP):

```python
# In DownloadManager.download():
output_file = self.download(url, on_progress)  # → MP4

# Optionally apply post-processor
if self.postprocessor.is_available():
    output_file = self.postprocessor.process(output_file)

return output_file
```

This design allows:
1. Drop-in `VocalRemover(PostProcessorBase)` subclass
2. No changes to GUI event handlers
3. No changes to `DownloadManager` public API
4. Optional feature: user can disable/enable via config

---

## Technology Stack

| Component | Choice | Why |
|-----------|--------|-----|
| GUI | CustomTkinter | Modern, lightweight, native file dialogs, minimal dependencies |
| Downloader | yt-dlp | Actively maintained, handles YouTube changes, robust error handling |
| Audio/Video Merge | FFmpeg | Industry standard, lossless merge, MP4 compatibility |
| Config | JSON + pathlib | Simple, human-readable, no external DB needed |
| Threading | Python threading | Built-in, simple use case, no async complexity |
| Testing | pytest | Standard Python testing, easy mocking |

---

## Error Handling Strategy

| Scenario | Detection | User Message | Recovery |
|----------|-----------|--------------|----------|
| Invalid URL | Regex validation before download | "Please enter a valid YouTube URL: https://..." | Retry with correct URL |
| FFmpeg Missing | `shutil.which("ffmpeg")` at startup | "FFmpeg not found. Install: choco install ffmpeg" | Install FFmpeg, restart app |
| Geo-Restricted | yt-dlp ExtractorError with "geo" keyword | "This video is not available in your region." | Try VPN or different video |
| Network Timeout | yt-dlp DownloadError + socket timeout | "Network timeout. Check connection and retry." | Auto-retry, manual retry |
| Invalid Directory | `Path.mkdir()` or permission test | "Directory is not writable: [path]" | Pick different folder |
| Partial File (crash) | `.part` files left behind | Auto-cleaned on next download attempt | Automatic |

---

## Validation & Testing

### Manual Test Plan (MVP)

1. **Happy Path**: Valid URL → MP4 in chosen folder
   - Test with: https://www.youtube.com/watch?v=dQw4w9WgXcQ
   - Verify file exists and plays in media player

2. **Invalid URL**: Blocked with clear message
   - Test with: `not-a-url`
   - Expected: "Please enter a valid YouTube URL"

3. **FFmpeg Missing**: Actionable guidance
   - Rename/hide FFmpeg temporarily
   - Expected: "FFmpeg not found. Install: choco install ffmpeg"

4. **Network Interruption**: Graceful error
   - Disconnect internet mid-download
   - Expected: "Network timeout. Retry."

5. **Long Video Progress**: Live feedback
   - Download a 1hr+ video
   - Verify progress bar updates, speed displayed

6. **Geo-Restricted Content**: Clear message
   - Test with a known geo-blocked video
   - Expected: "Video is not available in your region"

### Unit Tests (Optional for MVP)

```python
# tests/test_validators.py
def test_is_valid_youtube_url():
    assert is_valid_youtube_url("https://www.youtube.com/watch?v=abc123")
    assert is_valid_youtube_url("https://youtu.be/abc123")
    assert not is_valid_youtube_url("https://example.com")

def test_sanitize_filename():
    assert sanitize_filename("My: Video <2024>") == "My_ Video _2024_"

# tests/test_downloader.py (with mocked yt-dlp)
def test_fetch_video_info_success(mocker):
    mocker.patch('yt_dlp.YoutubeDL.extract_info', return_value={...})
    manager = DownloadManager(Path("/tmp"))
    info = manager.fetch_video_info("https://...")
    assert info['title'] == "Test Video"
```

---

## Future Enhancements

### Phase 4: Vocal Removal (Karaoke Mode)

**Planned Scope** (Post-MVP):

1. **Dependency**: Demucs (source separation model)
   - PyPI: `demucs`
   - Model download: ~250MB
   - Processing time: ~5 min for 1hr video (CPU) or ~30sec (GPU)

2. **Implementation**:
   ```python
   class VocalRemover(PostProcessorBase):
       def __init__(self, output_dir):
           self.model = demucs.load_model('htdemucs')
       
       def process(self, video_path: Path) -> Path:
           # Extract audio → apply vocal removal → merge back
           instrumental_audio = self.model.separate(...)
           return self._merge_instrumental_video(video_path, instrumental_audio)
   ```

3. **UI Changes**:
   - Add checkbox: "Create karaoke version (instrumental only)"
   - If checked: show "Processing vocals..." after download
   - Output: `My Video (instrumental).mp4` alongside original

4. **No Core Changes Needed**: `DownloadManager` already has hook point for `PostProcessorBase`

### Other Possible Enhancements

- **CLI**: `python -m src.cli --url "..." --output "./videos"`
- **Batch Mode**: Download multiple videos from a text file
- **Metadata**: Save video info (title, uploader, date) to JSON alongside file
- **Thumbnails**: Download and embed video thumbnail in MP4 metadata
- **Playlist Support**: Download all videos from a playlist
- **Quality Selector**: UI dropdown for video quality preference
- **Packaging**: PyInstaller `.exe` for Windows distribution

---

## Known Limitations (MVP)

| Limitation | Reason | Workaround |
|-----------|--------|-----------|
| Single video only (no playlists) | Scope constraint for MVP | Download each video separately |
| No pause/resume | Atomic download model | Restart on interruption |
| No quality selector | Format selection automated for best MP4 | Manual use of yt-dlp for advanced options |
| No subtitle download | Out of scope for video MVP | Use yt-dlp directly for subs |
| Offline mode unsupported | YouTube API requires live connection | Must be online |

---

## Security & Privacy

- **No Remote Connections**: App only talks to YouTube (via yt-dlp). No telemetry, no tracking.
- **File Handling**: Filenames sanitized to prevent directory traversal (`../` injection).
- **SSL Verification**: yt-dlp uses urllib with certificate validation (enabled by default).
- **Local Storage**: All downloads stored in user-selected folder. No cloud sync.

---

## Build & Distribution (Future)

### Single-File .exe (Windows)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
# Output: dist/main.exe (~100-150MB with all dependencies)
```

---

## Conclusion

This architecture prioritizes:
1. **Simplicity**: Minimal dependencies, straightforward flow
2. **Extensibility**: Clear interfaces for post-processing
3. **Reliability**: Robust error handling, native GUI
4. **Maintainability**: Separated concerns, testable modules

The MVP is fully functional and production-ready for single-video MP4 downloads. Future enhancements can build on this foundation without major refactoring.
