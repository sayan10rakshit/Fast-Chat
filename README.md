# ⚡Fast-Chat
  
<img src="utils/static/Fast-Chat_avatar.gif" alt="Fast-Chat" width="400">

### An AI chat assistant for Lightning-Fast Conversations

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fast-chat.streamlit.app/)

Engage in a lightning-fast chat conversation with **Fast-Chat**, leveraging the capabilities of **GROQ**'s cutting-edge **Language Processing Unit** (**[GROQ LPU<sup>TM</sup>](https://wow.groq.com/why-groq/)**). Interact with Fast-Chat and receive immediate responses to your inquiries.

#### Powered by

[![Gemma Model](https://img.shields.io/badge/Gemma-Google_AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/gemma) [![Llama Model](https://img.shields.io/badge/Llama-Meta_AI-0668E1?style=for-the-badge&logo=meta&logoColor=white)](https://llama.meta.com/) [![Mistral AI](https://img.shields.io/badge/Mistral-Mistral_AI-FF6B6B?style=for-the-badge&logo=mistralai&logoColor=white)](https://mistral.ai/news/mixtral-of-experts/) [![Microsoft](https://img.shields.io/badge/Microsoft-Microsoft_Research-00A4EF?style=for-the-badge&logo=microsoft&logoColor=white)](https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/) [![Groq AI](https://img.shields.io/badge/Groq-Inference_Platform-000000?style=for-the-badge&logo=groq&logoColor=white)](https://wow.groq.com/why-groq/) [![Eleven Labs](https://img.shields.io/badge/ElevenLabs-Voice_Synthesis-3D3D3D?style=for-the-badge&logo=elevenlabsColor=white)](https://elevenlabs.io/) [![Prodia](https://img.shields.io/badge/Prodia-Image_Generation-7B68EE?style=for-the-badge&logo=prodia&logoColor=white)](https://prodia.com/)


<div style="text-align: center;">
  <img src="utils/static/groq.jpg" alt="Groq Image" width="500" height="300" style="margin-bottom: 20px;">
</div>

<div style="display: flex; justify-content: space-around; margin-bottom: 20px;">
  <img src="utils/static/gemma.webp" alt="Gemma Image" width="166" height="100">
  <img src="utils/static/llama.webp" alt="Llama Image" width="166" height="100">
  <img src="utils/static/mistral_ai_image.jpg" alt="Mistral AI Image" width="166" height="100">
</div>

<div style="display: flex; justify-content: space-around;">
  <img src="utils/static/elevenlabs.jpg" alt="ElevenLabs Image" width="166" height="100">
  <img src="utils/static/microsoft.png" alt="Microsoft Image" width="166" height="100">
  <img src="utils/static/prodia.png" alt="Prodia Image" width="166" height="100">
</div>

## Key Functionalities

- [x] ⚡ **Real-Time Responses**: Experience near-instantaneous replies for a smooth and uninterrupted conversation flow.
- [x] 🔍 **Web Search Integration**: Fast-Chat gives 3 modes for search:
  - 🔍 **DuckDuckGo**: Fastest search tool to get quick answers.
  - 🔍 **DeepSearch (Google)**: Most comprehensive search tool to get more informative answers.
  - 🔍 **DuckDuckGo Agentic**: Most powerful search tool to get more accurate answers.
- [x] 📺 **YouTube Comprehension**: Just paste a YouTube video/shorts link and ask anything about it. (Currently supports ~25 mins video with English subtitles)
- [x] 🎙️ **Voice Recognition**: Speak directly to Fast-Chat, and it will accurately interpret and process your queries.
- [x] 🗣️ **Audio Output**: Fast-Chat responds through voice, offering an enhanced and interactive communication experience.
- [x] 🎨 **Image Generation**: Fast-Chat can generate images tailored to your needs.
- [x] 🖼️ **Image Understanding**: Fast-Chat supports images as input, for richer interactions.
- [x] 📝 **Contextual Awareness**: Retain conversation context for more relevant and insightful responses.

## Getting Started

### Prerequisites

- **`Python 3.8`** or higher
- **`git`**
- **`pipenv`** (recommended)
- [🔗GROQ API key](https://console.groq.com/keys)
- [🔗SerpAPI key](https://serpapi.com/dashboard) (optional)
- [🔗ElevenLabs API key](https://elevenlabs.io/app/speech-synthesis/text-to-speech) (optional)
- [🔗Prodia API key](https://app.prodia.com/api) (optional)

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
.env_for_fast_chat\Scripts\Activate
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
      .env_for_fast_chat\Scripts\Activate
      streamlit run app.py
      ```

      ```powershell
      # Deactivate the virtual environment after using Fast-Chat
      deactivate
      ```

      </details>

- When the app is running, use Fast-Chat in your browser at `http://localhost:8501`

## Coming Soon

- [ ] **Document Summarization**: Summarize lengthy documents and articles for quick and easy understanding.
