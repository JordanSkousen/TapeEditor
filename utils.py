import os
import subprocess
import re

def probe(file):
  proc = subprocess.Popen(["ffprobe", "-i", file, "-of", "csv"], stderr=subprocess.PIPE)
  return str(proc.stderr.read())

def get_frame_rate(probe_out):
  return re.findall(r'(\d+)(?: fps)', probe_out)[0]

def get_duration(probe_out):
  return re.findall(r'(?:Duration: )((\d+\:?\.?)+)', probe_out)[0][0]

def get_files(dir):
  for root, dirs, files in os.walk(dir):
    for file in files:
      file = os.path.join(root, file)
      yield file

def frame_to_timestamp(frame_num, fps):
  hr = frame_num // (fps * 3600)
  frame_num = frame_num - hr * fps * 3600
  min = frame_num // (fps * 60)
  frame_num = frame_num - min * fps * 60
  sec = frame_num // fps
  frame_num = frame_num - sec * fps
  return "{}:{}:{}.{}".format(hr, min, sec, str(frame_num / fps)[2:5])