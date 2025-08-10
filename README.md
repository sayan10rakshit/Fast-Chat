# ⚡ Fast-Chat: Elevating Lightning-Fast Conversations with AI

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://fast-chat.streamlit.app/)

<img src="utils/static/Fast-Chat_avatar.gif" alt="Fast-Chat" width="400" align="right" />

---
## Key Features

- ⚡ **Instant Responses**: Enjoy lightning-fast replies powered by GROQ’s advanced AI technology, ensuring a smooth conversation flow.
- 🔍 **Multi-Mode Web Search Integration**:
  - **DuckDuckGo**: Fast, efficient search for quick answers.
  - **DeepSearch (Google)**: Comprehensive search for detailed insights.
  - **DuckDuckGo Agentic**: Accurate, contextual search with agentic capabilities.
- 📺 **YouTube Understanding**: Analyze YouTube videos (up to 25 mins with English subtitles) by simply pasting a link and asking questions about the content.
- 🎙️ **Voice Interaction**: Talk directly to Fast-Chat with built-in voice recognition, enhancing conversational engagement.
- 🗣️ **Audio Output**: Receive responses in an expressive voice for an immersive, interactive experience.
- 🖼️ **Image Interpretation**: Submit images and receive intelligent responses to visual content.
- 📝 **Contextual Continuity**: Retain conversation context for a more tailored and relevant interaction.

---


<div style="text-align: center; margin-bottom: 30px;">
  <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; max-width: 600px; margin: 0 auto;">
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
      <img src="utils/static/groq-circle.webp" alt="Groq" width="35" height="35" style="border-radius: 50%;">
      <span style="font-weight: bold; font-size: 16px;">Groq</span>
    </div>
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
      <img src="utils/static/openai.webp" alt="OpenAI" width="35" height="35" style="border-radius: 50%;">
      <span style="font-weight: bold; font-size: 16px;">OpenAI</span>
    </div>
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
      <img src="utils/static/Meta_logo.webp" alt="Meta" width="35" height="25" style="border-radius:0%;">
      <span style="font-weight: bold; font-size: 16px;">Meta</span>
    </div>
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
      <img src="utils/static/deepseek_logo.webp" alt="DeepSeek" width="35" height="35" style="border-radius: 50%;">
      <span style="font-weight: bold; font-size: 16px;">DeepSeek</span>
    </div>
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
      <img src="utils/static/moonshot_logo.webp" alt="Moonshot AI" width="35" height="35" style="border-radius: 50%;">
      <span style="font-weight: bold; font-size: 16px;">Moonshot AI</span>
    </div>
    <div style="display: flex; align-items: center; justify-content: center; gap: 10px;">
      <img src="utils/static/qwen_logo.webp" alt="Alibaba Cloud" width="35" height="35" style="border-radius: 50%;">
      <span style="font-weight: bold; font-size: 16px;">Alibaba Cloud</span>
    </div>
  </div>
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
