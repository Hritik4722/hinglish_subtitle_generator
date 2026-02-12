import math
import re

MAX_CHARS = 32
MAX_LINES = 2
MIN_DURATION = 0.8  


def split_text_into_chunks(text):

    parts = re.split(r'[,\.!?]', text)

    cleaned_parts = [p.strip() for p in parts if p.strip()]

    final_chunks = []

    for part in cleaned_parts:
        if len(part) <= MAX_CHARS:
            final_chunks.append(part)
        else:
            # fallback to word-based split
            words = part.split()
            current = ""

            for word in words:
                if len(current) + len(word) + 1 <= MAX_CHARS:
                    current += (" " if current else "") + word
                else:
                    final_chunks.append(current)
                    current = word

            if current:
                final_chunks.append(current)

    return final_chunks


def segment_creator_mode(segments):
    new_segments = []

    for seg in segments:
        text_chunks = split_text_into_chunks(seg["text"])


        if len(text_chunks) > 1:
            if len(text_chunks[-1].split()) <= 2:
                text_chunks[-2] += " " + text_chunks[-1]
                text_chunks.pop()

        chunk_count = len(text_chunks)

        if chunk_count == 0:
            continue

        total_duration = seg["end"] - seg["start"]
        duration_per_chunk = total_duration / chunk_count

        current_start = seg["start"]

        for i, chunk in enumerate(text_chunks):

            if i == chunk_count - 1:
                new_end = seg["end"]
            else:
                new_end = current_start + duration_per_chunk

            new_segments.append({
                "start": round(current_start, 2),
                "end": round(new_end, 2),
                "text": chunk
            })

            current_start = new_end

    return new_segments
