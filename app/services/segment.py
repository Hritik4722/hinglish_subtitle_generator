import re

MAX_CHARS = 32
MIN_DURATION = 1.0  # safer reading time


def split_text_into_chunks(text):
    # Split on natural pauses first
    parts = re.split(r'[,.!?]', text)
    parts = [p.strip() for p in parts if p.strip()]

    chunks = []

    for part in parts:
        if len(part) <= MAX_CHARS:
            chunks.append(part)
        else:
            words = part.split()
            current = ""

            for word in words:
                # Avoid splitting abbreviations like A I
                if len(word) == 1 and current:
                    current += " " + word
                    continue

                if len(current) + len(word) + 1 <= MAX_CHARS:
                    current += (" " if current else "") + word
                else:
                    if current:
                        chunks.append(current)
                    current = word

            if current:
                chunks.append(current)

    return chunks


def merge_small_fragments(chunks):
    if not chunks:
        return chunks

    merged = []
    i = 0

    while i < len(chunks):
        chunk = chunks[i]

        # Merge single-letter or 1-word tiny fragments
        if i > 0 and (len(chunk.split()) <= 1 or len(chunk) <= 3):
            merged[-1] += " " + chunk
        else:
            merged.append(chunk)

        i += 1

    return merged


def segment_creator_mode(segments):
    new_segments = []

    for seg in segments:
        text_chunks = split_text_into_chunks(seg["text"])
        text_chunks = merge_small_fragments(text_chunks)

        if not text_chunks:
            continue

        total_duration = seg["end"] - seg["start"]
        total_words = sum(len(chunk.split()) for chunk in text_chunks)

        current_start = seg["start"]

        for i, chunk in enumerate(text_chunks):
            words_in_chunk = len(chunk.split())

            # Proportional timing based on word count
            duration = (words_in_chunk / total_words) * total_duration

            # Enforce minimum duration
            duration = max(duration, MIN_DURATION)

            # Prevent overflow on last chunk
            if i == len(text_chunks) - 1:
                new_end = seg["end"]
            else:
                new_end = min(current_start + duration, seg["end"])

            new_segments.append({
                "start": round(current_start, 2),
                "end": round(new_end, 2),
                "text": chunk
            })

            current_start = new_end

    return new_segments
