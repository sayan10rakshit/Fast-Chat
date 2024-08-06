# Fast-Chat⚡

### Powered by GROQ's Language Processing Unit

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fast-chat.streamlit.app/)

Engage in a lightning-fast chat experience with Fast-Chat, leveraging the capabilities of GROQ's cutting-edge Language Processing Unit ([GROQ LPU<sup>TM</sup>](https://wow.groq.com/why-groq/)). Interact with Fast-Chat and receive immediate responses to your inquiries.

##### Powered by

[![Gemma Model](https://img.shields.io/badge/Gemma_Model-Open_Models-blue)](https://ai.google.dev/gemma) [![Llama Model](https://img.shields.io/badge/Llama_Model-Open_Models-violet)](https://llama.meta.com/) [![Mistral AI](https://img.shields.io/badge/Mistral_AI-Open_Models-orange)](https://mistral.ai/news/mixtral-of-experts/) [![Groq AI](https://img.shields.io/badge/Groq_AI-Fast_Inference_Engine-black)](https://wow.groq.com/why-groq/)

<div style="display: flex; justify-content: space-around;">
  <img src="utils/images/gemma.webp" width="200">
  <img src="utils/images/llama.webp" width="200">
  <img src="utils/images/mistral_ai_image.jpg" width="200">
  <img src="utils/images/groq.jpg" width="200">
</div>

## Key Functionalities

- [x] ⚡**Real-Time Responses**: Experience near-instantaneous responses to your queries, facilitating a seamless conversation flow.
- [x] 🔍 **Web Search Integration**: Fast-Chat can search the web for information and provide you with relevant results.
- [x] 📺 **YouTube Comprehension**: Fast-Chat possesses the ability to understand and potentially respond to content from YouTube videos and shorts.
- [x] ✨ **Interactive Interface**: Enjoy a user-friendly and intuitive chat interface for a smooth interaction.
- [x] 📝 **Contextual Awareness**: Fast-Chat maintains conversational context, enabling it to provide more relevant and engaging responses.
- [x] 🤖 **Model Selection**: Choose from a variety of models to tailor the chat experience to your specific needs.
- [x] 🪛 **Tune Parameters**: Adjust parameters to refine the response generation process and personalize your interaction.

## Getting Started

### Prerequisites

- **`Python 3.8`** or higher
- **`pipenv`** (recommended)
- [🔗GROQ API key](https://console.groq.com/keys)
- [🔗SerpAPI key](https://serpapi.com/dashboard) (optional)

### Installation

1. Clone the repository

```sh
git clone https://github.com/sayan10rakshit/Fast-Chat.git
cd Fast-Chat
```

2. Install the required dependencies using `pipenv`/`venv`:

```sh
# Using pipenv
pipenv install
```

OR

```sh
# Using venv
python -m venv .env_for_fast_chat
source .env_for_fast_chat/bin/activate
pip install -r requirements.txt
```

## Usage

- Launch with Streamlit:
  - With `pipenv`

    ```sh
    # You can run without activating the virtual environment
    pipenv run streamlit run app.py
    ```

    OR

    ```sh
    # Activate the virtual environment
    pipenv shell
    streamlit run app.py
    # Deactivate the virtual environment after using Fast-Chat
    deactivate
    ```

  - With `venv`

    ```sh
    # Activate the virtual environment
    source .env_for_fast_chat/bin/activate
    streamlit run app.py
    # Deactivate the virtual environment after using Fast-Chat
    deactivate
    ```

## Coming Soon

- [ ] **Voice Recognition**: Implement voice recognition functionality to enable voice-based interactions.
- [ ] **Multi-Modal Support**: Incorporate support for multi-modal interactions, including text, images, and videos.
- [ ] **Multi-Language Support**: Extend support for multiple languages to cater to a diverse user base.
- [ ] **User Profiling**: Implement user profiling to personalize the chat experience and responses.
