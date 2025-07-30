# utils.py
import os
import subprocess
from moviepy.editor import VideoFileClip
from django.conf import settings


MAX_VIDEO_DURATION = settings.MAX_VIDEO_DURATION  # 最大長（秒）

def compress_and_trim_video(input_path, output_path, max_duration=30, target_bitrate="800k"):
    try:
        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-ss", "0",
            "-t", str(max_duration),
            "-vcodec", "libx264",
            "-b:v", target_bitrate,
            "-preset", "fast",
            "-acodec", "aac",
            "-movflags", "+faststart",
            "-y", output_path
        ]
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"ffmpegエラー: {e}")
        return False