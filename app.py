import os
import time
import random
import json
import requests
import base64
from io import BytesIO

import groq
from groq import Groq
from st_audiorec import st_audiorec
import streamlit as st
from PIL import Image

import folium
from folium import IFrame
from folium.features import DivIcon
from streamlit_folium import st_folium

import elevenlabs
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
import asyncio
from concurrent.futures import ThreadPoolExecutor

from utils.extract_subs import prepare_prompt, filter_links
from utils.get_web_results import search_the_web, REGIONS
from utils.get_web_results_serp import get_web_results
from utils.get_location import find_closest_match
from utils.agentic_search import generate_search_strings, agentic_search_crawler

voice_name_to_id = {
    "Jessica": {"id": "cgSgspJ2msm6clMCkdW9", "type": "Conversational"},
    "Matilda": {"id": "XrExE9yKIg1WjnnlVkGX", "type": "Narration"},
    "Lily": {"id": "pFZP5JQG7iQjIQuC4Bku", "type": "Narration"},
    "Alice": {"id": "Xb7hH8MSUJpSbSDYk0k2", "type": "News"},
    "Brian": {"id": "nPczCjzI2devNBz1zQrb", "type": "Narration"},
    "Charlie": {"id": "IKne3meq5aSn9XLyUdCD", "type": "Conversational"},
    "Charlotte": {"id": "XB0fDUnXU5powFXDhCwa", "type": "Characters"},
    "Daniel": {"id": "onwK4e9ZLuTAKqWW03F9", "type": "News"},
    "Dorothy": {"id": "ThT5KcBeYPX3keUQqHPh", "type": "Narration"},
    "Elli": {"id": "MF3mGyEYCl7XYWbV9V6O", "type": "Narration"},
    "Emily": {"id": "LcfcDJNUP1GQjkzn1xUU", "type": "Meditation"},
    "Fin": {"id": "D38z5RcWu1voky8WS1ja", "type": "Characters"},
    "Freya": {"id": "jsCqWAovK2LkecY7zXl4", "type": "Characters"},
    "George": {"id": "JBFqnCBsd6RMkjVDRZzb", "type": "Narration"},
    "Glinda": {"id": "z9fAnlkpzviPz146aGWa", "type": "Characters"},
    "Laura": {"id": "FGY2WhTYpPnrIDTdsKH5", "type": "Social Media"},
    "Michael": {"id": "flq6f7yk4E4fJM5XTYuZ", "type": "Narration"},
    "Nicole": {"id": "piTKgcLEGmPE4e6mEKli", "type": "ASMR"},
    "Ethan": {"id": "g5CIjZEefAph4nQFvHAz", "type": "ASMR"},
}


#! Text to Speech Function using ElevenLabs API
#! -------------------------------------------------------------------------------------------------


def text_to_speech_file(
    text: str, api_key: str, voice_name: str = "Lily (Narration)"
) -> str:
    """
    Generates an audio file from the given text using the ElevenLabs API.

    Args:
        text (str): The text to convert to speech.
        api_key (str): The ElevenLabs API key.
        voice_name (str, optional): The name of the voice to use. Defaults to "Lily (Narration)".

    Returns:
        str: The path to the generated audio file.
    """

    voice_id = voice_name_to_id[voice_name.split(" ")[0]]["id"]

    client = ElevenLabs(
        api_key=api_key,
    )
    response = client.text_to_speech.convert(
        voice_id=voice_id,
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.5,
            style=0.5,
            use_speaker_boost=True,
        ),
    )

    save_file_path = f"agent_audio.mp3"

    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    return save_file_path


# Async wrapper to run text_to_speech_file in a separate thread
async def generate_audio_async(text: str, voice_name: str) -> str:
    """
    Generate audio from text using the ElevenLabs API.

    This is an async wrapper for the text_to_speech_file function.

    Args:
        text (str): The text to convert to speech.
        voice_name (str): The name of the voice to use.

    Returns:
        str: The path to the generated audio file.
    """
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        audio_file_path = await loop.run_in_executor(
            pool,
            text_to_speech_file,
            text,
            st.session_state.elevenlabs_api_key,
            voice_name,
        )
    return audio_file_path


#! End of Text to Speech Function
#! -------------------------------------------------------------------------------------------------

#! Toggle Logic
#! -------------------------------------------------------------------------------------------------


# Define a function to handle the toggling logic
def handle_toggle(toggle_name: str) -> None:
    """
    Handles the toggling logic for the sidebar toggles.

    If one toggle is turned on, the other is turned off.
    Here, the toggles are "use_you_tube" and "search_the_web".

    Args:
        toggle_name (str): The name of the toggle that was changed.
    """
    if toggle_name == "use_you_tube":
        st.session_state.search_the_web = False
        st.session_state.use_audio_input = False
        st.session_state.use_audio_output = False
        st.session_state.show_file_uploader = False
        st.session_state.img_gen = False
    elif toggle_name == "search_the_web":
        st.session_state.use_you_tube = False
        st.session_state.show_file_uploader = False
        st.session_state.img_gen = False
    elif toggle_name == "use_audio_input":
        st.session_state.use_you_tube = False
        st.session_state.show_file_uploader = False
        st.session_state.img_gen = False
    elif toggle_name == "show_file_uploader":
        st.session_state.use_audio_input = False
        st.session_state.use_audio_output = False
        st.session_state.use_you_tube = False
        st.session_state.search_the_web = False
        st.session_state.img_gen = False
    elif toggle_name == "img_gen":
        st.session_state.use_audio_input = False
        st.session_state.use_audio_output = False
        st.session_state.use_you_tube = False
        st.session_state.search_the_web = False
        st.session_state.show_file_uploader = False


def handle_search_toggle(toggle_name: str) -> None:
    if toggle_name == "use_agentic_search":
        st.session_state.use_agentic_search = True
        st.session_state.use_serp_api = False
        st.session_state.use_plain_duckduckgo = False
    elif toggle_name == "use_serp_api":
        st.session_state.use_serp_api = True
        st.session_state.use_agentic_search = False
        st.session_state.use_plain_duckduckgo = False
    elif toggle_name == "use_plain_duckduckgo":
        st.session_state.use_plain_duckduckgo = True
        st.session_state.use_agentic_search = False
        st.session_state.use_serp_api = False


#! End of Toggle Logic
#! -------------------------------------------------------------------------------------------------

#! Image Processing Functions
#! -------------------------------------------------------------------------------------------------


def safe_open_image(file):
    MAX_IMAGE_SIZE = (4000, 4000)
    """Safely open an image file and resize if it's too large."""
    try:
        with Image.open(file) as img:
            # Check if image needs resizing
            if img.size[0] > MAX_IMAGE_SIZE[0] or img.size[1] > MAX_IMAGE_SIZE[1]:
                img.thumbnail(MAX_IMAGE_SIZE, Image.LANCZOS)
            # Convert to RGB if it's not
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")
            return img.copy()
    except Exception as e:
        st.error(f"Error opening image: {str(e)}")
        return None


def compress_image(image, max_size=(800, 800), quality=85):
    """Compress and resize the image, handling alpha channel."""
    img = image.copy()
    img.thumbnail(max_size, Image.LANCZOS)

    # Convert to RGB if the image has an alpha channel
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
        img = background

    buffered = BytesIO()
    img.save(buffered, format="JPEG", quality=quality, optimize=True)
    return Image.open(buffered)


def encode_image(image):
    buffered = BytesIO()
    image.save(buffered, format="JPEG", quality=85, optimize=True)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


#! End of Image Processing Functions
#! -------------------------------------------------------------------------------------------------


#! Functions to generate image
#! -------------------------------------------------------------------------------------------------
def generate_image(
    payload: dict,
    api_key: str,
):
    url = "https://api.prodia.com/v1/sdxl/generate"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Prodia-Key": api_key,
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        job_id = response.json()["job"]
        return job_id
    else:
        st.error(f"Error: {response.status_code} - {response.text}")
        return None


def get_image_url(job_id: str, api_key: str):
    url = f"https://api.prodia.com/v1/job/{job_id}"
    headers = {
        "accept": "application/json",
        "X-Prodia-Key": api_key,
    }

    max_retries = 10
    retry_delay = 2

    for _ in range(max_retries):
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            if data["status"] == "succeeded":
                return data["imageUrl"]
            elif data["status"] == "failed":
                st.error("Image generation failed")
                return None
        elif response.status_code in [400, 401, 402]:
            st.error(f"Error: {response.status_code} - {response.text}")
            return None

        time.sleep(retry_delay)

    st.error("Image generation timed out")
    return None


#! End of Functions to generate image
#! -------------------------------------------------------------------------------------------------


#! Functions to generate maps popup
#! -------------------------------------------------------------------------------------------------
# Function to generate HTML popup with improved aesthetics
def generate_popup(place):
    phone = None
    price = None
    description = None
    operating_hours = None
    try:
        phone = place["phone"]
    except:
        pass
    try:
        price = place["price"]
    except:
        pass
    try:
        description = place["description"]
    except:
        pass
    try:
        operating_hours = f"""
        <ul style="margin: 5px 0; padding-left: 20px; list-style-type: disc;">
            <li><b>Monday:</b> {place['operating_hours']['monday']}</li>
            <li><b>Tuesday:</b> {place['operating_hours']['tuesday']}</li>
            <li><b>Wednesday:</b> {place['operating_hours']['wednesday']}</li>
            <li><b>Thursday:</b> {place['operating_hours']['thursday']}</li>
            <li><b>Friday:</b> {place['operating_hours']['friday']}</li>
            <li><b>Saturday:</b> {place['operating_hours']['saturday']}</li>
            <li><b>Sunday:</b> {place['operating_hours']['sunday']}</li>
        </ul>
        """
    except:
        pass

    return f"""
    <div style="font-family: Arial, sans-serif;">
        <div style="display: flex; flex-direction: row; align-items: flex-start;">
            <div style="flex: 1; padding-right: 10px;">
                <h2 style="margin: 0; color: #2E86C1;">{place['title']}</h2>
                <p style="margin: 10px 0;"><b>Rating:</b> {place['rating']}</p>
                <p style="margin: 10px 0;"><b>Reviews:</b> {place['reviews']}</p>
                <p style="margin: 10px 0;"><b>Price:</b> {price}</p>
                <p style="margin: 10px 0;"><b>Type:</b> {place['type']}</p>
                <p style="margin: 10px 0;"><b>Address:</b> {place['address']}</p>
                <p style="margin: 10px 0;"><b>Phone:</b> {phone}</p>
                <p style="margin: 10px 0;"><b>Coordinates:</b> Lat: {place['gps_coordinates']['latitude']}, Lng: {place['gps_coordinates']['longitude']}</p>
                <div style="margin-top: 10px;">
                    <b>Operating Hours:</b>
                    {operating_hours}
                </div>
                <p style="margin: 10px 0;"><b>Description:</b> {description}</p>
            </div>
            <div style="flex-shrink: 0;">
                <img src="{place['thumbnail']}" alt="Thumbnail" style="width: 168px; height: 120px; border-radius: 10px;">
            </div>
        </div>
    </div>
    """


#! End of Functions to generate maps popup
#! -------------------------------------------------------------------------------------------------


#! Function to display media content
#! -------------------------------------------------------------------------------------------------
def show_media(
    role="assistant",
    model_output=None,
    img_links=None,
    video_links=None,
    MARKDOWN_PLACEHOLDER=None,
    audio_file_path=None,
    related_questions=None,
    maps_search_results=None,
) -> (
    None
):  #! This will only be executed (display the media content/s) if either YouTube or Web search is enabled
    """
    This is a function to display all the media contents.

    - Displays prompts/responses.
    - If YouTube integration is enabled, it displays the YouTube video/shorts.
    - If web search integration is enabled, it displays relevant images, videos, references, and related questions.

    Args:
        role (str, optional): The role of the speaker. Defaults to "assistant".
        img_links (list, optional): All the image links extracted from the search results. Defaults to None.
        video_links (list, optional): All the video links extracted from the search results. Defaults to None.
        MARKDOWN_PLACEHOLDER (str, optional): The list of web search references. Defaults to None.
        audio_file_path (str, optional): The path to the audio file generated from the model response. Defaults to None.
        related_questions (list, optional): The list of related questions extracted from the search results. Defaults to None.
        maps_search_results (list, optional): The json data of the maps search results. Defaults to None.
    """

    # ? YOUTUBE VIDEO/SHORTS RESULTS after model response
    # Display the YouTube video/shorts after the response
    main_cols = st.columns([0.6, 0.4])

    if model_output is not None:
        with main_cols[0]:
            # write model output
            with st.chat_message(role):
                st.markdown(model_output)

            if audio_file_path:
                st.audio(
                    audio_file_path,
                    format="audio/mp3",
                    autoplay=True,
                )

        with main_cols[1]:
            # ? WEB SEARCH RESULTS after model response
            # ? Display the images

            if img_links is not None:
                if len(img_links) == 1:
                    st.caption("**Image**")
                    st.image(img_links[0], use_column_width="auto")
                elif len(img_links) == 2:
                    st.caption("**Images from the web**")
                    cols_img = st.columns(2)
                    for idx, img_link in enumerate(img_links):
                        with cols_img[idx % 2]:
                            st.image(img_link, use_column_width="auto")
                elif len(img_links) > 2:
                    st.caption("**Images from the web**")
                    cols_img = st.columns(3)
                    pics_to_show = 3 if len(img_links) > 3 else len(img_links)

                    # Show the initial set of images
                    for idx, img_link in enumerate(img_links[:pics_to_show]):
                        with cols_img[idx % 3]:
                            st.image(img_link, use_column_width="auto")

                    # Show additional images under the expander if there are any
                    if len(img_links) > pics_to_show:
                        with st.expander("View more images"):
                            more_cols = st.columns(3)
                            for idx, img_link in enumerate(img_links[pics_to_show:]):
                                with more_cols[idx % 3]:
                                    st.image(
                                        img_link,
                                        use_column_width="auto",
                                    )

            # ? Display the videos
            if video_links is not None:
                if len(video_links) == 1:
                    st.caption("**Video from the web**")
                    try:
                        st.video(video_links[0][0], start_time=0)
                    except Exception as e:
                        print(e)
                if len(video_links) > 1:
                    st.caption("**Videos from the web**")
                    cols_vids = st.columns(2)
                    videos_to_show = 2 if len(video_links) > 2 else len(video_links)
                    for idx, (video_link, _) in enumerate(video_links[:videos_to_show]):
                        with cols_vids[idx % 2]:
                            try:
                                st.video(video_link, start_time=0)
                            except Exception as e:
                                print(e)
                    # Show additional videos under the expander if there are any
                    if len(video_links) > videos_to_show:
                        with st.expander("View more videos"):
                            more_cols = st.columns(2)
                            for idx, (video_link, _) in enumerate(
                                video_links[videos_to_show:]
                            ):
                                with more_cols[idx % 2]:
                                    try:
                                        st.video(video_link, start_time=0)
                                    except Exception as e:
                                        print(e)

            if MARKDOWN_PLACEHOLDER is not None:
                with st.expander("Sources from the web"):
                    st.markdown(MARKDOWN_PLACEHOLDER)

        # ? Display the maps search results
        if maps_search_results is not None:
            try:
                map_data = json.loads(maps_search_results)
                data = map_data["local_results"]
                # Create a map centered at the first place's coordinates with a dark theme
                m = folium.Map(
                    location=[
                        data[0]["gps_coordinates"]["latitude"],
                        data[0]["gps_coordinates"]["longitude"],
                    ],
                    zoom_start=14,
                    tiles="cartodbdark_matter",
                )

                for place in data:
                    popup_html = generate_popup(place)
                    iframe = IFrame(popup_html, width=500, height=300)
                    popup = folium.Popup(iframe, max_width=500)

                    # Add a place name with a high-visibility color and no overlapping
                    folium.Marker(
                        location=[
                            place["gps_coordinates"]["latitude"],
                            place["gps_coordinates"]["longitude"],
                        ],
                        icon=DivIcon(
                            icon_size=(200, 36),
                            icon_anchor=(0, 0),
                            html=f"""
                            <div style="
                                display: inline-block; 
                                font-size: 14px; 
                                color: #FFD700;  /* Gold color for high visibility */
                                background-color: rgba(0, 0, 0, 0.7); 
                                padding: 5px 10px; 
                                border-radius: 8px; 
                                border: 2px solid #FFD700;
                                white-space: nowrap;
                                max-width: 200px;  
                                overflow: hidden;
                                text-overflow: ellipsis;">
                                {place["title"]}
                            </div>
                            """,
                        ),
                    ).add_to(m)

                    # Add marker with popup
                    folium.Marker(
                        location=[
                            place["gps_coordinates"]["latitude"],
                            place["gps_coordinates"]["longitude"],
                        ],
                        popup=popup,
                        icon=folium.Icon(color="lightgray", icon="info-sign"),
                    ).add_to(m)

                # Fit map to bounds of all markers
                locations = [
                    [
                        place["gps_coordinates"]["latitude"],
                        place["gps_coordinates"]["longitude"],
                    ]
                    for place in data
                ]
                m.fit_bounds(locations)

                with st.container():
                    # Render map in Streamlit
                    st_folium(m, width=725)
                    if map_data["search_metadata"]["google_maps_url"]:
                        st.markdown(
                            '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">',
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            f"<i class='fab fa-google'></i>&nbsp;&nbsp;&nbsp;[View on Google Maps]({map_data['search_metadata']['google_maps_url']})",
                            unsafe_allow_html=True,
                        )

            except Exception as e:
                print(e)

        # ? Display additional related questions and their results
        if related_questions is not None:
            st.markdown("### Related Questions")
            for question in related_questions:
                with st.expander(question["question"]):
                    if "thumbnail" in question:
                        if "title" in question:
                            st.markdown(f"**{question['title']}**")
                        col1, col2 = st.columns([5, 1])
                        if "thumbnail" in question:
                            col2.image(question["thumbnail"])
                        if "snippet" in question:
                            col1.write(question["snippet"])
                        if "link" in question:
                            if "source_logo" in question:
                                # Show the source logo inside markdown just before the link
                                col1.markdown(
                                    f"![source]({question['source_logo']})  [{question['displayed_link']}]({question['link']})"
                                )
                            else:
                                col1.markdown(
                                    f"[{question['displayed_link']}]({question['link']})"
                                )
                    else:
                        if "title" in question:
                            st.markdown(f"**{question['title']}**")
                        if "snippet" in question:
                            st.write(question["snippet"])
                        if "link" in question:
                            if "source_logo" in question:
                                # Show the source logo inside markdown just before the link
                                st.markdown(
                                    f"![source]({question['source_logo']})  [{question['displayed_link']}]({question['link']})"
                                )
                            else:
                                st.markdown(
                                    f"[{question['displayed_link']}]({question['link']})"
                                )


#! End of Function to display media content
#! -------------------------------------------------------------------------------------------------


def sidebar_and_init() -> tuple:
    """
    Defines the sidebar and initializes the session state variables.

    Returns:
        model (str): The model selected by the user.
        temperature (float): The temperature for calculating the softmax probabilities in the final layer.
        max_tokens (int): The maximum tokens allowed in the response.
        top_p (float): The top p cumulative probability tokens to consider in each step of the sampling process.
        region (str): The region selected by the user.
        max_results (int): The maximum results to refer from the search.
        audio_data (bytes): The audio data recorded by the user.

    """
    model = None
    temperature = None
    max_tokens = None
    top_p = None
    region = None
    max_results = None
    audio_data = None

    # ! Declaring all the session state variables

    if "fast_chat_instructions" not in st.session_state:
        st.session_state.fast_chat_instructions = """
        CONFIDENTIAL INFO, do not share with anyone.
        You are Fast Chat, a powerful AI assistant that can help you with a variety of tasks.
        You can: 
        1) Summarize YouTube videos/shorts having English subtitles if the user just provides the link.
        2) Conduct a web search and include latest information in the response.
        3) Listen to the user via audio input and respond with audio output.        
        """

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "display_message" not in st.session_state:
        st.session_state.display_message = []

    if "groq_api_key" not in st.session_state:
        st.session_state.groq_api_key = ""

    if "is_groq_api_key_valid" not in st.session_state:
        st.session_state.is_groq_api_key_valid = False

    if "page_reload_count" not in st.session_state:
        st.toast("Enter your GROQ API key to get started", icon="⚡")
        placeholder_messages = random.choice(
            [
                "What's on your mind?",
                "Ask me anything!",
                "Let me summarize a YouTube video/shorts for you.",
                "What's up?",
                "YT Video/Shorts summary? I'm here!",
                "Just ask!",
                "Vent out your thoughts!",
            ]
        )
        st.session_state.page_reload_count = 0

        st.session_state.display_message.append(
            {
                "role": "assistant",
                "content": placeholder_messages,
                "media": {
                    "audio_file_path": None,
                    "img_links": None,
                    "video_links": None,
                    "MARKDOWN_PLACEHOLDER": None,
                    "related_questions": None,
                    "maps_search_results": None,
                },
            }
        )

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": st.session_state.fast_chat_instructions,
            }
        )

    if "model_output" not in st.session_state:
        st.session_state.model_output = ""

    if "use_audio_input" not in st.session_state:
        st.session_state.use_audio_input = False

    if "use_audio_output" not in st.session_state:
        st.session_state.use_audio_output = False

    if "voice_name" not in st.session_state:
        st.session_state.voice_name = "Lily (Narration)"

    if "st.session_state.audio_file_path" not in st.session_state:
        st.session_state.audio_file_path = None

    if "show_file_uploader" not in st.session_state:
        st.session_state.show_file_uploader = False
    if "successfully_ran" not in st.session_state:
        st.session_state.successfully_ran = False

    if "img_gen" not in st.session_state:
        st.session_state.img_gen = False

    #! Logic to clear the chat history, remove any audio files generated, reinitialize the toggles and reload the page
    if "clear_chat_tracker" not in st.session_state:
        st.session_state.clear_chat_tracker = []

    if "elevenlabs_api_key" not in st.session_state:
        st.session_state.elevenlabs_api_key = ""

    if "is_elevenlabs_api_key_valid" not in st.session_state:
        st.session_state.is_elevenlabs_api_key_valid = False

    if "prodia_api_key" not in st.session_state:
        st.session_state.prodia_api_key = ""

    if "is_prodia_api_key_valid" not in st.session_state:
        st.session_state.is_prodia_api_key_valid = False

    if "use_you_tube" not in st.session_state:
        st.session_state.use_you_tube = False

    if "search_the_web" not in st.session_state:
        st.session_state.search_the_web = False

    if "use_plain_duckduckgo" not in st.session_state:
        st.session_state.use_plain_duckduckgo = False

    if "use_serp_api" not in st.session_state:
        st.session_state.use_serp_api = False

    if "serp_api_key" not in st.session_state:
        st.session_state.serp_api_key = ""

    if "serpapi_location" not in st.session_state:
        st.session_state.serpapi_location = ""

    if "old_user_serpapi_location" not in st.session_state:
        st.session_state.old_user_serpapi_location = ""

    if "use_agentic_search" not in st.session_state:
        st.session_state.use_agentic_search = False

    st.session_state.page_reload_count += (
        1  # will be incremented each time streamlit reruns the script
    )

    if "img_links" not in st.session_state:
        st.session_state.img_links = []
    if "video_links" not in st.session_state:
        st.session_state.video_links = []
    if "related_questions" not in st.session_state:
        st.session_state.related_questions = []
    if "MARKDOWN_PLACEHOLDER" not in st.session_state:
        st.session_state.MARKDOWN_PLACEHOLDER = None

    if "special_message" not in st.session_state:
        st.session_state.special_message = ""
    if "special_message_shown" not in st.session_state:
        st.session_state.special_message_shown = False

    if "special_message2" not in st.session_state:
        st.session_state.special_message2 = ""
    if "special_message2_shown" not in st.session_state:
        st.session_state.special_message2_shown = False
    if "special_message3" not in st.session_state:
        st.session_state.special_message3 = ""
    if "special_message3_shown" not in st.session_state:
        st.session_state.special_message3_shown = False

    st.markdown("# Fast Chat ⚡")
    st.markdown("by **[Sayan Rakshit](https://github.com/sayan10rakshit/Fast-Chat)**")

    #! Iterate over the messages and display them
    for message in st.session_state.display_message:
        show_media(
            role=message["role"],
            model_output=message["content"],
            img_links=message["media"]["img_links"],
            video_links=message["media"]["video_links"],
            MARKDOWN_PLACEHOLDER=message["media"]["MARKDOWN_PLACEHOLDER"],
            audio_file_path=message["media"]["audio_file_path"],
            related_questions=message["media"]["related_questions"],
            maps_search_results=message["media"]["maps_search_results"],
        )

    with st.sidebar:
        #! Only show the input field if the API key is not valid or if some error has occurred
        if (
            st.session_state.groq_api_key == ""
            or not st.session_state.is_groq_api_key_valid
        ):
            groq_api_key = st.text_input("GROQ API Key", type="password")
            if groq_api_key != "":
                st.session_state.groq_api_key = groq_api_key
            st.markdown(
                "[Get your FREE API key!](https://console.groq.com/keys)",
                help="""Since running an LLM is computationally expensive,
                this app uses an API to run the model on the cloud.
                See more details [here](https://wow.groq.com/)""",
            )

        if (
            st.session_state.use_audio_input
        ):  #! Only the models having lesser parameters are used for audio input since they have
            #! higher rate limits
            model = st.selectbox(
                "Select Model",
                [
                    "gemma2-9b-it",
                    "gemma-7b-it",
                    "mixtral-8x7b-32768",
                    "llama-3.2-1b-preview",
                    "llama-3.2-3b-preview",
                    "llama-3.1-8b-instant",
                    "llama3-8b-8192",
                ],
                index=3,
            )
        elif (
            st.session_state.show_file_uploader
            and st.session_state.page_reload_count == 1
        ) or (
            st.session_state.show_file_uploader
            and not st.session_state.successfully_ran
        ):
            #! Just show Llama 3.2 (for vision) only if one of the following conditions are met
            #!  - If the user has uploaded a file and this is the first time the page is being loaded OR
            #!  - If the user has uploaded a file and the model has not successfully run
            #! Thus if the model has successfully run, then the file uploader will be untoggled by default
            #! The user has to untoggle and retoggle the file uploader to run the model again
            model = st.selectbox(
                "Select Model",
                [
                    "llama-3.2-11b-vision-preview",
                    "llama-3.2-90b-vision-preview",
                ],
                index=1,
            )
        else:
            model = st.selectbox(
                "Select Model",
                [
                    "gemma2-9b-it",
                    "mixtral-8x7b-32768",
                    "llama-3.3-70b-specdec",
                    "llama-3.3-70b-versatile",
                    "llama-3.2-1b-preview",
                    "llama-3.2-3b-preview",
                    "llama-3.2-11b-vision-preview",
                    "llama-3.2-90b-vision-preview",
                    "llama-3.1-8b-instant",
                    "llama3-8b-8192",
                    "llama3-70b-8192",
                    "deepseek-r1-distill-llama-70b",
                ],
                index=11,
            )

        if "gemma" in model:
            st.markdown("[**Model by**](https://ai.google.dev/gemma)")
            st.image(
                "https://www.gstatic.com/images/branding/googlelogo/svg/googlelogo_clr_74x24px.svg",
                width=125,
            )

        elif "llama" in model:
            st.markdown("[**Model by**](https://www.llama.com/)")
            st.image(
                "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Meta_Platforms_Inc._logo.svg/320px-Meta_Platforms_Inc._logo.svg.png",
                width=125,
            )

        elif "mixtral" in model:
            st.markdown("[**Model by**](https://mistral.ai/news/mixtral-of-experts/)")
            st.image(
                "https://upload.wikimedia.org/wikipedia/de/thumb/b/b7/Mistral_AI_Logo.png/320px-Mistral_AI_Logo.png",
                width=125,
            )

        if not st.session_state.use_audio_input and not st.session_state.search_the_web:
            temperature = st.slider(
                "Temperature",
                0.0,
                2.0,
                1.0,
                0.01,
                help="0.0 is deterministic, 1.0 is default, 2.0 is very creative",
            )
        else:
            temperature = 1.0  #! Hardcoded to 1.0 for audio input to refrain from sending multiple requests to the API
            st.success(f"{temperature=}")

        if model == "mixtral-8x7b-32768" and st.session_state.use_audio_input:
            max_tokens = 32768  #! Hardcoded to 32768 for audio input to refrain from sending multiple requests to the API
            st.success(f"{max_tokens=}")
        elif model == "mixtral-8x7b-32768" and not st.session_state.use_audio_input:
            max_tokens = st.slider(
                "Max Tokens", 0, 32768, 1024, help="Max tokens in the response"
            )
        if (
            model == "deepseek-r1-distill-llama-70b"
            and st.session_state.use_audio_input
        ):
            max_tokens = 131072  #! Hardcoded to 32768 for audio input to refrain from sending multiple requests to the API
            st.success(f"{max_tokens=}")
        elif (
            model == "deepseek-r1-distill-llama-70b"
            and not st.session_state.use_audio_input
        ):
            max_tokens = st.slider(
                "Max Tokens", 0, 131072, 32768, help="Max tokens in the response"
            )
        elif model == "llama-3.3-70b-versatile" and st.session_state.use_audio_input:
            max_tokens = 32768  #! Hardcoded to 32768 for audio input to refrain from sending multiple requests to the API
            st.success(f"{max_tokens=}")
        elif (
            model == "llama-3.3-70b-versatile" and not st.session_state.use_audio_input
        ):
            max_tokens = st.slider(
                "Max Tokens", 0, 32768, 8192, help="Max tokens in the response"
            )
        elif (
            model in ("llama-3.1-8b-instant", "llama-3.1-70b-versatile")
            and not st.session_state.use_audio_input
        ):
            max_tokens = st.slider(
                "Max Tokens", 0, 8000, 1024, help="Max tokens in the response"
            )
        elif (
            model in ("llama-3.1-8b-instant", "llama-3.1-70b-versatile")
            and st.session_state.use_audio_input
        ):
            max_tokens = 8000
            st.success(f"{max_tokens=}")
        elif (
            model
            in (
                "llama-3.2-1b-preview",
                "llama-3.2-3b-preview",
                "llama3-70b-8192",
                "llama3-8b-8192",
                "gemma2-9b-it",
                "gemma-7b-it",
                "llama-3.2-11b-vision-preview",
                "llama-3.2-90b-vision-preview",
                "llama-3.3-70b-specdec",
            )
            and st.session_state.use_audio_input
        ):
            max_tokens = 8192
            st.success(f"{max_tokens=}")
        elif (
            model
            in (
                "llama-3.2-1b-preview",
                "llama-3.2-3b-preview",
                "llama3-70b-8192",
                "llama3-8b-8192",
                "gemma2-9b-it",
                "gemma-7b-it",
                "llama-3.2-11b-vision-preview",
                "llama-3.2-90b-vision-preview",
                "llama-3.3-70b-specdec",
            )
            and not st.session_state.use_audio_input
        ):
            max_tokens = st.slider(
                "Max Tokens", 0, 8192, 1024, help="Max tokens in the response"
            )
        else:
            max_tokens = st.slider(
                "Max Tokens", 0, 8192, 1024, help="Max tokens in the response"
            )

        if not st.session_state.use_audio_input and not st.session_state.search_the_web:
            top_p = st.slider(
                "Top P",
                0.0,
                1.0,
                0.9,
                0.01,
                help="""A stochastic decoding method where the top p cumulative probability tokens (sorted w.r.t. probability)
                are considered in each time step. The top p tokens are sampled randomly.""",
            )
        elif (
            st.session_state.use_agentic_search
            and st.session_state.search_the_web
            and not st.session_state.use_audio_input
        ):
            top_p = 0.9  #! Hardcoded to 0.9 for agentic search
            st.success(f"{top_p=}")
        else:
            top_p = 0.8  #! Hardcoded to 0.8 for audio input to refrain from sending multiple requests to the API

        #! Logic to clear the chat history, remove any audio files generated, reinitialize the toggles and reload the page
        if len(st.session_state.clear_chat_tracker) > 0:
            if st.session_state.clear_chat_tracker[
                -1
            ]:  # ? If the user has cleared the chat in the last refresh
                st.session_state.use_audio_input = False  # ? Un-toggle the audio input

        st.toggle(
            "Audio Input",
            st.session_state.use_audio_input,
            key="use_audio_input",
            on_change=handle_toggle,
            args=("use_audio_input",),
        )

        if st.session_state.use_audio_input:
            #! Logic to clear the chat history, remove any audio files generated, reinitialize the toggles and reload the page
            if (
                len(st.session_state.clear_chat_tracker) > 0
            ):  # ? If running for the first time
                if not st.session_state.clear_chat_tracker[
                    -1
                ]:  # ? If the user has not cleared the chat in the last refresh
                    audio_data = st_audiorec()
                    FILE_NAME = "audio.wav"
                    if audio_data:
                        with st.spinner("Processing the audio..."):
                            with open(FILE_NAME, "wb") as file:
                                file.write(audio_data)
                else:  # ? If the user has cleared the chat in the last refresh then un-toggle the audio input
                    st.session_state.use_audio_input = False

        #! Logic to clear the chat history, remove any audio files generated, reinitialize the toggles and reload the page
        if len(st.session_state.clear_chat_tracker) > 0:
            if st.session_state.clear_chat_tracker[
                -1
            ]:  # ? If the user has cleared the chat in the last refresh
                st.session_state.use_audio_output = (
                    False  # ? Un-toggle the audio output
                )

        st.toggle(
            "Audio Output",
            st.session_state.use_audio_output,
            key="use_audio_output",
            on_change=handle_toggle,
            args=("use_audio_output",),
        )

        if st.session_state.use_audio_output:
            # ! Only show the input field if the API key is not valid or if some error has occurred
            if (
                st.session_state.elevenlabs_api_key == ""
                or not st.session_state.is_elevenlabs_api_key_valid
            ):
                elevenlabs_api_key = st.text_input(
                    "Enter ElevenLabs API Key", type="password"
                )
                if elevenlabs_api_key != "":
                    st.session_state.elevenlabs_api_key = elevenlabs_api_key
                st.markdown(
                    "[Get your FREE API key!](https://elevenlabs.io/app/voice-lab)",
                    help="""Go to My Workspace at the bottom of the left sidebar and 
                    click on the Profile + API Key to get your FREE API key.
                    Since generating audio output is computationally expensive,
                    this app uses an API to generate audio output.
                    See more details [here](https://elevenlabs.io/)""",
                )

            _ = st.selectbox(
                "Select Voice",
                [
                    f"{agent_name} ({voice_name_to_id[agent_name]['type']})"
                    for agent_name in voice_name_to_id.keys()
                ],
                index=2,
                key="voice_name",
                help="Select the voice for the audio output.",
            )

        #! Logic to clear the chat history, remove any audio files generated, reinitialize the toggles and reload the page
        if len(st.session_state.clear_chat_tracker) > 0:
            if st.session_state.clear_chat_tracker[-1]:
                st.session_state.use_you_tube = (
                    False  # ? Un-toggle the YouTube integration
                )

        st.toggle(
            "Use YouTube",
            st.session_state.use_you_tube,
            key="use_you_tube",
            on_change=handle_toggle,
            args=("use_you_tube",),
        )

        #! Logic to clear the chat history, remove any audio files generated, reinitialize the toggles and reload the page
        if len(st.session_state.clear_chat_tracker) > 0:
            if st.session_state.clear_chat_tracker[-1]:
                st.session_state.search_the_web = (
                    False  # ? Un-toggle the web search integration
                )

        st.toggle(
            "Search the Web",
            st.session_state.search_the_web,
            key="search_the_web",
            on_change=handle_toggle,
            args=("search_the_web",),
        )

        if len(st.session_state.clear_chat_tracker) > 0:
            if st.session_state.clear_chat_tracker[-1]:
                st.session_state.use_plain_duckduckgo = (
                    False  # ? Un-toggle the plain duckduckgo search
                )

        if len(st.session_state.clear_chat_tracker) > 0:
            if st.session_state.clear_chat_tracker[-1]:
                st.session_state.use_serp_api = False  # ? Un-toggle the serp api search

        if len(st.session_state.clear_chat_tracker) > 0:
            if st.session_state.clear_chat_tracker[-1]:
                st.session_state.use_agentic_search = (
                    False  # ? Un-toggle the agentic search
                )

        # ! No SerpApi Integration for audio input to avoid multiple requests to the API
        # ? Just to reduce the number of requests to the API
        if st.session_state.search_the_web and not st.session_state.use_audio_input:
            region = st.selectbox(
                "Select Region",
                REGIONS,
                index=25,
                help="Select the region to get the search results from.",
            )

            if not st.session_state.use_agentic_search:
                max_results = st.slider(
                    "Max search results to refer",
                    10,
                    30,
                    12,
                    help="More results might take longer to process but will provide more context.",
                )

            st.toggle(
                "DuckDuckGo",
                st.session_state.use_plain_duckduckgo,
                on_change=handle_search_toggle,
                args=("use_plain_duckduckgo",),
                help="Fast and reliable search tool to get quick answers.",
            )

            st.toggle(
                "DeepSearch (Google)",
                st.session_state.use_serp_api,
                on_change=handle_search_toggle,
                args=("use_serp_api",),
                help="The most comprehensive search tool to get more informative answers.",
            )

            agentic_search = st.toggle(
                "DuckDuckGo Agentic (Experimental)",
                st.session_state.use_agentic_search,
                on_change=handle_search_toggle,
                args=("use_agentic_search",),
                help="Most powerful search tool to get more accurate answers. Recommended for paid plans.",
            )

            if agentic_search:
                st.session_state.special_message3 = """
                - **Agentic Search** is an experimental feature and has a long wait time\n
                - Ideal for GROQ paid plans\n
                - **Rate Limit will be more likely to be hit for free plans**\n
                - We highly recommend **llama-3.3-70b-versatile** for **Agentic Search**\n
                """

            # ? SerpApi Integration
            if st.session_state.use_serp_api:
                st.session_state.special_message2 = """
                Though DeepSearch gives more comprehensive search results, it might be pretty slow.\n
                """

                serp_api_key = st.text_input(
                    "SerpApi Key",
                    type="password",
                    help="Enter your SerpApi key to perform DeepSearch.",
                )
                st.markdown(
                    "[Get your FREE SerpApi key!](https://serpapi.com/manage-api-key)",
                    help="""A very powerful API to get comprehensive search results from the web.""",
                )
                if serp_api_key != "":
                    st.session_state.serp_api_key = serp_api_key
                serpapi_location = st.text_input(
                    "Enter location for SerpApi",
                    "Kolkata, West Bengal, India",
                    help="Enter the location to get the search results from.",
                )
                if (  # Only if the user has changed the location then only find the closest match
                    serpapi_location
                    and serpapi_location != st.session_state.old_user_serpapi_location
                ):
                    with st.spinner("Finding the closest match for the location..."):
                        authentic_serpapi_location = find_closest_match(
                            serpapi_location
                        )
                        st.success(f"Using location: {authentic_serpapi_location}")
                        st.session_state.serpapi_location = authentic_serpapi_location
                        st.session_state.old_user_serpapi_location = serpapi_location

            if max_results is not None:
                if max_results >= 20 and model in (
                    "llama3-70b-8192",
                    "llama-3.1-70b-versatile",
                ):
                    st.session_state.special_message = f"""
                    Although {model} is a powerful model, you might get slow responses.\n
                    It is recommended to use other models or to reduce the max search results.\n
                    mixtral-8x7b-32768 is faster and can handle more search results.
                    """

        elif st.session_state.search_the_web and st.session_state.use_audio_input:
            region = st.selectbox(
                "Select Region",
                REGIONS,
                index=25,
                help="Select the region to get the search results from.",
            )

            max_results = 30  # Hardcoded to 30 for audio input to refrain from sending multiple requests to the API

        #! Logic to clear the chat history, remove any audio files generated, reinitialize the toggles and reload the page
        if len(st.session_state.clear_chat_tracker) > 0:
            if st.session_state.clear_chat_tracker[-1]:
                st.session_state.show_file_uploader = (
                    False  # ? Un-toggle the file uploader
                )
        #! Untoggle the file uploader by default if it ran the last time successfully
        if st.session_state.successfully_ran and st.session_state.page_reload_count > 1:
            st.session_state.successfully_ran = False
            st.session_state.show_file_uploader = False

        checkbox_cols = st.columns([0.5, 0.5])
        with checkbox_cols[0]:
            st.checkbox(
                "Attatch Image",
                st.session_state.show_file_uploader,
                key="show_file_uploader",
                on_change=handle_toggle,
                args=("show_file_uploader",),
            )

        #! Logic to clear the chat history, remove any audio files generated, reinitialize the toggles and reload the page
        if len(st.session_state.clear_chat_tracker) > 0:
            if st.session_state.clear_chat_tracker[-1]:
                st.session_state.img_gen = False  # ? Un-toggle the image generation

        with checkbox_cols[1]:
            st.checkbox(
                "Generate Image",
                st.session_state.img_gen,
                key="img_gen",
                on_change=handle_toggle,
                args=("img_gen",),
            )

        if st.session_state.img_gen:
            if (
                st.session_state.prodia_api_key == ""
                or not st.session_state.is_prodia_api_key_valid
            ):
                prodia_api_key = st.text_input(
                    "Enter Prodia API Key",
                    type="password",
                    help="Enter your Prodia API key to generate images.",
                )

                if prodia_api_key != "":
                    st.session_state.prodia_api_key = prodia_api_key
                st.markdown(
                    "[Get your FREE Prodia API key!](https://app.prodia.com/api)",
                    help="""A very powerful API to generate images from text.""",
                )

        if st.button("Clear Chat"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": st.session_state.fast_chat_instructions,
                }
            ]

            st.session_state.display_message = [
                {
                    "role": "assistant",
                    "content": "Let's start afresh shall we? 😁",
                    "media": {
                        "audio_file_path": None,
                        "img_links": None,
                        "video_links": None,
                        "MARKDOWN_PLACEHOLDER": None,
                        "related_questions": None,
                        "maps_search_results": None,
                    },
                }
            ]

            # remove audio.wav from the directory
            if os.path.exists("audio.wav"):
                os.remove("audio.wav")
            if os.path.exists("agent_audio.mp3"):
                os.remove("agent_audio.mp3")

            #! Logic to clear the chat history, remove any audio files generated, reinitialize the toggles and reload the page
            st.session_state.clear_chat_tracker.append(True)

            # reload the page to display the welcome message
            st.rerun()
        else:
            #! Logic to clear the chat history, remove any audio files generated, reinitialize the toggles and reload the page
            st.session_state.clear_chat_tracker.append(False)

        st.markdown("**:gray[Powered by]**")
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Groq_logo.svg/152px-Groq_logo.svg.png",
            width=50,
        )

    # ? Show if model is llama3-70b-8192 and max_results is greater than 20
    if st.session_state.special_message and not st.session_state.special_message_shown:
        st.warning(st.session_state.special_message)
        st.session_state.special_message = ""
        st.session_state.special_message_shown = True

    # ? Show if SerpApi is used
    if (
        st.session_state.special_message2
        and not st.session_state.special_message2_shown
    ):
        st.warning(st.session_state.special_message2)
        st.session_state.special_message2 = ""
        st.session_state.special_message2_shown = True

    if (
        st.session_state.special_message3
        and not st.session_state.special_message3_shown
    ):
        st.warning(st.session_state.special_message3)
        st.session_state.special_message3 = ""
        st.session_state.special_message3_shown = True

    return (
        model,
        temperature,
        max_tokens,
        top_p,
        region,
        max_results,
        audio_data,
    )


def body(
    prompt: str = None,
    encoded_image: str = None,
    payload: dict = None,
    model: str = None,
    temperature: float = None,
    max_tokens: int = None,
    top_p: float = None,
    region: str = None,
    max_results: int = None,
) -> tuple:
    """
    The main body of the app that handles the user input and model response.

    Args:
        prompt (str, optional): The user input. Defaults to None.
        model (str, optional): The model selected by the user. Defaults to None.
        temperature (float, optional): The temperature for calculating the softmax probabilities in the final layer. Defaults to None.
        max_tokens (int, optional): The maximum tokens allowed in the response. Defaults to None.
        top_p (float, optional): The top p cumulative probability tokens to consider in each step of the sampling process. Defaults to None.
        region (str, optional): The region selected by the user. Defaults to None.
        max_results (int, optional): The maximum results to refer from the search. Defaults to None.

    Returns
        -  img_links (list): The list of image links extracted from the search results.
        -  video_links (list): The list of video links extracted from the search results.
        -  MARKDOWN_PLACEHOLDER (str): The markdown placeholder for the search results.
        -  related_questions (list): The list of related questions extracted from the search results.
        -  maps_search_results (str): The search results for the maps search.
        -  model_output (str): The model response.
        -  audio_file_path (str): The path to the audio file generated from the model response.
    """

    GENERIC_RESPONSE = "Sorry, that's on me.\nDue to limited hardware resources in \
                                the free tier, I can't respond to this query.\nPlease try again later or \
                                    upgrade to a paid plan to get more hard.\n\
                                        Let's start afresh shall we? 😁"

    BODY = """"""
    img_links = None
    video_links = None
    MARKDOWN_PLACEHOLDER = None
    related_questions = None
    audio_file_path = None
    model_output = None
    maps_search_results = None

    if (
        prompt and st.session_state.show_file_uploader
    ):  #! Implement Llama 3.2 model for image input
        if st.session_state.groq_api_key == "":
            st.warning("Please enter your GROQ API key.")
        else:
            try:
                if encoded_image:
                    try:
                        show_media(
                            role="user",
                            model_output=prompt,
                        )

                        message = [
                            {
                                "role": "user",
                                "content": [
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{encoded_image}"
                                        },
                                    },
                                    {"type": "text", "text": prompt},
                                ],
                            }
                        ]

                        try:
                            with st.spinner("Processing the image..."):
                                client = Groq(api_key=st.session_state.groq_api_key)
                                chat_completion = client.chat.completions.create(
                                    model=model,
                                    messages=message,
                                    temperature=temperature,
                                    max_tokens=max_tokens,
                                    top_p=top_p,
                                    stream=False,
                                )
                                model_output = chat_completion.choices[
                                    0
                                ].message.content

                                st.session_state.messages.append(
                                    {
                                        "role": "user",
                                        "content": prompt,
                                    }
                                )
                                st.session_state.messages.append(
                                    {
                                        "role": "assistant",
                                        "content": model_output,
                                    }
                                )
                                st.session_state.display_message.append(
                                    {
                                        "role": "user",
                                        "content": prompt,
                                        "media": {
                                            "audio_file_path": None,
                                            "img_links": None,
                                            "video_links": None,
                                            "MARKDOWN_PLACEHOLDER": None,
                                            "related_questions": None,
                                            "maps_search_results": None,
                                        },
                                    },
                                )
                                st.session_state.display_message.append(
                                    {
                                        "role": "assistant",
                                        "content": model_output,
                                        "media": {
                                            "audio_file_path": None,
                                            "img_links": [
                                                f"data:image/jpeg;base64,{encoded_image}"
                                            ],
                                            "video_links": None,
                                            "MARKDOWN_PLACEHOLDER": None,
                                            "related_questions": None,
                                            "maps_search_results": None,
                                        },
                                    }
                                )
                                st.session_state.successfully_ran = True
                                img_links = [f"data:image/jpeg;base64,{encoded_image}"]

                                st.info(
                                    """
                                    - The **Attatch Image** checkbox will be ❌ un-checked automatically.\n
                                    - ❌ Un-check and ✅ Re-check the **Attatch Image** checkbox to attatch your image again.
                                    """,
                                )
                        except groq.RateLimitError:
                            st.session_state.messages = []
                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": "The user has exceeded the rate limit.",
                                }
                            )
                            st.write("You have exceeded the rate limit.")
                            st.session_state.is_groq_api_key_valid = False
                            print("Rate limit error")

                        except groq.AuthenticationError:
                            st.error("Invalid API key.")
                            del st.session_state.groq_api_key
                            del st.session_state.messages
                            del (
                                st.session_state.page_reload_count
                            )  # Display the welcome message again
                            st.session_state.is_groq_api_key_valid = False
                            print("Invalid API key")

                        except groq.BadRequestError:
                            with st.chat_message("assistant"):
                                st.write(GENERIC_RESPONSE)
                                del st.session_state.messages
                            st.session_state.is_groq_api_key_valid = False
                            print("Bad request error")

                        except groq.InternalServerError:
                            with st.chat_message("assistant"):
                                st.write(GENERIC_RESPONSE)
                                del st.session_state.messages
                            st.session_state.is_groq_api_key_valid = False
                            print("Internal server error")

                    except Exception as e:
                        print(e)
                        st.warning(
                            "Somthing went wrong with the image. Please try again."
                        )
                else:
                    st.warning("Please upload an image to proceed.")
            except Exception as e:
                print(e)
                st.error(
                    "Something went wrong with the image processing. Please try again later."
                )

    #! Implement Prodia API for image generation
    elif prompt and st.session_state.img_gen and payload:
        if st.session_state.prodia_api_key:
            show_media(
                role="user",
                model_output=prompt,
            )

            try:
                with st.spinner("Generating the image..."):
                    job_id = generate_image(
                        payload=payload,
                        api_key=st.session_state.prodia_api_key,
                    )
                    if job_id:
                        image_url = get_image_url(
                            job_id, api_key=st.session_state.prodia_api_key
                        )
                        if image_url:
                            st.session_state.is_prodia_api_key_valid = True
                            img_links = [image_url]

                            model_output = f"""
                            ### ✅ Image Generation Successful!
                            
                            **Positive Prompt**: `{payload["prompt"]}`\n
                            **Negative Prompt**: `{payload["negative_prompt"]}`

                            ---
                            
                            #### **Generation Settings**:
                            
                            - **Image Style**: `{payload["style_preset"]}`
                            - **Steps**: `{payload["steps"]}`
                            - **Classifier-Free Guidance Scale (CFG)**: `{payload["cfg_scale"]}`
                            - **Seed**: `{payload["seed"]}`
                            - **Sampler**: `{payload["sampler"]}`
                            - **Width**: `{payload["width"]}`
                            - **Height**: `{payload["height"]}`
                            
                            ---                            
                            
                            Visit the link to view the image 👇\n
                            [{image_url}]({image_url})
                            """

                            st.session_state.messages.append(
                                {
                                    "role": "user",
                                    "content": prompt,
                                }
                            )
                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": model_output
                                    + ". The image is generated successfully and is shown to the user.",
                                }
                            )
                            st.session_state.display_message.append(
                                {
                                    "role": "user",
                                    "content": prompt,
                                    "media": {
                                        "audio_file_path": None,
                                        "img_links": None,
                                        "video_links": None,
                                        "MARKDOWN_PLACEHOLDER": None,
                                        "related_questions": None,
                                        "maps_search_results": None,
                                    },
                                }
                            )
                            st.session_state.display_message.append(
                                {
                                    "role": "assistant",
                                    "content": model_output,
                                    "media": {
                                        "audio_file_path": None,
                                        "img_links": img_links,
                                        "video_links": None,
                                        "MARKDOWN_PLACEHOLDER": None,
                                        "related_questions": None,
                                        "maps_search_results": None,
                                    },
                                }
                            )
                        else:
                            st.error("Failed to generate image")
                            st.session_state.is_prodia_api_key_valid = False
                    else:
                        st.error("Failed to start image generation job")
                        st.session_state.is_prodia_api_key_valid = False
            except Exception as e:
                print(e)
                st.error(
                    "Something went wrong with the image generation. Please try again later."
                )
                st.session_state.is_prodia_api_key_valid = False

        else:
            st.warning("Please enter your Prodia API key.")

    elif (
        prompt
        and not st.session_state.show_file_uploader
        and not st.session_state.img_gen
    ):
        # Add user message to chat history
        if (
            st.session_state.groq_api_key == ""
        ):  # ? Check if the user has not entered the GROQ API key
            st.warning("Please enter your GROQ API key.")
        elif (
            st.session_state.elevenlabs_api_key == ""
            and st.session_state.use_audio_output
        ):  # ? Check if the user has enabled audio output and has not entered the ElevenLabs API key
            st.warning("Please enter your ElevenLabs API key.")
            st.session_state.is_elevenlabs_api_key_valid = False
        else:
            try:
                client = Groq(
                    api_key=st.session_state.groq_api_key,
                )
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.display_message.append(
                    {
                        "role": "user",
                        "content": prompt,
                        "media": {
                            "audio_file_path": None,
                            "img_links": None,
                            "video_links": None,
                            "MARKDOWN_PLACEHOLDER": None,
                            "related_questions": None,
                            "maps_search_results": None,
                        },
                    }
                )

                # ? Display the user message
                show_media(
                    role="user",
                    model_output=prompt,
                )

                # check if the prompt contains a youtube link and user asked something related to the video
                prompt_modified_list = None
                video_links = filter_links(prompt)
                if video_links and st.session_state.use_you_tube:
                    with st.spinner("Seeing the YouTube video/shorts..."):
                        prompt_modified_list = prepare_prompt(prompt)
                        if (
                            prompt_modified_list
                        ):  # only add the modified prompt if subtitles were extracted
                            for prompt_modified in prompt_modified_list:
                                st.session_state.messages.append(
                                    {
                                        "role": "user",
                                        "content": prompt_modified,
                                    }  # add the modified prompt to the chat history
                                )
                        # If subtitles were not extracted, then treat the prompt as a normal prompt

                spinner_message = random.choice(
                    [
                        "Let me think...",
                        "I'm on it...",
                        "I'm working on it...",
                        "I'm thinking...",
                        "Gotcha! Let me think...",
                    ]
                )

                if st.session_state.search_the_web:
                    with st.spinner("Searching the web..."):
                        if (  # ? Deep Search Integration with SerpApi
                            st.session_state.use_serp_api
                            and st.session_state.serp_api_key
                            and st.session_state.serpapi_location
                        ):
                            print("Deep Search Selected")
                            (
                                BODY,
                                img_links,
                                video_links,
                                MARKDOWN_PLACEHOLDER,
                                related_questions,
                                maps_search_results,
                            ) = get_web_results(
                                api_key=st.session_state.serp_api_key,
                                groq_api_key=st.session_state.groq_api_key,
                                query=prompt,
                                location=st.session_state.serpapi_location,
                                max_results=max_results,
                            )
                        elif (
                            st.session_state.use_agentic_search
                        ):  # ? Agentic Search Integration
                            try:
                                objective_json = generate_search_strings(
                                    prompt, api_key=st.session_state.groq_api_key
                                )

                                if objective_json:
                                    search_icon = "🔍"
                                    with st.expander(
                                        "Strategy generated!", expanded=False
                                    ):
                                        for _, objective in enumerate(
                                            objective_json["objectives"]
                                        ):
                                            st.info(
                                                f"##### 🎯{objective['description']}"
                                            )

                                            for search_string in objective[
                                                "search_strings"
                                            ]:
                                                st.markdown(
                                                    f"- {search_icon} {search_string}"
                                                )

                                            st.markdown("---")

                                        # Final Objective section
                                        st.write("### 🏁 Final Objective")
                                        st.success(objective_json["final_objective"])

                                        # CSS for aesthetic appeal
                                        st.markdown(
                                            """
                                        <style>
                                        div[data-testid="stExpander"] {
                                            background-color: var(--background-color);
                                            border-radius: 10px;
                                            padding: 10px;
                                        }
                                        div[data-testid="stExpander"] h2 {
                                            color: var(--primary-color);
                                        }
                                        div[data-testid="stMarkdownContainer"] {
                                            color: var(--text-color);
                                            font-family: 'Arial', sans-serif;
                                        }
                                        </style>
                                        """,
                                            unsafe_allow_html=True,
                                        )

                                    (
                                        BODY,
                                        img_links,
                                        video_links,
                                        MARKDOWN_PLACEHOLDER,
                                    ) = agentic_search_crawler(
                                        objective_json=objective_json,
                                        api_key=st.session_state.groq_api_key,
                                    )

                                    if BODY:
                                        # Feed extracted information to the model for the model's reference
                                        st.session_state.messages.append(
                                            {
                                                "role": "assistant",
                                                "content": BODY,
                                            }
                                        )

                                else:
                                    st.error(
                                        "Something went wrong while generating the search strategy. Please try again later."
                                    )
                                    st.session_state.is_groq_api_key_valid = False
                            except Exception as e:
                                print(e)
                                st.error(
                                    "Something went wrong with the Agentic Search. Please try again later."
                                )
                                st.session_state.is_groq_api_key_valid = False

                            print("Agentic Search Selected")
                        elif (
                            st.session_state.use_plain_duckduckgo
                        ):  # ? Plain DuckDuckGo Search
                            print("Just using normal DuckDuckGo search")
                            BODY, img_links, video_links, MARKDOWN_PLACEHOLDER = (
                                search_the_web(
                                    prompt,
                                    max_results=max_results,
                                    region=region,
                                    # api_key=<some_api_key>, #! give a separate api key to use a different agent for the web search prompt
                                )
                            )

                        if BODY:
                            if st.session_state.use_agentic_search:
                                print(BODY)
                            # Feed extracted information to the model for the model's reference
                            st.session_state.messages.append(
                                {
                                    "role": "user",
                                    # "role": "assistant",  #! Just experimenting with the role
                                    "content": BODY,
                                }
                            )

                if (
                    st.session_state.use_agentic_search
                    and st.session_state.search_the_web
                ):
                    with st.spinner(
                        "Waiting for 10 seconds to reduce the rate limit error..."
                    ):
                        time.sleep(10)
                # Give some feedback to the user while the model is generating the response
                with st.spinner(spinner_message):
                    try:
                        chat_completion = client.chat.completions.create(
                            model=model,
                            messages=st.session_state.messages,
                            temperature=temperature,
                            max_tokens=max_tokens,
                            top_p=top_p,
                        )

                        model_output = chat_completion.choices[0].message.content

                        # Keep track of the model's output for the model's future reference
                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": model_output,
                            }
                        )

                        # ? If the model response is generated successfully then remove the GROQ api key input
                        st.session_state.is_groq_api_key_valid = True
                        # ? If the user has enabled audio output and the agent has generated a response
                        # ? then generate audio output
                        if model_output and st.session_state.use_audio_output:
                            try:
                                # Generate audio output
                                with st.spinner("Generating audio..."):
                                    audio_file_path = asyncio.run(
                                        generate_audio_async(
                                            model_output,
                                            voice_name=st.session_state.voice_name,
                                        )
                                    )

                                # ? If the audio output is generated successfully then remove the ELEVENLABS api key input
                                st.session_state.is_elevenlabs_api_key_valid = True
                            except elevenlabs.core.api_error.ApiError as err:
                                if err.status_code == 401:
                                    st.error(
                                        "You might have entered an invalid API or have exhausted the maximum quota."
                                    )
                                    st.session_state.is_elevenlabs_api_key_valid = False
                                else:
                                    st.error(
                                        "Something went wrong with audio generation. Please try again later."
                                    )
                                    st.session_state.is_elevenlabs_api_key_valid = False
                                print(
                                    "API error, check for the api parameters or the API key"
                                )

                        #! The user will not see unstructured extracted information dump
                        #! from the web search/YouTube video/shorts transcript.
                        #! Only the model responses and accompanying media will be shown to the user
                        #! Thus keeping the `display_message` list seperate from the `messages` list
                        st.session_state.display_message.append(
                            {
                                "role": "assistant",
                                "content": model_output,
                                "media": {
                                    "audio_file_path": audio_file_path,
                                    "img_links": img_links,
                                    "video_links": video_links,
                                    "MARKDOWN_PLACEHOLDER": MARKDOWN_PLACEHOLDER,
                                    "related_questions": related_questions,
                                    "maps_search_results": maps_search_results,
                                },
                            }
                        )

                    except groq.RateLimitError:
                        if st.session_state.use_agentic_search and BODY:
                            st.error(
                                """
                                - Rate Limit Error faced while processing the search results.\n
                                - Results might be incomplete or unreliable.\n
                                - Upgrade to a paid plan to increase the rate limit and avoid such errors.
                                """
                            )
                            model_output = BODY
                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": BODY,
                                }
                            )
                            st.session_state.display_message.append(
                                {
                                    "role": "assistant",
                                    "content": BODY,
                                    "media": {
                                        "audio_file_path": None,
                                        "img_links": img_links,
                                        "video_links": video_links,
                                        "MARKDOWN_PLACEHOLDER": MARKDOWN_PLACEHOLDER,
                                        "related_questions": related_questions,
                                        "maps_search_results": None,
                                    },
                                }
                            )
                        else:
                            st.session_state.messages = []
                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": "The user has exceeded the rate limit.",
                                }
                            )
                            st.error("You have exceeded the rate limit.")
                        st.session_state.is_groq_api_key_valid = False
                        print("Rate limit error")

            except elevenlabs.core.api_error.ApiError as err:
                if err.status_code == 401:
                    st.error("Invalid API key for Elevenlabs.")
                    st.session_state.is_elevenlabs_api_key_valid = False
                else:
                    st.error(
                        "Something went wrong with audio generation. Please try again later."
                    )
                    st.session_state.is_elevenlabs_api_key_valid = False
                print("API error, check for the api parameters or the API key")

            except groq.AuthenticationError:
                st.error("Invalid API key.")
                del st.session_state.groq_api_key
                del st.session_state.messages
                del (
                    st.session_state.page_reload_count
                )  # Display the welcome message again
                st.session_state.is_groq_api_key_valid = False
                print("Invalid API key")

            except groq.BadRequestError:
                with st.chat_message("assistant"):
                    st.write(GENERIC_RESPONSE)
                    del st.session_state.messages
                st.session_state.is_groq_api_key_valid = False
                print("Bad request error")

            except groq.InternalServerError:
                with st.chat_message("assistant"):
                    st.write(GENERIC_RESPONSE)
                    del st.session_state.messages
                st.session_state.is_groq_api_key_valid = False
                print("Internal server error")

            except Exception as err:
                with st.chat_message("assistant"):
                    st.write("Something Went Wrong")
                    del st.session_state.messages
                st.session_state.is_groq_api_key_valid = False
                st.session_state.is_elevenlabs_api_key_valid = False
                print(err)

    return (
        img_links,
        video_links,
        MARKDOWN_PLACEHOLDER,
        related_questions,
        maps_search_results,
        model_output,
        audio_file_path,
    )


if __name__ == "__main__":
    st.set_page_config(
        page_title="Fast Chat",
        page_icon="⚡",
        layout="wide",
        menu_items={
            "About": "Welcome to Fast Chat! You can ask questions, get summaries of YouTube videos, and search the web. Enjoy chatting! 😊",
        },
    )

    img_links = None
    video_links = None
    MARKDOWN_PLACEHOLDER = None
    related_questions = None
    maps_search_results = None
    current_prompt = None
    audio_data = None
    FILE_NAME = "audio.wav"
    model_output = None
    encoded_image = None
    prompt = None  # ? For img gen
    payload = None  # ? For img gen

    all_sidebar_values = sidebar_and_init()
    audio_data = all_sidebar_values[-1]

    sidebar_values = all_sidebar_values[:-1]

    # ? Audio Input check
    if st.session_state.use_audio_input and audio_data and os.path.exists(FILE_NAME):

        abs_path = os.path.join(os.path.dirname(__file__), FILE_NAME)

        whisper_client = Groq(
            api_key=st.session_state.groq_api_key,
        )

        if os.path.exists(FILE_NAME) and len(audio_data) > 0:
            with st.spinner("Transcribing the audio..."):
                try:
                    transcription = None
                    with open(abs_path, "rb") as file:
                        transcription = whisper_client.audio.transcriptions.create(
                            file=(abs_path, file.read()),
                            model="whisper-large-v3",
                        )

                    if transcription:
                        current_prompt = transcription.text

                except Exception as e:
                    st.error(
                        "An error occurred while processing the audio. \nClick on `Reset` and try again."
                    )
                    print(e)
                    current_prompt = st.chat_input("Ask me anything!")

                finally:  # Remove the audio file after processing
                    os.remove(abs_path)
                    audio_data = None

    elif st.session_state.show_file_uploader:
        try:
            with st.chat_message("assistant"):
                st.markdown(
                    "Upload an image, then ask me anything"
                )  # ? Display a message to the user to upload an image
            uploaded_file = st.file_uploader(
                "Choose an image...",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=False,
            )

            if uploaded_file is not None:
                image = safe_open_image(uploaded_file)
                if image:
                    # Compress Image
                    compressed_image = compress_image(image)

                    st.image(
                        compressed_image,
                        caption="Uploaded Image",
                        use_column_width=False,
                    )

                    # Encode image to base64
                    encoded_image = encode_image(compressed_image)
                else:
                    st.error(
                        "Failed to process the uploaded image. Please try a different image."
                    )
                current_prompt = st.chat_input("Ask me anything!")

        except Exception as e:
            st.error(
                "An error occurred while processing the uploaded image. \nClick on `Reset` and try again."
            )
            st.session_state.successfully_ran = (
                True  # ? Untoggle the file uploader by default
            )
            current_prompt = st.chat_input("Ask me anything!")

    elif st.session_state.img_gen:

        with st.form(key="user_input_form"):
            prompt = st.text_input(
                "Enter your message or image prompt:",
                value="A panda in a bamboo forest eating bamboo sticks",
            )
            negative_prompt = st.text_input(
                "Enter a negative prompt (optional):", value="ugly, dark"
            )

            model_name_sampler_style_cols = st.columns([1, 1, 1])
            with model_name_sampler_style_cols[0]:
                model_name = st.selectbox(
                    "Choose a model:",
                    [
                        "sd_xl_base_1.0.safetensors [be9edd61]",
                        "dynavisionXL_0411.safetensors [c39cc051]",
                        "dreamshaperXL10_alpha2.safetensors [c8afe2ef]",
                    ],
                    index=0,
                )
            with model_name_sampler_style_cols[1]:
                sampler = st.selectbox(
                    "Choose a sampler:",
                    [
                        "DPM++ 2M Karras",
                        "DPM++ SDE Karras",
                        "Euler",
                        "Euler a",
                        "Heun",
                    ],
                    index=1,
                )

            with model_name_sampler_style_cols[2]:
                style_preset = st.selectbox(
                    "Choose a style preset:",
                    [
                        "3d-model",
                        "analog-film",
                        "anime",
                        "cinematic",
                        "comic-book",
                        "digital-art",
                        "enhance",
                        "fantasy-art",
                        "isometric",
                        "line-art",
                        "low-poly",
                        "neon-punk",
                        "origami",
                        "photographic",
                        "pixel-art",
                        "tile-texture",
                    ],
                    index=2,
                )

            steps_cfg_scale_seed_cols = st.columns([1, 1, 1])
            with steps_cfg_scale_seed_cols[0]:
                steps = st.slider("Number of steps:", 20, 50, 20)
            with steps_cfg_scale_seed_cols[1]:
                cfg_scale = st.slider("Classifier-Free Guidance Scale", 5, 15, 7)
            with steps_cfg_scale_seed_cols[2]:
                seed = st.number_input(
                    "Seed", value=-1, step=1, min_value=-1, max_value=1000
                )

            submit_button = st.form_submit_button("Send")

        if submit_button:
            if prompt:
                current_prompt = prompt
                payload = {
                    "model": model_name,
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "style_preset": style_preset,
                    "steps": steps,
                    "cfg_scale": cfg_scale,
                    "seed": seed,
                    "sampler": sampler,
                    "width": 1024,
                    "height": 1024,
                }
            else:
                st.warning("Please enter a prompt to generate the image.")

    else:  # Old good text input when audio input is failing
        current_prompt = st.chat_input("Ask me anything!")

    if current_prompt:
        (
            img_links,
            video_links,
            MARKDOWN_PLACEHOLDER,
            related_questions,
            maps_search_results,
            model_output,
            audio_file_path,
        ) = body(
            current_prompt,
            encoded_image,
            payload,
            *sidebar_values,
        )

        show_media(
            "assistant",
            model_output,
            img_links,
            video_links,
            MARKDOWN_PLACEHOLDER,
            audio_file_path,
            related_questions,
            maps_search_results,
        )

        st.info(
            "**Fast Chat ocassionally gives misleading responses. Kindly verify the information from reliable sources.**",
            icon="ℹ️",
        )
