<div style="display: flex; justify-content: space-between; align-items: center;">

  <h1 style="margin: 0;">⚡ Fast-Chat</h1>
  
  <img src="utils/static/Fast-Chat_avatar.gif" alt="Fast-Chat" width="250" style="margin-left: 5px;" />

</div>

### An AI chat assistant for Lightning-Fast Conversations

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fast-chat.streamlit.app/)

Engage in a lightning-fast chat conversation with **Fast-Chat**, leveraging the capabilities of **GROQ**'s cutting-edge **Language Processing Unit** (**[GROQ LPU<sup>TM</sup>](https://wow.groq.com/why-groq/)**). Interact with Fast-Chat and receive immediate responses to your inquiries.

#### Powered by

[![Gemma Model](https://img.shields.io/badge/Gemma_Model-Open_Models-blue)](https://ai.google.dev/gemma) [![Llama Model](https://img.shields.io/badge/Llama_Model-Open_Models-violet)](https://llama.meta.com/) [![Mistral AI](https://img.shields.io/badge/Mistral_AI-Open_Models-orange)](https://mistral.ai/news/mixtral-of-experts/) [![Groq AI](https://img.shields.io/badge/Groq_AI-Fast_Inference_Engine-black)](https://wow.groq.com/why-groq/) [![Eleven Labs](https://img.shields.io/badge/ElevenLabs-Voice_Synthesis-green)](https://elevenlabs.io/)

<div style="display: flex; justify-content: space-around;">
  <img src="utils/static/groq.jpg" width="200">
</div>

<div style="display: flex; justify-content: space-around;">
  <img src="utils/static/gemma.webp" width="200" height="100">
  <img src="utils/static/llama.webp" width="200" height="100">
  <img src="utils/static/mistral_ai_image.jpg" width="200" height="100">
  <img src="utils/static/elevenlabs.jpg" width=200 height="100">
</div>

## Key Functionalities

- [x] ⚡**Real-Time Responses**: Experience near-instantaneous responses to your queries, facilitating a seamless conversation flow.
- [x] 🔍 **Web Search Integration**: Fast-Chat can search the web for information and provide you with relevant results.
- [x] 📺 **YouTube Comprehension**: Fast-Chat possesses the ability to understand and potentially respond to content from YouTube videos and shorts.
- [x] 🎙️ **Voice Recognition**: Fast-Chat can listen to you and comprehend your queries
- [x] 🗣️ **Audio Output**: Fast-Chat can talk back to you.
- [x] ✨ **Interactive Interface**: Enjoy a user-friendly and intuitive chat interface for a smooth interaction.
- [x] 📝 **Contextual Awareness**: Fast-Chat maintains conversational context, enabling it to provide more relevant and engaging responses.
- [x] 🤖 **Model Selection**: Choose from a variety of models to tailor the chat experience to your specific needs.
- [x] 🪛 **Tune Parameters**: Adjust parameters to refine the response generation process and personalize your interaction.

## Getting Started

### Prerequisites

- **`Python 3.8`** or higher
- **`git`**
- **`pipenv`** (recommended)
- [🔗GROQ API key](https://console.groq.com/keys)
- [🔗SerpAPI key](https://serpapi.com/dashboard) (optional)
- [🔗ElevenLabs API key](https://elevenlabs.io/app/speech-synthesis/text-to-speech) (optional)

### Installation

1. Clone the repository

```sh
git clone https://github.com/sayan10rakshit/Fast-Chat.git
cd Fast-Chat
```

2. Install the required dependencies using `pipenv`/`venv`:

![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)![macOS](<https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0>)![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

```sh
# Using pipenv
pipenv install
```

**OR**
  
![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)![macOS](<https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0>)

```sh
# Using venv
python3 -m venv .env_for_fast_chat
source .env_for_fast_chat/bin/activate
pip install -r requirements.txt
```

🚨 **NOTE**: If you are facing any error/s try using `python` instead of `python3` in the above commands  

<details>
<summary><img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows" /></summary>

```powershell
# Using venv
python3 -m venv .env_for_fast_chat
.env_for_fast_chat\Scripts\Activate.ps1
pip install -r requirements.txt
```

  🚨 **NOTE**: If you are facing any error/s try using `python` instead of `python3` in the above commands  
</details>

## Usage

- Launch with Streamlit:
  - With `pipenv`

    ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)![macOS](<https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0>)![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)

    ```sh
    # You can run without activating the virtual environment
    pipenv run streamlit run app.py
    ```

    **OR**

    ```sh
    # Activate the virtual environment
    pipenv shell
    streamlit run app.py
    ```

    ```sh
    # Deactivate the virtual environment after using Fast-Chat
    deactivate
    ```

  - With `venv`
  
      ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)![macOS](<https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0>)

      ```sh
      # Activate the virtual environment
      source .env_for_fast_chat/bin/activate
      streamlit run app.py
      ```

      ```sh
      # Deactivate the virtual environment after using Fast-Chat
      deactivate
      ```

      <details>
      <summary><img src="https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white" alt="Windows" /></summary>

      ```powershell
      # Activate the virtual environment
      .env_for_fast_chat\Scripts\Activate.ps1
      streamlit run app.py
      ```

      ```powershell
      # Deactivate the virtual environment after using Fast-Chat
      deactivate
      ```

      </details>

- When the app is running, use Fast-Chat in your browser at `http://localhost:8501`

## Coming Soon

- [ ] **Image Generation**: Implement image generation capabilities to Fast-Chat.
- [ ] **Multi-Modal Support**: Incorporate support for multi-modal interactions, including text, images, and videos.
- [ ] **Multi-Language Support**: Extend support for multiple languages to cater to a diverse user base.
- [ ] **User Profiling**: Implement user profiling to personalize the chat experience and responses.
