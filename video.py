from utils import probe, get_frame_rate, get_duration
import re

class Video:
  def __init__(self, video_file):
    self.file = video_file
    self.probe_out = probe(video_file)
    self.fps = int(get_frame_rate(self.probe_out))
    duration_split = [int(n) for n in re.findall(r'(\d+)', get_duration(self.probe_out))]
    self.total_frames = duration_split[0] * self.fps * 3600 + duration_split[1] * self.fps * 60 + duration_split[2] * self.fps + duration_split[3]

  