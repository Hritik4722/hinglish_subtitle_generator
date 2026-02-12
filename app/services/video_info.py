import subprocess
import json

def get_video_resolution(video_path):
    command = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "json",
        video_path
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    data = json.loads(result.stdout)
    width = data["streams"][0]["width"]
    height = data["streams"][0]["height"]

    return width, height
