import groq
from groq import Groq
import streamlit as st
import time


if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "page_reload_count" not in st.session_state:
    st.session_state.page_reload_count = 0
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": "Hello! Want some fast responses? Ask me anything!",
        }
    )

st.session_state.page_reload_count += (
    1  # will be incremented each time streamlit reruns the script
)

st.markdown("# Fast Chat ⚡")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def response_generator(response_object: dict):
    final_response = response_object.choices[0].message.content
    for word in final_response.split():
        yield word + " "
        time.sleep(0.005)


with st.sidebar:
    groq_api_key = st.text_input("GROQ API Key", type="password")
    if groq_api_key != "":
        st.session_state.api_key = groq_api_key
    st.markdown("[Get your API key](https://console.groq.com/keys).")

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

if prompt := st.chat_input("What is up?"):
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

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                chat_completion = client.chat.completions.create(
                    model=model,
                    messages=st.session_state.messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    top_p=top_p,
                )
                if "script" in prompt or "code" in prompt:
                    response = st.write(chat_completion.choices[0].message.content)
                else:
                    response = st.write_stream(response_generator(chat_completion))

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        except groq.AuthenticationError:
            st.error("Invalid API key.")
            del st.session_state.api_key
            del st.session_state.messages
            del st.session_state.page_reload_count  # Display the welcome message again
