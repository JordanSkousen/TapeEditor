# TapeEditor

Trims the start & ends of videos of digitized tapes (VHS, Hi8, miniDV, etc.) by searching for the in and out points of a VCR's blue screen (or whatever screen(s) you specify).

## Requirements

* python
* ffmpeg

## Usage

First, you'll need to extract some example frames of what you want to cut out (like a VCR blue screen). Use the following command:

```bash
  python main.py extract <video_file> <timestamp> <output_image>
```
  * `<video_file>`: The video file to extract a frame from.
  * `<timestamp>`: The timestamp of the frame to be extracted. Must be in the format `[HH:]MM:SS[.mm]`, where `HH` is hours, `MM` is minutes, `SS` is seconds, and `mm` is milliseconds.
  * `<output_image>`: Where to save the extracted frame. The output will always be in a PNG format, no matter the output's extension; so it's best to use `.png`.

Try to extract as many frames as you'll need. Even small changes, like "PLAY" onscreen, need to be extracted.

Next, we'll do a "dry run" on your video file(s) to make sure you've extracted the right frames and it's going to trim the video where you want. Use this command to "mark" the in and out points of each video:

```bash
  python main.py mark <dir_or_video_file> --find=<dir_or_image_file>
```
  * `<dir_or_video_file>`: The video file/directory of video files to be marked. Accepted extensions are `*.mkv`, `*.mp4`, `*.m4v`, `*.mov`.
  * `--find=<dir_or_image_file>`: The image file/directory of image files of example frames to skip that you extracted earlier. Accepted extensions are `*.jpg`, `*.jpeg`, `*.png`, `*.bmp`.

After all your videos are marked, the in and out points of each video will be printed. Check to make sure these points are correct; if not, you'll need to extract the in/out frame its marked.

Finally, edit your video file(s) with this command:

```bash
  python main.py edit <dir_or_video_file> --find=<dir_or_image_file> --output=<dir_or_video_file> [--encode-mp4]
```
  * `<dir_or_video_file>`: The video file/directory of video files to be edited. Accepted extensions are `*.mkv`, `*.mp4`, `*.m4v`, `*.mov`.
  * `--find=<dir_or_image_file>`: The image file/directory of image files of example frames to skip. Accepted extensions are `*.jpg`, `*.jpeg`, `*.png`, `*.bmp`.
  * `--output <dir_or_video_file>`: If a single video file is being edited, this is the video file to output to. Otherwise, this is the directory where the edited video files will be output to.
  * `--encode-mp4`: (optional) Encodes the file to MP4 when editing it. If skipped, the file will be remuxed.