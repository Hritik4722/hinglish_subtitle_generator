import os
import json

from app.services.audio import extract_audio
from app.services.whisper_stt import transcribe_audio
from app.services.hinglish import convert_hinglish
from app.services.segment import segment_creator_mode
from app.services.ass_generator import generate_ass
from app.services.ffmpeg_render import burn_subtitles
from app.services.video_info import get_video_resolution


def full_pipeline(job_id: str, jobs_dir="jobs"):

    job_path = os.path.join(jobs_dir, job_id)

    if not os.path.isdir(job_path):
        raise FileNotFoundError("Job folder not found")

    video_path = os.path.join(job_path, "input.mp4")
    audio_path = os.path.join(job_path, "audio.wav")
    transcript_path = os.path.join(job_path, "raw.json")
    hinglish_path = os.path.join(job_path, "hinglish.json")
    segmented_path = os.path.join(job_path, "segmented.json")
    ass_path = os.path.join(job_path, "subtitles.ass")
    output_path = os.path.join(job_path, "output.mp4")

    if not os.path.isfile(video_path):
        raise FileNotFoundError("input.mp4 is missing")

    try:
        # Extract Audio
        extract_audio(video_path, audio_path)
        if not os.path.isfile(audio_path):
            raise RuntimeError("Audio extraction failed")

        # Whisper STT
        transcribe_audio(audio_path, transcript_path, "hi")
        if not os.path.isfile(transcript_path):
            raise RuntimeError("Transcription failed")

        # Hinglish Conversion
        with open(transcript_path, "r", encoding="utf-8") as f:
            raw_segments = json.load(f)

        cleaned_segments = convert_hinglish(raw_segments)

        with open(hinglish_path, "w", encoding="utf-8") as f:
            json.dump(cleaned_segments, f, ensure_ascii=False, indent=2)

        # Segmentation
        segmented = segment_creator_mode(cleaned_segments)

        with open(segmented_path, "w", encoding="utf-8") as f:
            json.dump(segmented, f, ensure_ascii=False, indent=2)

        # Get Video Resolution
        width, height = get_video_resolution(video_path)

        # Load Style
        style_path = os.path.join("app", "styles", "minimal.json")

        with open(style_path, "r", encoding="utf-8") as f:
            style_config = json.load(f)

        # Generate ASS
        generate_ass(segmented, ass_path, width, height, style_config)

        if not os.path.isfile(ass_path):
            raise RuntimeError("ASS generation failed")

        # Burn Subtitles
        burn_subtitles(video_path, ass_path, output_path)

        if not os.path.isfile(output_path):
            raise RuntimeError("Video rendering failed")

        return output_path

    except Exception as e:
        raise RuntimeError(f"Pipeline failed: {str(e)}")
