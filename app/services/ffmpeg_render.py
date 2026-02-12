import subprocess
import os

def burn_subtitles(video_path, ass_path, output_path):

    video_path = os.path.abspath(video_path)
    ass_path = os.path.abspath(ass_path)
    output_path = os.path.abspath(output_path)

    # Escape backslashes, colons, and single quotes for FFmpeg filter syntax
    ass_path_fixed = ass_path.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")

    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vf", f"ass='{ass_path_fixed}'",
        "-c:a", "copy",
        output_path
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise Exception(f"FFmpeg failed: {result.stderr}")
