import pytube
from youtube_transcript_api import YouTubeTranscriptApi
import re
from typing import Generator


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


def filter_links(text: str) -> list[str]:
    """
    This function filters out the YouTube video links from the raw text.

    Args:
        text (str): The raw text containing the YouTube video links.

    Returns:
        str: The filtered text without the YouTube video links.
    """
    pattern = r"((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu\.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?"
    all_links = re.findall(pattern, text)
    if not all_links:
        return []
    all_correct_links = []
    for link in all_links:
        (
            _,  # protocol
            _,  # subdomain
            domain,
            _,  # path
            video_id,
            query,
            extra,
        ) = link
        if (domain and video_id and query) and (domain and query and extra):
            correct_link = "".join(link)
            correct_link = (
                correct_link[:-1] if correct_link.endswith(".") else correct_link
            )
            all_correct_links.append(correct_link)
    return all_correct_links


def prepare_prompt(raw_text: str) -> str:
    """
    This function extracts the subtitles from a YouTube video and prepares a prompt for the model.

    Args:
        raw_text (str): The raw text containing the YouTube video links.

    Returns:
        str: The prompt containing the extracted subtitles.
    """
    youtube_links = filter_links(raw_text)
    if not youtube_links:
        return None
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
                prompt += body + f"\n</helper_message{idx+1}>\n"
            except Exception:
                prompt += f"<helper_message{idx+1}> ERROR Read the message below to respond {idx+1}.\n"
                body = "Error: Unable to extract subtitles from the video. Hence just respond that either subtitles are disables or this video do not exist anymore"
                prompt += body + f"\n</helper_message{idx+1}>\n"

        prompt_list = make_batches(prompt, 5000)
        return prompt_list

    except Exception:
        return None
