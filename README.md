# TapeEditor

Trims the start & ends of videos of digitized tapes (VHS, Hi8, miniDV, etc.)

## Installation



## Usage

* Edit a video file/directory of video files:
```bash
  tape_editor.py edit <dir|input_video_file> --find <dir|image_file> --output <dir|output_video_file> [--remux]
```
  * *<dir|input_video_file>*: The video file/directory of video files to be edited. Accepted extensions are `*.mkv`, `*.mp4`, `*.m4v`, `*.mov`.
  * *--find <dir|image_file>*: The image file/directory of image files of example frames to skip (for example, the blue screen before the tape begins). To extract these example frames, use the `extract` command (see below). Accepted extensions are `*.jpg`, `*.jpeg`, `*.png`, `*.bmp`.
  * *--output <dir|output_video_file>*: If a single video file is being edited, this is the video file to output to. Otherwise, this is the directory where the edited video files will be output to.
  * *--remux*: (optional) Remux the file to MP4 when editing it.

* Extract a frame from a video file:
```bash
  tape_editor.py extract <video_file> <timestamp> <output_image>
```
  * *<video_file>*: The video file to extract a frame from.
  * *<timestamp>*: The timestamp of the frame to be extracted. Must be in the format `[HH:]MM:SS[.mm]`, where `HH` is hours, `MM` is minutes, `SS` is seconds, and `mm` is milliseconds.
  * *<output_image>*: Where to save the extracted frame. The output will always be in a PNG format, no matter the output's extension; so it's best to use `.png`.

* Show the help screen:
```bash
  tape_editor.py -h | --help
```