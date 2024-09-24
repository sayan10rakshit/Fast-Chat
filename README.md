
---

# ⚡ Fast-Chat: Elevating Lightning-Fast Conversations with AI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fast-chat.streamlit.app/)

<img src="utils/static/Fast-Chat_avatar.gif" alt="Fast-Chat" width="400" align="right" />

**Fast-Chat** is a state-of-the-art AI chat assistant designed to facilitate real-time, seamless interactions. Leveraging **GROQ's** cutting-edge **[Language Processing Unit<sup>TM</sup>](https://wow.groq.com/why-groq/)**, Fast-Chat delivers prompt and insightful responses, empowering users with instant answers and dynamic conversations.

## Key Features

- ⚡ **Instant Responses**: Enjoy lightning-fast replies powered by GROQ’s advanced AI technology, ensuring a smooth conversation flow.
- 🔍 **Multi-Mode Web Search Integration**:
  - **DuckDuckGo**: Fast, efficient search for quick answers.
  - **DeepSearch (Google)**: Comprehensive search for detailed insights.
  - **DuckDuckGo Agentic**: Accurate, contextual search with agentic capabilities.
- 📺 **YouTube Understanding**: Analyze YouTube videos (up to 25 mins with English subtitles) by simply pasting a link and asking questions about the content.
- 🎙️ **Voice Interaction**: Talk directly to Fast-Chat with built-in voice recognition, enhancing conversational engagement.
- 🗣️ **Audio Output**: Receive responses in an expressive voice for an immersive, interactive experience.
- 🎨 **Image Generation**: Get custom-generated images based on your requests.
- 🖼️ **Image Interpretation**: Submit images and receive intelligent responses to visual content.
- 📝 **Contextual Continuity**: Retain conversation context for a more tailored and relevant interaction.

---

## Backed By

[![Gemma Model](https://img.shields.io/badge/Gemma-Google_AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/gemma)
[![Llama Model](https://img.shields.io/badge/Llama-Meta_AI-0668E1?style=for-the-badge&logo=meta&logoColor=white)](https://llama.meta.com/)
[![Mistral AI](https://img.shields.io/badge/Mistral-Mistral_AI-FF6B6B?style=for-the-badge&logo=mistralai&logoColor=white)](https://mistral.ai/news/mixtral-of-experts/)
[![Microsoft](https://img.shields.io/badge/Microsoft-Microsoft_Research-00A4EF?style=for-the-badge&logo=microsoft&logoColor=white)](https://azure.microsoft.com/en-us/services/cognitive-services/computer-vision/)
[![Groq AI](https://img.shields.io/badge/Groq-Inference_Platform-000000?style=for-the-badge&logo=groq&logoColor=white)](https://wow.groq.com/why-groq/)
[![Eleven Labs](https://img.shields.io/badge/ElevenLabs-Voice_Synthesis-3D3D3D?style=for-the-badge&logo=elevenlabs&logoColor=white)](https://elevenlabs.io/)
[![Prodia](https://img.shields.io/badge/Prodia-Image_Generation-7B68EE?style=for-the-badge&logo=prodia&logoColor=white)](https://prodia.com/)

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

---

## Getting Started

### Prerequisites

- **Python 3.8** or higher
- **Git**
- **Pipenv** (recommended)
- API Keys:
  - [🔗GROQ API Key](https://console.groq.com/keys)
  - [🔗SerpAPI Key](https://serpapi.com/dashboard) (optional)
  - [🔗ElevenLabs API Key](https://elevenlabs.io/app/speech-synthesis/text-to-speech) (optional)
  - [🔗Prodia API Key](https://app.prodia.com/api) (optional)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/sayan10rakshit/Fast-Chat.git
   cd Fast-Chat
   ```

2. Install dependencies using **Pipenv** or **venv**:

   - **Using Pipenv**:

     ```bash
     pipenv install
     ```

   - **Using venv**:

     ```bash
     python3 -m venv .env_for_fast_chat
     source .env_for_fast_chat/bin/activate
     pip install -r requirements.txt
     ```

   > 🚨 **Tip**: If you encounter issues, try replacing `python3` with `python`.

---

## Usage

- **Launch Fast-Chat via Streamlit**:
  - **Using Pipenv**:

    ```bash
    pipenv run streamlit run app.py
    ```

    or activate the environment first:

    ```bash
    pipenv shell
    streamlit run app.py
    ```

  - **Using venv**:

    ```bash
    source .env_for_fast_chat/bin/activate
    streamlit run app.py
    ```

  - For Windows:

    ```powershell
    .env_for_fast_chat\Scripts\Activate
    streamlit run app.py
    ```

Once running, access **Fast-Chat** in your browser at `http://localhost:8501`.

---

## Roadmap

- [ ] **Document Summarization**: Enable summarization of lengthy articles and documents for easy comprehension.

---
