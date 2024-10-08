import os
import subprocess
import logging
from celery import shared_task
from .models import Video, Subtitle


@shared_task
def extract_subtitles(video_id):
    video = Video.objects.get(id=video_id)
    video_path = video.file.path
    subtitle_path = f"{video_path.rsplit('.', 1)[0]}.srt"

    logging.info(f"Extracting subtitles from {video_path} to {subtitle_path}")

    # Use ffmpeg to extract subtitles
    result = subprocess.run(
        ["ffmpeg", "-i", video_path, "-map", "0:s:0", subtitle_path],
        capture_output=True,
    )

    if result.returncode != 0:
        logging.error(f"FFmpeg error: {result.stderr.decode()}")
        return "Failed to extract subtitles."

    # Check if the subtitle file was created
    if not os.path.exists(subtitle_path):
        logging.error(f"Subtitle file not found at path: {subtitle_path}")
        return "Subtitle file not found."

    # Try reading the subtitle file
    try:
        with open(subtitle_path, "r") as f:
            lines = f.readlines()
            logging.info(
                f"Successfully read {len(lines)} lines from the subtitle file."
            )

            for i in range(0, len(lines), 4):  # Assuming 4 lines per subtitle entry
                if i + 3 < len(lines):
                    text = lines[i + 2].strip()
                    start_end = lines[i + 1].strip().split(" --> ")
                    if len(start_end) != 2:
                        logging.warning(
                            f"Unexpected format in line: {lines[i + 1].strip()}"
                        )
                        continue

                    start_time = convert_to_seconds(start_end[0].strip())
                    end_time = convert_to_seconds(start_end[1].strip())

                    Subtitle.objects.create(
                        video=video,
                        text=text,
                        start_time=start_time,
                        end_time=end_time,
                        language="en",
                    )
                    logging.info(f"Added subtitle: {text}")

    except FileNotFoundError:
        logging.error(
            f"File not found error while trying to read the subtitle file: {subtitle_path}"
        )
        return "Failed to read subtitle file."
    except Exception as e:
        logging.error(f"Error reading subtitle file: {e}")
        return "Failed to read subtitle file."

    return "Subtitles extracted successfully."


def convert_to_seconds(time_str):
    """Convert subtitle time string (hh:mm:ss,ms) to total seconds."""
    hours, minutes, seconds = time_str.replace(",", ".").split(":")
    return int(hours) * 3600 + int(minutes) * 60 + float(seconds)
