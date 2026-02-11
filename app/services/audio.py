import subprocess
import os

def extract_audio(video_path: str, audio_path: str):

    if not os.path.exists(video_path):
        raise FileNotFoundError("video not found")
    
    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-ar", "1600",
        "-ac", "1",
        audio_path
    ]

    subprocess.run(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True
    )
