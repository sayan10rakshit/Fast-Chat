import pytube
from youtube_transcript_api import YouTubeTranscriptApi
import re


# def make_batches(text: str, max_words: int) -> list:
#     # Split the text into batches where each batch has a maximum of max_words
#     words = text.split()
#     if len(words) <= max_words:
#         return [text]
#     else:
#         return [
#             " ".join(words[i : i + max_words]) for i in range(0, len(words), max_words)
#         ]


def make_batches(text, max_characters):
    if len(text) <= max_characters:
        return [text]
    else:
        return [
            text[i : i + max_characters] for i in range(0, len(text), max_characters)
        ]


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
                prompt += f"<helper_message{idx+1}> Here is the script of YouTube video no {idx+1}.\n"
                body = " ".join(text["text"] for text in transcript)
                prompt += (
                    body
                    + f"\n<helper_message{idx+1}> Just be on point and do not deviate from what the user asks.\n"
                )
            except Exception:
                prompt += f"<helper_message{idx+1}> ERROR Read the message below to respond {idx+1}.\n"
                body = "Error: Unable to extract subtitles from the video. Hence just respond that either subtitles are disables or this video do not exist anymore"
                prompt += body + f"\n<helper_message{idx+1}>\n"

        prompt_list = make_batches(prompt, 5000)
        return prompt_list

    except Exception:
        return None
