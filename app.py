import random

import groq
from groq import Groq
import streamlit as st
from extract_subs import prepare_prompt, filter_links


def main():
    st.set_page_config(
        page_title="Fast Chat",
        page_icon="⚡",
        layout="wide",
    )

    # rest of your code
    RESPONSE = "Sorry, that's on me.\nDue to limited hardware resources in \
                                the free tier, I can't respond to this query.\nPlease try again later or \
                                    upgrade to a paid plan to get more hard"

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

    st.session_state.page_reload_count += (
        1  # will be incremented each time streamlit reruns the script
    )

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

        use_you_tube = st.toggle("Use YouTube", False)
        if use_you_tube:
            st.session_state.use_you_tube = True
        else:
            st.session_state.use_you_tube = False

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
                if filter_links(prompt) and st.session_state.use_you_tube:
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

                            # Add assistant response to chat history
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
                            st.session_state.messages.append(
                                {"role": "assistant", "content": RESPONSE}
                            )
                            st.write(RESPONSE)

            except groq.AuthenticationError:
                st.error("Invalid API key.")
                del st.session_state.api_key
                del st.session_state.messages
                del (
                    st.session_state.page_reload_count
                )  # Display the welcome message again

            except groq.BadRequestError:
                with st.chat_message("assistant"):
                    st.write(RESPONSE + "\nLet's start afresh shall we? 😁")
                    del st.session_state.messages

            except groq.InternalServerError:
                with st.chat_message("assistant"):
                    st.write(RESPONSE + "\nLet's start afresh shall we? 😁")
                    del st.session_state.messages

            except Exception:
                with st.chat_message("assistant"):
                    st.write(RESPONSE + "\nLet's start afresh shall we? 😁")
                    del st.session_state.messages


if __name__ == "__main__":
    main()
