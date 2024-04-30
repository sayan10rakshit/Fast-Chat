import pytube
from youtube_transcript_api import YouTubeTranscriptApi
import re


def prepare_prompt(raw_text: str) -> str:
    """
    This function extracts the subtitles from a YouTube video and prepares a prompt for the model.

    Args:
        raw_text (str): The raw text containing the YouTube video links.

    Returns:
        str: The prompt containing the extracted subtitles.
    """
    pattern = r"(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[a-zA-Z0-9\-\_\=\&]{1,}"
    youtube_links = re.findall(pattern, raw_text)
    prompt = ""

    try:
        for idx, link in enumerate(youtube_links):
            yt = pytube.YouTube(link)
            transcript_obj = YouTubeTranscriptApi()
            try:
                transcript = transcript_obj.get_transcript(
                    yt.video_id, languages=["en"]
                )
                prompt += f"<startoftext{idx+1}> Full raw transcript of YouTube video no {idx+1}.\n"
                body = " ".join(text["text"] for text in transcript)
                prompt += body + f"\n<endoftext{idx+1}>\n"
            except Exception:
                prompt += f"<startoftext{idx+1}> Full raw transcript of YouTube video no {idx+1}.\n"
                body = "Error: Unable to extract subtitles from the video. Hence just respond that either subtitles are disables or this video do not exist anymore"
                prompt += body + f"\n<endoftext{idx+1}>\n"

        return prompt

    except Exception:
        return None
