import whisper
import json

model = whisper.load_model("small")

def transcribe_audio(audio_path: str, audio_text_json_path: str,video_language: str):

    result = model.transcribe(
        audio_path,         
        task="transcribe",
        # language=video_language,
        temperature=0.0,
        beam_size=5
    )

    segments =[]
    for seg in result["segments"]:
        segments.append(
            {
                "start": seg["start"],
                "end": seg["end"],
                "text": seg["text"].strip()
            }
        )

    with open(audio_text_json_path,"w",encoding="utf-8") as f:
        json.dump(segments,f,ensure_ascii=False,indent=2)


