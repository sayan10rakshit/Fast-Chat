# ⚡Fast-Chat
  
<img src="utils/static/Fast-Chat_avatar.gif" alt="Fast-Chat" width="400">

### An AI chat assistant for Lightning-Fast Conversations

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fast-chat.streamlit.app/)

Engage in a lightning-fast chat conversation with **Fast-Chat**, leveraging the capabilities of **GROQ**'s cutting-edge **Language Processing Unit** (**[GROQ LPU<sup>TM</sup>](https://wow.groq.com/why-groq/)**). Interact with Fast-Chat and receive immediate responses to your inquiries.

#### Powered by

[![Gemma Model](https://img.shields.io/badge/Gemma_Model-OS_Models-blue)](https://ai.google.dev/gemma) [![Llama Model](https://img.shields.io/badge/Llama_Model-OS_Models-violet)](https://llama.meta.com/) [![Mistral AI](https://img.shields.io/badge/Mistral_AI-OS_Models-orange)](https://mistral.ai/news/mixtral-of-experts/) [![Microsoft](https://img.shields.io/badge/Microsoft-OS_Models-blue)](https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/) [![Groq AI](https://img.shields.io/badge/Groq_AI-Inference_Service-black)](https://wow.groq.com/why-groq/) [![Eleven Labs](https://img.shields.io/badge/ElevenLabs-Voice_Synthesis-green)](https://elevenlabs.io/)

<div style="display: flex; justify-content: space-around;">
  <img src="utils/static/groq.jpg" alt="groq image" width="250" height="150">
  <img src="utils/static/gemma.webp" alt="gemma image" width="250" height="150">
  <img src="utils/static/llama.webp" alt="llama image" width="250" height="150">
</div>
<div style="display: flex; justify-content: space-around;">
  <img src="utils/static/mistral_ai_image.jpg" alt="mistral image" width="250" height="150"">
  <img src="utils/static/elevenlabs.jpg" alt="elevenlabs image" width="250" height="150">
  <img src="utils/static/microsoft.png" alt="microsoft image" width="250" height="150">
</div>

## Key Functionalities

- [x] ⚡ **Real-Time Responses**: Enjoy near-instant replies to your queries, ensuring a smooth and seamless conversation flow.
- [x] 🔍 **Web Search Integration**: Fast-Chat can search the web to provide you with accurate and relevant information.
- [x] 📺 **YouTube Comprehension**: Fast-Chat understands and responds to content from YouTube videos and shorts.
- [x] 🎙️ **Voice Recognition**: Speak directly to Fast-Chat, and it will accurately interpret your queries.
- [x] 🗣️ **Audio Output**: Fast-Chat can respond to you through voice, enhancing the interactive experience.
- [x] 🖼️ **Multi-Modal Understanding**: Fast-Chat can analyze and comprehend visual content such as images.
- [x] 📝 **Contextual Awareness**: Fast-Chat retains conversation context, providing more insightful and relevant responses.
- [x] 🤖 **Model Selection**: Customize your experience by selecting from a range of models to meet your specific needs.
- [x] 🪛 **Parameter Tuning**: Fine-tune response settings to personalize and optimize your interactions with Fast-Chat.

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

- [ ] **Image Generation**: Implement image generation capabilities to Fast-Chat.
- [ ] **Agentic Search**: Gives more comprehensive search results to ambiguous queries.
- [ ] **Map Integration**: Integrate maps to provide location-based information.
