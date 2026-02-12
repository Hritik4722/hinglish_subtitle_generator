def seconds_to_ass_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours}:{minutes:02d}:{secs:05.2f}"


def generate_ass(subtitles, output_path, width, height, style):

    font_size = int(height * style.get("font_size_ratio", 0.05))
    margin_v = int(height * style.get("margin_v_ratio", 0.10))

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {width}
PlayResY: {height}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,
{style.get("font_name", "Poppins")},
{font_size},
{style.get("primary_color", "&H00FFFFFF")},
{style.get("secondary_color", "&H000000FF")},
{style.get("outline_color", "&H00000000")},
{style.get("back_color", "&H64000000")},
{style.get("bold", 1)},
{style.get("italic", 0)},
{style.get("border_style", 1)},
{style.get("outline", 3)},
{style.get("shadow", 0)},
{style.get("alignment", 2)},
{style.get("margin_l", 40)},
{style.get("margin_r", 40)},
{margin_v},
1

[Events]
Format: Layer, Start, End, Style, Text
"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header.replace("\n\n", "\n"))

        for sub in subtitles:
            start = seconds_to_ass_time(sub["start"])
            end = seconds_to_ass_time(sub["end"])
            text = sub["text"].replace("\n", "\\N")

            line = f"Dialogue: 0,{start},{end},Default,{text}\n"
            f.write(line)
