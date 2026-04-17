# YouTube MP4 Downloader - User Manual

Welcome! This guide explains how to use YouTube MP4 Downloader.

## Quick Start (5 Steps)

1. **Open** the application
2. **Paste** a YouTube URL
3. **Click** "Load Video Info & Qualities"
4. **Select** quality (or use "Best (Auto)")
5. **Click** "Download"

That's it! 🎬

---

## How to Use - Detailed Guide

### Step 1: Paste a YouTube URL

Copy a YouTube link and paste it into the **URL field**:

**Valid formats:**
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- With parameters: `https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=10s`

**Where to get links:**
1. Open YouTube in your web browser
2. Find a video you want to download
3. Copy the URL from the address bar
4. Paste into the application URL field

### Step 2: Load Video Info

Click the **"Load Video Info & Qualities"** button to:
- ✓ Verify the video is accessible
- ✓ See the title, duration, and uploader
- ✓ Detect available video resolutions
- ✓ Check if download is possible

**What you'll see:**
- Video title
- Duration (in minutes)
- Uploader name
- Available quality options dropdown
- Preview information in the log

### Step 3: Select Quality (Optional)

The application shows available video resolutions:
- **1080p (Full HD)** - Best quality, larger file
- **720p (HD)** - Good balance, medium file
- **480p (SD)** - Small file, lower quality
- **Best (Auto)** - Recommended (default selection)

**How to choose:**
- **Best (Auto):** Always select this if unsure
- **High quality:** Choose 1080p for videos you'll watch on large screens
- **Save space:** Choose 480p or 720p if storage is limited
- **Faster download:** Lower quality downloads faster

**File sizes (rough estimates):**
- 1080p (Full HD): ~500MB-1GB per hour
- 720p (HD): ~250-500MB per hour
- 480p (SD): ~100-250MB per hour

### Step 4: Choose Save Location

**Default location:** `C:\Users\YOUR_USERNAME\Downloads`

**To change where videos are saved:**
1. Click the **"Browse"** button
2. Select a different folder
3. Click "Select Folder"
4. Next download will use the new location

**Recommended locations:**
- Videos folder: `C:\Users\YOUR_USERNAME\Videos`
- External drive: For large collections
- Cloud sync folder: For automatic backup (Dropbox, OneDrive, etc.)

**Check free space:**
- Before downloading, verify you have enough disk space
- The app shows download progress and estimated time

### Step 5: Download

Click the **"Download"** button:

**What happens:**
- Progress bar appears showing:
  - Download speed (MB/s)
  - Estimated time remaining
  - Percentage complete
- Log window shows real-time status
- Video automatically saves as MP4 when complete

**Download times (typical):**
- Short video (5 min): 30 seconds - 2 minutes
- Medium video (30 min): 1-5 minutes
- Long video (1-2 hours): 5-15 minutes

**Speed depends on:**
- Your internet connection
- Video quality selected
- YouTube server speed
- Your computer's performance

---

## Video Quality Explained

### What the app shows
The application displays all available resolutions detected from the video. However, it always downloads using yt-dlp's proven "best format" selector for maximum compatibility.

### Quality vs. File Size

| Quality | Resolution | File Size (per hour) | Best For |
|---------|-----------|----------------------|----------|
| 1080p (Full HD) | 1920×1080 | 500MB - 1GB | TV/Monitor viewing |
| 720p (HD) | 1280×720 | 250-500MB | Computer/Phone |
| 480p (SD) | 854×480 | 100-250MB | Mobile, limited storage |
| Best (Auto) | Varies | Auto-optimized | Recommended |

### Choosing Quality

**Pick 1080p if:**
- You have fast internet (10+ Mbps)
- You have plenty of disk space (500GB+)
- You'll watch on a large screen (TV, monitor)
- You want the best possible quality

**Pick 720p if:**
- You have moderate internet (5+ Mbps)
- You have limited disk space
- You'll watch on a computer
- You want a good balance

**Pick 480p if:**
- You have slow internet (<5 Mbps)
- You have very limited disk space
- You'll watch on a phone
- You just need to see the content

**Always use "Best (Auto)" if:**
- You're unsure which to choose
- You want the app to decide based on the video

---

## Troubleshooting

### Video URL Invalid / Not Found

**Symptoms:** Error message appears when clicking "Load Video Info"

**Causes & Solutions:**

**1. It's not a YouTube URL**
- ✗ `https://vimeo.com/123456`
- ✗ `https://dailymotion.com/video`
- ✓ `https://youtube.com/watch?v=...`
- ✓ `https://youtu.be/...`

**2. Video is deleted or private**
- Check if link works in your browser
- If video is private, only the uploader can access it
- If deleted, no one can download it

**3. Video is age-restricted**
- Log in to YouTube in your browser first
- Some age-restricted videos cannot be downloaded

**4. Video is geo-blocked**
- Some videos only available in specific countries
- Use a VPN to access (if legal in your country)
- Check error message for details

**5. Wrong URL format**
- ✗ `youtube.com` (missing https://)
- ✗ `youtube.com/user/USERNAME` (channel, not video)
- ✗ `youtube.com/watch?v=dQw4w` (incomplete ID)
- ✓ `https://youtube.com/watch?v=dQw4w9WgXcQ`

### Download Takes Too Long

**Normal behavior:**
- 1-hour video at 720p takes 5-15 minutes
- Speed varies based on internet and server

**To speed up:**

**1. Select lower quality**
- Try 480p instead of 1080p
- Smaller files download faster

**2. Check internet speed**
- Open Command Prompt
- Type: `ping google.com`
- If > 100ms latency, connection is slow

**3. Try different time**
- Download during off-peak hours
- Evenings/weekends are slower
- Try early morning or midday

**4. Close other apps**
- Close browsers, streaming apps, downloads
- Free up bandwidth

**5. Check YouTube server**
- Try a different video
- If all videos are slow, it's your internet

### Downloaded File is Corrupted

**Symptoms:** 
- Video plays but has no sound
- Video is choppy or pixelated
- Media player can't open the file

**Solutions:**

**1. Delete and redownload**
- Find the corrupted .mp4 file
- Delete it
- Click "Download" again

**2. Verify the video quality**
- Try downloading at lower quality
- Some original videos have poor quality

**3. Try a different video**
- If problem persists, try another YouTube video
- If that works, the original video might have issues

**4. Check your disk**
- Low disk space can cause corruption
- Free up space and try again

### Can't Find Downloaded File

**Symptoms:** 
- Download completed but can't locate file
- "Where did my video go?"

**Solutions:**

**1. Check the save location**
- Look in the folder shown in "Save to" field
- Default: `C:\Users\YOUR_USERNAME\Downloads`

**2. Search Windows**
- Click Windows Start button
- Type `.mp4` in search box
- Look for your video by date

**3. Check file explorer history**
- Open File Explorer
- Click "Downloads" folder
- Sort by "Date modified" (newest first)

**4. Look for partially downloaded files**
- Files being downloaded show as `.f16a` or `.tmp`
- These become `.mp4` when complete

### "FFmpeg not found" Error

**Cause:** FFmpeg wasn't installed or PATH not configured

**Solution:**
1. Uninstall the application
2. Reinstall `YouTubeDownloaderSetup.exe` 
3. Right-click, select "Run as administrator"
4. Complete installation

**Verify FFmpeg:**
- Open Command Prompt
- Type: `ffmpeg -version`
- You should see version information

If this doesn't work, see INSTALL.md troubleshooting section.

### "Invalid YouTube URL" When I Know It's Valid

**Solutions:**

1. **Copy-paste error**
   - Don't type URL manually
   - Use copy-paste from browser address bar

2. **Extra spaces**
   - Make sure no extra spaces at beginning/end
   - Select URL in text field, press Ctrl+A then paste

3. **URL has parameters**
   - These are OK: `?v=ID&t=10s&list=PLxxx`
   - Don't remove parts

4. **Playlist vs. single video**
   - App downloads single videos only
   - Don't use playlist URLs
   - Get single video URL instead

---

## Performance Tips

### For Faster Downloads

- **Close other programs** 
  - Web browsers, streaming apps, file downloads
  - Frees up bandwidth

- **Use wired internet**
  - WiFi is slower than ethernet cable
  - Connect directly to router if possible

- **Download during off-peak hours**
  - Early morning: 6-10 AM
  - Midday: 12-3 PM
  - Avoid: 6 PM - 11 PM (peak hours)

- **Select lower quality**
  - 480p downloads 50% faster than 1080p
  - Still looks good on most screens

- **Check your internet speed**
  - Visit speedtest.net
  - Need at least 2 Mbps for smooth downloads
  - 10+ Mbps recommended

### For Better Organization

- **Create folders**
  - Make "Music Videos" folder
  - Make "Tutorials" folder
  - Make "Comedy" folder

- **Rename files after download**
  - Right-click → Rename
  - Use descriptive names
  - Example: "Taylor_Swift_Blank_Space.mp4"

- **Use cloud storage**
  - Save to OneDrive, Google Drive, or Dropbox
  - Automatic backup
  - Access from any device

### For Limited Storage

- **Monitor disk space**
  - Right-click Drive C: → Properties
  - See how much space is free
- **Delete old videos you don't need**
- **Use external drive**
  - Connect USB hard drive
  - Save videos there instead

---

## Advanced: Custom Output Directory

The app remembers your last chosen directory.

**To change where videos save:**
1. Click **"Browse"** button next to "Save to"
2. Navigate to desired folder
3. Click **"Select Folder"**
4. All future downloads use this location

**To move videos later:**
1. Download completes
2. Right-click video file
3. Select "Cut"
4. Navigate to new folder
5. Right-click → "Paste"

---

## Getting Help

### If You Have Problems

**Check these first:**
1. Review troubleshooting section above
2. Verify you have admin rights
3. Check you're using a valid YouTube URL

### Report a Bug

1. Visit: https://github.com/yourusername/YouTubeDownloader/issues
2. Click "New Issue"
3. Include:
   - Error message (copy from log)
   - Video URL (if you can share it)
   - Windows version (Settings → System → About)
   - What you were trying to do
   - Steps to reproduce

### Request a Feature

Have an idea for improvement?
1. GitHub Issues: https://github.com/yourusername/YouTubeDownloader/issues
2. Suggest features
3. Vote on existing requests

---

## Support the Project

**Love the app?** Help make it better!

- ⭐ **Star on GitHub** - Shows your support
- 🐛 **Report bugs** - Help us improve
- 💡 **Suggest features** - Share your ideas
- 🔄 **Share with others** - Tell your friends!

Visit: https://github.com/yourusername/YouTubeDownloader

---

## Legal Reminders

### ⚠️ Important

- **Only download content you own or have permission to download**
- Respect copyright laws and YouTube's Terms of Service
- Some videos may have restrictions

### What You CAN Download
- ✓ Your own videos
- ✓ Creative Commons content
- ✓ Public domain material
- ✓ Content with explicit permission

### What You CANNOT Download
- ✗ Copyrighted music/movies
- ✗ Private videos (you don't own)
- ✗ Live streams (technical limitations)
- ✗ DRM-protected premium content

---

## FAQ

**Q: Is this legal?**
A: The tool is legal. Using it to download copyrighted content without permission is not. Always respect copyright.

**Q: How big are files?**
A: 1 hour of video at 720p = ~300MB. See "Video Quality" section for more details.

**Q: Can I download playlists?**
A: No, this version downloads single videos only. Download videos one by one.

**Q: Can I use this on Mac/Linux?**
A: Currently Windows only. Visit GitHub for updates.

**Q: Where are my videos saved?**
A: Default is your Downloads folder. Check "Save to" field in app.

**Q: Can I edit videos after downloading?**
A: Yes! Use free software like:
  - OBS Studio (screen recording)
  - DaVinci Resolve (video editing)
  - FFmpeg (command line)

**Q: How do I uninstall?**
A: See INSTALL.md → "Uninstall" section

**Q: What if download fails?**
A: Try again! If it keeps failing:
  1. Try different video
  2. Try lower quality
  3. Check internet connection
  4. Restart application
  5. Report issue on GitHub

---

**Happy downloading!** 🎬

For installation help, see **INSTALL.md**
