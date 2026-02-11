import whisper
import json

model = whisper.load_model("small")

def transcribe_audio(audio_path: str, audio_text_json_path: str):

    result = model.transcribe(
        audio_path,         
        task="transcribe",
        temperature=0.0,
        beam_size=5,
        initial_prompt=(
            "This audio contains Hinglish speech "
            "(Hindi and English mixed). "
            "Use correct words."
        )
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


