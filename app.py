import os
import random

import groq
from groq import Groq
from audiorecorder import audiorecorder
import streamlit as st
from utils.extract_subs import prepare_prompt, filter_links
from utils.get_web_results import search_the_web, REGIONS
from utils.get_web_results_serp import get_web_results
from utils.get_location import find_closest_match


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
    elif toggle_name == "search_the_web":
        st.session_state.use_you_tube = False


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

    """
    model = None
    temperature = None
    max_tokens = None
    top_p = None
    region = None
    max_results = None
    audio = None

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    if "remove_unnecessary_messages" not in st.session_state:
        st.session_state.remove_unnecessary_messages = False

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
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": placeholder_messages,
            }
        )

    if "use_audio_input" not in st.session_state:
        st.session_state.use_audio_input = False

    if "use_you_tube" not in st.session_state:
        st.session_state.use_you_tube = False

    if "search_the_web" not in st.session_state:
        st.session_state.search_the_web = False

    if "use_serp_api" not in st.session_state:
        st.session_state.use_serp_api = False

    if "serp_api_key" not in st.session_state:
        st.session_state.serp_api_key = ""

    if "serpapi_location" not in st.session_state:
        st.session_state.serpapi_location = ""

    if "old_user_serpapi_location" not in st.session_state:
        st.session_state.old_user_serpapi_location = ""

    st.session_state.page_reload_count += (
        1  # will be incremented each time streamlit reruns the script
    )

    if "all_yt_links" not in st.session_state:
        st.session_state.all_yt_links = []
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

    st.markdown(
        "# Fast Chat ⚡"
    )
    st.markdown("by **[Sayan Rakshit](https://github.com/sayan10rakshit/Fast-Chat)**")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    with st.sidebar:
        groq_api_key = st.text_input("GROQ API Key", type="password")
        if groq_api_key != "":
            st.session_state.api_key = groq_api_key
        st.markdown(
            "[Get your FREE API key!](https://console.groq.com/keys)",
            help="""Since running an LLM is computationally expensive,
            this app uses an API to run the model on the cloud.
            See more details [here](https://wow.groq.com/)""",
        )

        model = st.selectbox(
            "Select Model",
            [
                "gemma2-9b-it",
                "gemma-7b-it",
                "mixtral-8x7b-32768",
                "llama-3.1-8b-instant",
                "llama3-8b-8192",
                "llama-3.1-70b-versatile",
                "llama3-70b-8192",
            ],
            index=5,
        )

        if "gemma" in model:
            st.markdown("[**Model by**](https://ai.google.dev/gemma)")
            st.image(
                "https://www.gstatic.com/images/branding/googlelogo/svg/googlelogo_clr_74x24px.svg",
                width=125,
            )

        elif "llama" in model:
            st.markdown("[**Model by**](https://llama.meta.com/)")
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

        temperature = st.slider(
            "Temperature",
            0.0,
            2.0,
            1.0,
            0.01,
            help="0.0 is deterministic, 1.0 is default, 2.0 is very creative",
        )

        if model == "mixtral-8x7b-32768":
            max_tokens = st.slider(
                "Max Tokens", 0, 32768, 1024, help="Max tokens in the response"
            )
        elif model in ("llama3-70b-8192", "llama-3.1-70b-versatile"):
            max_tokens = st.slider(
                "Max Tokens", 0, 8000, 1024, help="Max tokens in the response"
            )
        else:
            max_tokens = st.slider(
                "Max Tokens", 0, 8192, 1024, help="Max tokens in the response"
            )

        top_p = st.slider(
            "Top P",
            0.0,
            1.0,
            0.9,
            0.01,
            help="""A stochastic decoding method where the top p cumulative probability tokens (sorted w.r.t. probability)
            are considered in each time step. The top p tokens are sampled randomly.""",
        )

        st.toggle(
            "Audio Input",
            st.session_state.use_audio_input,
            key="use_audio_input",
        )

        if st.session_state.use_audio_input:
            audio = audiorecorder(
                start_prompt="",
                stop_prompt="",
                pause_prompt="",
                show_visualizer=True,
                key=None,
            )

        st.toggle(
            "Use YouTube",
            st.session_state.use_you_tube,
            key="use_you_tube",
            on_change=handle_toggle,
            args=("use_you_tube",),
        )

        st.toggle(
            "Search the Web",
            st.session_state.search_the_web,
            key="search_the_web",
            on_change=handle_toggle,
            args=("search_the_web",),
        )

        if st.session_state.search_the_web:
            region = st.selectbox(
                "Select Region",
                REGIONS,
                index=25,
                help="Select the region to get the search results from.",
            )

            max_results = st.slider(
                "Max search results to refer",
                10,
                30,
                12,
                help="More results might take longer to process but will provide more context.",
            )

            st.session_state.use_serp_api = st.toggle(
                "Perform DeepSearch",
                False,
            )

            # ? SerpApi Integration
            if st.session_state.use_serp_api:
                st.session_state.special_message2 = """
                Although DeepSearch gives more comprehensive search results, it might be pretty slow.\n
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
                    authentic_serpapi_location = find_closest_match(serpapi_location)
                    st.success(f"Using location: {authentic_serpapi_location}")
                    st.session_state.serpapi_location = authentic_serpapi_location
                    st.session_state.old_user_serpapi_location = serpapi_location

            if max_results >= 20 and model in (
                "llama3-70b-8192",
                "llama-3.1-70b-versatile",
            ):
                st.session_state.special_message = f"""
                Although {model} is a more powerful model, you might get slow responses.\n
                It is recommended to use other models or to reduce the max search results.\n
                mixtral-8x7b-32768 is faster and can handle more tokens.
                """

        if st.button("Clear Chat"):
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "Let's start afresh shall we? 😁",
                }
            ]
            st.session_state.remove_unnecessary_messages = False
            # reload the page to display the welcome message
            st.rerun()

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

    return (model, temperature, max_tokens, top_p, region, max_results, audio)


def body(
    prompt=None,
    model=None,
    temperature=None,
    max_tokens=None,
    top_p=None,
    region=None,
    max_results=None,
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

    Returns:
        all_yt_links (list): The list of YouTube links extracted from the prompt.
        img_links (list): The list of image links extracted from the search results.
        video_links (list): The list of video links extracted from the search results.
        MARKDOWN_PLACEHOLDER (str): The markdown placeholder for the search results.
        related_questions (list): The list of related questions extracted from the search results.
    """

    GENERIC_RESPONSE = "Sorry, that's on me.\nDue to limited hardware resources in \
                                the free tier, I can't respond to this query.\nPlease try again later or \
                                    upgrade to a paid plan to get more hard.\n\
                                        Let's start afresh shall we? 😁"

    all_yt_links = None
    img_links = None
    video_links = None
    MARKDOWN_PLACEHOLDER = None
    related_questions = None

    if prompt:
        # Add user message to chat history
        if st.session_state.api_key == "":

            st.warning("Please enter your GROQ API key.")
        else:
            try:
                client = Groq(
                    api_key=st.session_state.api_key,
                )
                st.session_state.messages.append({"role": "user", "content": prompt})
                # Display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(prompt)

                # check if the prompt contains a youtube link and user asked something related to the video
                prompt_modified_list = None
                all_yt_links = filter_links(prompt)
                if all_yt_links and st.session_state.use_you_tube:
                    with st.spinner("Seeing the YouTube video/shorts..."):
                        prompt_modified_list = prepare_prompt(prompt)
                        if (
                            prompt_modified_list
                        ):  # only add the modified prompt if subtitles were extracted
                            st.session_state.remove_unnecessary_messages = True  # a flag to remove the modified prompt from the chat history
                            for prompt_modified in prompt_modified_list:
                                st.session_state.messages.append(
                                    {
                                        "role": "user",
                                        "content": prompt_modified,
                                    }  # temporarily add the modified prompt to the chat history
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
                            (
                                BODY,
                                img_links,
                                video_links,
                                MARKDOWN_PLACEHOLDER,
                                related_questions,
                            ) = get_web_results(
                                api_key=st.session_state.serp_api_key,
                                query=prompt,
                                location=st.session_state.serpapi_location,
                                max_results=max_results,
                            )
                        else:  # ? DuckDuckGo Integration
                            BODY, img_links, video_links, MARKDOWN_PLACEHOLDER = (
                                search_the_web(
                                    prompt,
                                    max_results=max_results,
                                    region=region,
                                    # api_key=<some_api_key>, #! give a separate api key to use a different agent for the web search prompt
                                )
                            )

                        if BODY:
                            st.session_state.remove_unnecessary_messages = True  # a flag to remove the search results from the chat history
                            st.session_state.messages.append(
                                {
                                    "role": "user",
                                    "content": BODY,
                                }  # temporarily add the search results to the chat history
                            )

                # Display assistant response in chat message container
                with st.spinner(spinner_message):
                    with st.chat_message("assistant"):
                        try:
                            chat_completion = client.chat.completions.create(
                                model=model,
                                messages=st.session_state.messages,
                                temperature=temperature,
                                max_tokens=max_tokens,
                                top_p=top_p,
                            )

                            model_output = chat_completion.choices[0].message.content

                            if (
                                prompt_modified_list
                                and st.session_state.remove_unnecessary_messages  # if YouTube subtitles were extracted and the flag is set
                            ):
                                # If subtitles were extracted, then remove the modified prompt from the chat history
                                for _ in range(
                                    len(prompt_modified_list)
                                ):  # remove all the modified prompts
                                    st.session_state.messages.pop()  # last n = len(prompt_modified_list) messages contain the modified prompts
                                st.session_state.remove_unnecessary_messages = False
                            elif (
                                st.session_state.search_the_web
                                and st.session_state.remove_unnecessary_messages  # if search results were displayed and the flag is set
                            ):
                                # If search results were displayed, then remove the search results from the chat history
                                st.session_state.messages.pop()
                                st.session_state.remove_unnecessary_messages = False

                            # Add assistant response to chat history
                            #! Previous clean-ups was/were necessary to remove the modified prompt or search results from the chat history
                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": model_output,
                                }
                            )

                            st.write(model_output)

                        except groq.RateLimitError:
                            if (
                                prompt_modified_list
                                and st.session_state.remove_unnecessary_messages
                            ):
                                for _ in range(len(prompt_modified_list)):
                                    st.session_state.messages.pop()
                                st.session_state.remove_unnecessary_messages = False
                            st.session_state.messages = []
                            st.session_state.messages.append(
                                {"role": "assistant", "content": GENERIC_RESPONSE}
                            )
                            st.write(GENERIC_RESPONSE)
                            print("Rate limit error")

            except groq.AuthenticationError:
                st.error("Invalid API key.")
                del st.session_state.api_key
                del st.session_state.messages
                del (
                    st.session_state.page_reload_count
                )  # Display the welcome message again
                print("Invalid API key")

            except groq.BadRequestError:
                with st.chat_message("assistant"):
                    st.write(GENERIC_RESPONSE)
                    del st.session_state.messages
                print("Bad request error")

            except groq.InternalServerError:
                with st.chat_message("assistant"):
                    st.write(GENERIC_RESPONSE)
                    del st.session_state.messages
                print("Internal server error")

            except Exception as e:
                with st.chat_message("assistant"):
                    st.write(GENERIC_RESPONSE)
                    del st.session_state.messages
                print(e)

    return all_yt_links, img_links, video_links, MARKDOWN_PLACEHOLDER, related_questions


def show_media(
    all_yt_links=None,
    img_links=None,
    video_links=None,
    MARKDOWN_PLACEHOLDER=None,
) -> (
    None
):  #! This will only be executed (display the media content/s) if either YouTube or Web search is enabled
    """
    Display the YouTube video/shorts and web search results after the model response.

    This function is responsible for displaying the images, videos, and web search references after the model response on the right side of the app.
    The media content is only displayed for the current prompt and not for the previous prompts.

    Args:
        all_yt_links (list, optional): All the YouTube links extracted from the prompt. Defaults to None.
        img_links (list, optional): All the image links extracted from the search results. Defaults to None.
        video_links (list, optional): All the video links extracted from the search results. Defaults to None.
        MARKDOWN_PLACEHOLDER (str, optional): The list of web search references. Defaults to None.
        related_questions (list, optional): The list of related questions extracted from the search results. Defaults to None.
    """
    # ? YOUTUBE VIDEO/SHORTS RESULTS after model response
    # Display the YouTube video/shorts after the response
    if (
        all_yt_links
        and st.session_state.use_you_tube
        and all_yt_links[0][
            1
        ]  # stored as (link, type) in the list, type is either "video" or "shorts"
        == "video"  # if the YT content is a shorts, don't display it
    ):
        for video_link, _ in all_yt_links:
            try:
                st.video(video_link, start_time=0)
            except Exception as e:
                print(e)

    # ? WEB SEARCH RESULTS after model response
    # Display the web search references after the response
    elif st.session_state.search_the_web:
        # ? Display the images

        if img_links:
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
        if video_links:
            st.caption("**Videos from the web**")
            cols_vids = st.columns(2)
            # if video_links:
            videos_to_show = 2 if len(video_links) > 2 else len(video_links)
            # ? SerpApi Integration
            if (
                st.session_state.use_serp_api
                and st.session_state.serp_api_key
                and st.session_state.serpapi_location
            ):
                for idx, video_link in enumerate(video_links[:videos_to_show]):
                    with cols_vids[idx % 2]:
                        try:
                            st.video(video_link, start_time=0)
                        except Exception as e:
                            print(e)
                if len(video_links) > videos_to_show:
                    with st.expander("View more videos"):
                        more_cols = st.columns(2)
                        for idx, video_link in enumerate(video_links[videos_to_show:]):
                            with more_cols[idx % 2]:
                                try:
                                    st.video(video_link, start_time=0)
                                except Exception as e:
                                    print(e)
            # ? DDG Integration
            else:
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

        with st.expander("Sources from the web"):
            st.markdown(MARKDOWN_PLACEHOLDER)


if __name__ == "__main__":
    st.set_page_config(
        page_title="Fast Chat",
        page_icon="⚡",
        layout="wide",
        menu_items={
            "About": "Welcome to Fast Chat! You can ask questions, get summaries of YouTube videos, and search the web. Enjoy chatting! 😊",
        },
    )

    all_yt_links = None
    img_links = None
    video_links = None
    MARKDOWN_PLACEHOLDER = None
    related_questions = None
    current_prompt = None

    all_sidebar_values = sidebar_and_init()
    audio = all_sidebar_values[-1]
    sidebar_values = all_sidebar_values[:-1]

    # ? Audio Input check
    if st.session_state.use_audio_input and audio:

        if audio is not None and len(audio) > 0:
            FILE_NAME = "audio.wav"
            audio.export(FILE_NAME, format="wav")
            abs_path = os.path.dirname(__file__) + "/" + FILE_NAME

            whisper_client = Groq(
                api_key=st.session_state.api_key,
            )

            try:
                transcription = None
                with open(abs_path, "rb") as file:
                    transcription = whisper_client.audio.transcriptions.create(
                        file=(abs_path, file.read()),
                        model="whisper-large-v3",
                    )

                if transcription:
                    current_prompt = transcription.text

            # ? If some error occurs while processing the audio, then revert back to text input
            except Exception as e:
                st.error("An error occurred while processing the audio.")
                print(e)
                current_prompt = st.chat_input("Ask me anything!")

    else:
        current_prompt = st.chat_input("Ask me anything!")

    if current_prompt:
        main_cols = st.columns([0.6, 0.4])
        with main_cols[0]:
            (
                st.session_state.all_yt_links,
                st.session_state.img_links,
                st.session_state.video_links,
                st.session_state.MARKDOWN_PLACEHOLDER,
                st.session_state.related_questions,
            ) = body(
                current_prompt,
                *sidebar_values,
            )

        with main_cols[1]:
            show_media(
                st.session_state.all_yt_links,
                st.session_state.img_links,
                st.session_state.video_links,
                st.session_state.MARKDOWN_PLACEHOLDER,
            )

        if st.session_state.related_questions:
            st.markdown("### Related Questions")
            for question in st.session_state.related_questions:
                with st.expander(question["question"]):
                    if "thumbnail" in question:
                        if "title" in question:
                            st.markdown(f"**{question['title']}**")
                        col1, col2 = st.columns([1, 5])
                        if "thumbnail" in question:
                            col1.image(question["thumbnail"])
                        if "snippet" in question:
                            col2.write(question["snippet"])
                        if "link" in question:
                            if "source_logo" in question:
                                # Show the source logo inside markdown just before the link
                                col2.markdown(
                                    f"![source]({question['source_logo']})  [{question['displayed_link']}]({question['link']})"
                                )
                            else:
                                col2.markdown(
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

    if current_prompt:
        st.info(
            "**Fast Chat ocassionally gives misleading results. Kindly verify the information from reliable sources.**",
            icon="ℹ️",
        )
