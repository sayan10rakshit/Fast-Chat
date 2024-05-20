import random

import groq
from groq import Groq
import streamlit as st
from extract_subs import prepare_prompt, filter_links
from get_web_results import search_the_web, REGIONS


# Define a function to handle the toggling logic
def handle_toggle(toggle_name):
    if toggle_name == "use_you_tube":
        st.session_state.search_the_web = False
    elif toggle_name == "search_the_web":
        st.session_state.use_you_tube = False


def main():
    st.set_page_config(
        page_title="Fast Chat",
        page_icon="⚡",
        layout="wide",
    )

    # rest of your code
    GENERIC_RESPONSE = "Sorry, that's on me.\nDue to limited hardware resources in \
                                the free tier, I can't respond to this query.\nPlease try again later or \
                                    upgrade to a paid plan to get more hard.\n\
                                        Let's start afresh shall we? 😁"

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

    if "use_you_tube" not in st.session_state:
        st.session_state.use_you_tube = False

    if "search_the_web" not in st.session_state:
        st.session_state.search_the_web = False

    st.session_state.page_reload_count += (
        1  # will be incremented each time streamlit reruns the script
    )

    if "special_message" not in st.session_state:
        st.session_state.special_message = None
    if "special_message_shown" not in st.session_state:
        st.session_state.special_message_shown = False

    st.markdown("# Fast Chat ⚡")

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
            ["mixtral-8x7b-32768", "gemma-7b-it", "llama3-70b-8192", "llama3-8b-8192"],
            index=2,
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
            help="A stochastic decoding method where the model considers the cumulative probability of the most likely tokens.",
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

            if max_results >= 20 and model == "llama3-70b-8192":
                st.session_state.special_message = """
                Although llama3-70b-8192 is the most powerful model, you might get slow responses.\n
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

    if st.session_state.special_message and not st.session_state.special_message_shown:
        st.warning(st.session_state.special_message)
        st.session_state.special_message = None
        st.session_state.special_message_shown = True

    if prompt := st.chat_input("Ask me anything!"):
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
                            st.session_state.remove_unnecessary_messages = True
                            for prompt_modified in prompt_modified_list:
                                st.session_state.messages.append(
                                    {"role": "user", "content": prompt_modified}
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
                        BODY, img_links, video_links, MARKDOWN_PLACEHOLDER = (
                            search_the_web(
                                prompt,
                                max_results=max_results,
                                region=region,
                                # api_key=<some_api_key>, #! give a separate api key to use a different agent for the web search prompt
                            )
                        )

                        if BODY:
                            st.session_state.remove_unnecessary_messages = True
                            st.session_state.messages.append(
                                {"role": "user", "content": BODY}
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
                                and st.session_state.remove_unnecessary_messages
                            ):
                                # If subtitles were extracted, then remove the modified prompt from the chat history
                                for _ in range(len(prompt_modified_list)):
                                    st.session_state.messages.pop()
                                st.session_state.remove_unnecessary_messages = False
                            elif (
                                st.session_state.search_the_web
                                and st.session_state.remove_unnecessary_messages
                            ):
                                # If search results were displayed, then remove the search results from the chat history
                                st.session_state.messages.pop()
                                st.session_state.remove_unnecessary_messages = False

                            # Add assistant response to chat history
                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "content": model_output,
                                }
                            )

                            st.write(model_output)

                            # ? YOUTUBE VIDEO/SHORTS RESULTS after model response
                            # Display the YouTube video/shorts after the response
                            col1, _ = st.columns([0.5, 0.5])
                            if (
                                all_yt_links
                                and st.session_state.use_you_tube
                                and all_yt_links[0][
                                    1
                                ]  # stored as (link, type) in the list, type is either "video" or "shorts"
                                == "video"  # if the YT content is a shorts, don't display it
                            ):
                                with col1:
                                    for video_link, _ in all_yt_links:
                                        st.video(video_link, start_time=0)

                            # ? WEB SEARCH RESULTS after model response
                            # Display the web search references after the response
                            elif st.session_state.search_the_web:
                                # ? Display the images

                                if img_links:
                                    st.caption("**Images from the web**")
                                    cols = st.columns(3)
                                    pics_to_show = (
                                        3 if len(img_links) > 3 else len(img_links)
                                    )

                                    # Show the initial set of images
                                    for idx, img_link in enumerate(
                                        img_links[:pics_to_show]
                                    ):
                                        with cols[idx % 3]:
                                            st.image(img_link, use_column_width="auto")

                                    # Show additional images under the expander if there are any
                                    if len(img_links) > pics_to_show:
                                        with st.expander("View more images"):
                                            more_cols = st.columns(3)
                                            for idx, img_link in enumerate(
                                                img_links[pics_to_show:]
                                            ):
                                                with more_cols[idx % 3]:
                                                    st.image(
                                                        img_link,
                                                        use_column_width="auto",
                                                    )

                                # ? Display the videos
                                if video_links:
                                    st.caption("**Videos from the web**")
                                    cols = st.columns(2)
                                    # if video_links:
                                    videos_to_show = (
                                        2 if len(video_links) > 2 else len(video_links)
                                    )
                                    for idx, (video_link, _) in enumerate(
                                        video_links[:videos_to_show]
                                    ):
                                        with cols[idx % 2]:
                                            st.video(video_link, start_time=0)
                                    # Show additional videos under the expander if there are any
                                    if len(video_links) > videos_to_show:
                                        with st.expander("View more videos"):
                                            more_cols = st.columns(2)
                                            for idx, (video_link, _) in enumerate(
                                                video_links[videos_to_show:]
                                            ):
                                                with more_cols[idx % 2]:
                                                    st.video(video_link, start_time=0)

                                with st.expander("Sources from the web"):
                                    st.markdown(MARKDOWN_PLACEHOLDER)
                                st.info(
                                    "**Fast Chat ocassionally gives misleading results. Kindly verify the information from reliable sources.**",
                                    icon="ℹ️",
                                )

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


if __name__ == "__main__":
    main()
