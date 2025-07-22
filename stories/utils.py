# utils.py
import os
import subprocess
from moviepy.editor import VideoFileClip
from django.conf import settings

MAX_VIDEO_DURATION = settings.MAX_VIDEO_DURATION  # 最大動画長さ（秒）

def trim_video(input_path, output_path, max_duration=MAX_VIDEO_DURATION):
    """
    動画を max_duration（秒）でトリミングし、output_path に保存
    """
    try:
        clip     = VideoFileClip(input_path)
        end_time = min(max_duration, clip.duration)
        trimmed  = clip.subclip(0, end_time)
        trimmed.write_videofile(output_path, codec="libx264", audio_codec="aac")
        clip.close()
        return True
    except Exception as e:
        print(f"動画トリミングエラー: {e}")
        return False


def compress_video(input_path, output_path, target_bitrate="800k"):
    """
    ffmpegを使用して動画を圧縮する
    """
    try:
        cmd = [
            "ffmpeg",
            "-i", input_path,
            "-vcodec", "libx264",
            "-b:v", target_bitrate,       # 映像のビットレート
            "-preset", "fast",            # 処理速度：ultrafast ~ veryslow
            "-acodec", "aac",
            "-strict", "-2",
            output_path,
            "-y"  # 上書き許可
        ]
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"動画圧縮エラー: {e}")
        return False