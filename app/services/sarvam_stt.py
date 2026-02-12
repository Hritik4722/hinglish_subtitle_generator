from sarvamai import SarvamAI
import os
from dotenv import load_dotenv

load_dotenv()

def sarvam_stt(audio_path: str, audio_text_json_path: str,video_language: str):
    client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))

    # Create batch job — change mode as needed
    job = client.speech_to_text_job.create_job(
        model="saaras:v3",
        mode="translit",
        # language_code="en-IN",
        language_code=video_language,
        with_diarization=True
    )

    # Upload and process files
    audio_paths = audio_path
    job.upload_files(file_paths=[audio_paths])
    job.start()

    # Wait for completion
    job.wait_until_complete()

    # Check file-level results
    file_results = job.get_file_results()

    # Download outputs for successful files
    if file_results['successful']:
        job.download_outputs(output_dir=os.path.dirname(audio_text_json_path))
        print(f"Download complete")

    return file_results