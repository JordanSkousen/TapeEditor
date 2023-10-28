#!/usr/bin/env python3
"""
Trims the start & ends of videos of digitized tapes (VHS, Hi8, miniDV, etc.)

Usage:
  tape_editor.py edit <dir_or_video_file> --find=<dir_or_image_file> --output=<dir_or_video_file> [--remux]
  tape_editor.py extract <video_file> <timestamp> <output_image>
  tape_editor.py -h | --help

Options:
  -h, --help                Show this screen
  --find DIR/FILE           The image file/directory of image files of example frames to skip (for example, the blue screen before the tape begins). To extract these example frames, use the extract command. Accepted extensions are *.jpg, *.jpeg, *.png, *.bmp.
  --output DIR/FILE         If a single video file is being edited, this is the video file to output to. Otherwise, this is the directory where the edited video files will be output to.
  --remux                   Remux the file to MP4 when editing it.

"""
import os
import io
import subprocess
import docopt
from PIL import Image
import imagehash

from video import Video
from utils import get_files, frame_to_timestamp

def extract(file, timestamp, output):
  print("Extracting frame at", timestamp, "from", file, "and saving it to", output, "...")
  subprocess.call(["ffmpeg", "-y", "-ss", timestamp, "-i", file, "-vframes", "1", "-c:v", "png", output], stderr=open(os.devnull, 'wb'))
  print("Complete!")

def hash_image(im):
  return imagehash.colorhash(im)

def hash_frame(file, timestamp):
  try:
    proc = subprocess.Popen(["ffmpeg", "-y", "-ss", timestamp, "-i", file, "-vframes", "1", "-c:v", "png", "-f", "image2pipe", "-"], stdout=subprocess.PIPE, stderr=open(os.devnull, 'wb'))
    output = proc.stdout.read()
    im = Image.open(io.BytesIO(output))
    return hash_image(im)
  except:
    return None

def search_for_edit_point(find_hashes, video, start_frame, stop_frame, frame_step):
  likely_point = -1
  success_count = 0
  for i in range(start_frame, stop_frame, frame_step):
    ts = frame_to_timestamp(i, video.fps)
    print("\tChecking frame {} (ts={})...".format(i, ts))
    if not str(hash_frame(video.file, ts)) in find_hashes:
      if likely_point == -1:
        likely_point = i
      success_count = success_count + 1
      threshold = (stop_frame - start_frame) // (frame_step * 2)
      if success_count >= min(5, threshold):
        return likely_point
    else:
      likely_point = -1
      success_count = 0
  return stop_frame

def get_edit_point(find_hashes, video, find_start):
  vid_end = video.total_frames - video.fps * 3 # must start at least 3 seconds away from end of video to account for timestamp discrepancies
  start = 0 if find_start else vid_end 
  end = vid_end if find_start else 0
  step = video.fps if find_start else video.fps * 60 * 5
  if not find_start:
    step = -1 * step
  while True:
    print("Finding {} of video \"{}\" (from frames {} - {}, step={})".format("start" if find_start else "end", video.file, start, end, step))
    edit_point = search_for_edit_point(find_hashes, video, start, end, step)
    if (step <= 1 and find_start) or (step >= -1 and not find_start):
      return edit_point
    else:
      start = edit_point - step
      end = edit_point + step
      step = step // 2

def trim_video(video, out_file, start_frame, end_frame, remux):
  start = frame_to_timestamp(start_frame, video.fps)
  end = frame_to_timestamp(end_frame, video.fps)
  print("Trimming video \"{}\" from timestamps {} to {} and saving to \"{}\"...".format(video.file, start, end, out_file))
  args = ["ffmpeg", "-y", "-ss", start, "-i", video.file, "-to", end]
  if not remux:
    args.extend(["-c", "copy"])
  args.append(out_file)
  subprocess.call(args)

def edit(find_dir, edit_dir, out_dir, remux):
  find_files = [find_dir] if os.path.isfile(find_dir) else get_files(find_dir, [".jpg", ".jpeg", ".png", ".bmp"])
  editing_single_file = os.path.isfile(edit_dir)
  edit_files = [edit_dir] if editing_single_file else get_files(edit_dir, [".mkv", ".mp4", ".m4v", ".mov"])

  find_hashes = []
  for pic in find_files:
    im = Image.open(pic)
    find_hashes.append(str(hash_image(im)))
  if len(find_hashes) == 0:
    raise Exception("No image files found in the --find directory!")
  
  for vid_file in edit_files:
    print("Editing \"{}\"...".format(vid_file))
    video = Video(vid_file)
    start = get_edit_point(find_hashes, video, True)
    print("Found start of video \"{}\" is frame {}".format(video.file, start))
    end = get_edit_point(find_hashes, video, False)
    print("Found end of video \"{}\" is frame {}".format(video.file, end))
    fname = os.path.split(video.file)[1]
    trim_video(video, fname if editing_single_file else os.path.join(out_dir, fname), start, end, remux)
    print("Successfully edited \"{}\".".format(video.file))


if __name__ == '__main__': 
  try: 
    args = docopt.docopt(__doc__)
    if args['extract']:
      extract(args['<file>'], args['<timestamp>'], args['<output>'])
    if args['edit']:
      edit(args['--find'], args['<dir_or_video_file>'], args['--output'], args['--remux'])
  except docopt.DocoptExit:
    print(__doc__) 
