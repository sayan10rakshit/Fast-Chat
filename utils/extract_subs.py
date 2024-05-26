import pytube
from youtube_transcript_api import YouTubeTranscriptApi
import re


# def make_batches(text: str, max_words: int) -> list: # ! Uncomment this function to make batches based on words
#     # Split the text into batches where each batch has a maximum of max_words
#     words = text.split()
#     if len(words) <= max_words:
#         return [text]
#     else:
#         return [
#             " ".join(words[i : i + max_words]) for i in range(0, len(words), max_words)
#         ]


def make_batches(text: str, max_characters: int) -> list[str]:
    """
    Make batches of text with a maximum number of characters.

    Args:
        text (str): The text to split into batches.
        max_characters (int): The maximum number of characters in each batch.

    Returns:
        list[str]: A list of text batches.
    """
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

    pattern = "(https:\\/\\/)?(www\\.|m\\.)?(youtube\\.com\\/|youtu.be\\/)(watch\\?v\\=|shorts\\/)?([a-zA-Z0-9\\-\\_\\?\\=]{1,11})(\\s+)?"
    all_links = re.findall(pattern, text)
    if not all_links:
        return []
    # remove duplicate entries from all_links which have the same 5th element
    final_links = []
    while all_links:
        link = all_links.pop()
        # (
        #     protocol,     idx: 0 eg: https://
        #     subdomain,    idx: 1 eg: www. or m.
        #     domain,       idx: 2 eg: youtube.com or youtu.be
        #     path,         idx: 3 eg: watch?v= or shorts/
        #     video_id,     idx: 4 eg: aFgJh1Kk6jg
        #     _ignore,      idx: 5 eg: any blank space
        # ) = link

        # Check if the video_id is not already present in the final_links and the video_id is not empty
        # Also check if the domain is there in the link
        if (link[4] not in [l[4] for l in all_links]) and link[2]:
            video_type = "shorts" if "shorts" in link[3] else "video"
            final_links.append(("".join(link), video_type))
    return final_links


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
        for idx, (link, video_type) in enumerate(youtube_links):
            yt = pytube.YouTube(link)
            transcript_obj = YouTubeTranscriptApi()
            try:
                transcript = transcript_obj.get_transcript(
                    yt.video_id, languages=["en"]
                )
                prompt += f"<helper_message{idx+1}> Here is the script of YouTube {video_type} no {idx+1}.\n"
                body = " ".join(text["text"] for text in transcript)
                prompt += body + f"\n</helper_message{idx+1}>\n"
            except Exception:
                prompt += f"<helper_message{idx+1}> ERROR Read the message below to respond {idx+1}.\n"
                body = f"Error: Unable to extract subtitles from the {video_type}. Hence just respond that either subtitles are disabled or this {video_type} do not exist anymore"
                prompt += body + f"\n</helper_message{idx+1}>\n"

        prompt_list = make_batches(prompt, 5000)
        return prompt_list

    except Exception:
        return None
