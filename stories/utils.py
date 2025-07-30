# utils.py
import os
import subprocess
from moviepy.editor import VideoFileClip
from django.conf import settings


MAX_VIDEO_DURATION = settings.MAX_VIDEO_DURATION  # 最大長さ（秒）

def convert_mov_to_mp4(input_path, output_path):
    """
    .mov → .mp4 に変換（拡張子ではなく中身に依存）
    """
    try:
        cmd = [
            "ffmpeg", "-i", input_path,
            "-vcodec", "libx264",
            "-acodec", "aac",
            "-preset", "ultrafast",
            "-movflags", "+faststart",
            "-y", output_path
        ]
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"MOV変換エラー: {e}")
        return False

def compress_and_trim_video(input_path, output_path, max_duration=MAX_VIDEO_DURATION, target_bitrate="800k"):
    """
    mp4動画をトリミング＋圧縮する（メモリ抑制）
    """
    try:
        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-ss", "0",
            "-t", str(max_duration),
            "-vcodec", "libx264",
            "-b:v", target_bitrate,
            "-preset", "ultrafast",
            "-acodec", "aac",
            "-movflags", "+faststart",
            "-y", output_path
        ]
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"圧縮エラー: {e}")
        return False