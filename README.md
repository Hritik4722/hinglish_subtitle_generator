# Subtitle Generator API

FastAPI backend that generates burned-in subtitles for uploaded videos.

It supports:
- Step-by-step processing endpoints (`/process`, `/cleanup`, `/segment`, `/ass`, `/render`)
- One-shot full pipeline endpoint (`/run/{job_id}`)

The pipeline is optimized for Hindi speech transcription + Hinglish cleanup, then renders subtitles directly into the output video.

---

## Features

- Upload a video and track it by `job_id`
- Extract mono 16k audio using FFmpeg
- Generate timestamped transcript using Whisper (`small` model)
- Clean/normalize text into natural Hinglish using Gemini
- Split subtitle lines for readability
- Generate `.ass` subtitle file from style config
- Burn subtitles into final `output.mp4`

---

## Project Structure

```text
app/
	main.py                  # FastAPI app + route registration
	routes/
		upload.py              # /upload
		process.py             # /process/{job_id}
		cleanup.py             # /cleanup/{job_id}
		segment.py             # /segment/{job_id}
		ass.py                 # /ass/{job_id}
		render.py              # /render/{job_id}
		full_pipline.py        # /run/{job_id}
	services/
		audio.py               # extract audio via ffmpeg
		whisper_stt.py         # Whisper transcription
		hinglish.py            # Gemini-based text cleanup
		segment.py             # subtitle segmentation
		ass_generator.py       # ASS generation
		ffmpeg_render.py       # burn ASS into video
		video_info.py          # ffprobe resolution detection
	styles/
		minimal.json           # default style used in code
		reels.json             # optional style preset
		bold.json              # currently empty
jobs/
	<job_id>/               # per-job input/output artifacts
```

---

## Processing Flow

1. `POST /upload` stores `input.mp4` in `jobs/<job_id>/`
2. `POST /process/{job_id}`
	 - `audio.wav` from FFmpeg
	 - `raw.json` from Whisper STT
3. `POST /cleanup/{job_id}`
	 - `hinglish.json` from Gemini cleanup/transliteration
4. `POST /segment/{job_id}`
	 - `segmented.json` with shorter subtitle chunks
5. `POST /ass/{job_id}`
	 - `subtitles.ass` using video resolution + style config
6. `POST /render/{job_id}`
	 - `output.mp4` with burned subtitles

Or run everything at once:
- `POST /run/{job_id}`

---

## Prerequisites

- Python 3.10+
- FFmpeg installed and available on `PATH`
	- `ffmpeg`
	- `ffprobe`
- (Optional alternative STT) Sarvam API access

Whisper downloads model weights on first use.

---

## Environment Variables

Create a `.env` file in project root:

```env
GEMINI_API_KEY=your_gemini_api_key
SARVAM_API_KEY=your_sarvam_api_key
```

Notes:
- `GEMINI_API_KEY` is required for `/cleanup` and `/run` (because full pipeline includes cleanup).
- `SARVAM_API_KEY` is only needed if you switch to Sarvam STT manually.

---

## Install & Run

### 1) Create / activate virtual environment

Windows PowerShell:

```powershell
python -m venv venv
& .\venv\Scripts\Activate.ps1
```

### 2) Install dependencies

```powershell
pip install -r requirements.txt
```

### 3) Run server

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Swagger docs:
- `http://127.0.0.1:8000/docs`

---

## API Endpoints

### Health

- `GET /`
	- Response: `{"status": "ok"}`

### Upload

- `POST /upload`
	- Form-data field: `file` (video)
	- Returns: `job_id`

Example:

```bash
curl -X POST "http://127.0.0.1:8000/upload" \
	-F "file=@sample.mp4"
```

### Step-by-step Pipeline

- `POST /process/{job_id}` → creates `audio.wav`, `raw.json`
- `POST /cleanup/{job_id}` → creates `hinglish.json`
- `POST /segment/{job_id}` → creates `segmented.json`
- `POST /ass/{job_id}` → creates `subtitles.ass`
- `POST /render/{job_id}` → creates `output.mp4`

### Full Pipeline

- `POST /run/{job_id}`
	- Executes all steps in sequence
	- Returns output video path on success

---

## Job Output Files

Each job is stored under `jobs/<job_id>/`:

- `input.mp4` (uploaded source)
- `audio.wav` (extracted audio)
- `raw.json` (Whisper transcript)
- `hinglish.json` (cleaned transliterated text)
- `segmented.json` (subtitle-friendly chunks)
- `subtitles.ass` (renderable subtitle script)
- `output.mp4` (final burned subtitle video)

---

## Styling

ASS style presets live in `app/styles/`.

Current behavior:
- Full pipeline uses `app/styles/minimal.json`
- `/ass/{job_id}` route also hardcodes style name to `minimal`

You can edit `minimal.json` to tune:
- font, size ratio
- colors (ASS color format)
- alignment and vertical margin
- bold/outline/background

---

## Error Behavior

Typical failure conditions:
- Job folder or `input.mp4` missing
- `ffmpeg`/`ffprobe` not installed or not on `PATH`
- Missing `GEMINI_API_KEY` for cleanup step
- Whisper model download issues (network/permissions)

Most endpoints return HTTP `404` for missing artifacts; service-level failures raise runtime exceptions.

---

## Known Gaps in Current Codebase

- `app/models/job.py` is empty
- `app/routes/download.py` and `app/routes/status.py` are empty
- `app/styles/bold.json` is empty


These do not block core pipeline execution, but are good cleanup targets.

---

## Quick Test Flow

1. Upload video → get `job_id`
2. Run full pipeline:

```bash
curl -X POST "http://127.0.0.1:8000/run/<job_id>"
```

3. Check generated file:
- `jobs/<job_id>/output.mp4`

---

## License

Add a license file if you plan to publish or distribute this project.
