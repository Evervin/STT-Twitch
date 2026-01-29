# STT Twitch Chat Integration

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)

A high-performance **Speech-to-Text (STT)** application that integrates directly with Twitch chat. Dictate your messages in real-time and have them sent to your stream chat instantly using AI-powered transcription.

![STT Preview](icon.ico)

## Features

- **Real-time Transcription**: Powered by `faster-whisper` for near-instant speech processing.
- **Twitch Integration**: Connects via SSL to your Twitch IRC for secure messaging.
- **Hybrid AI Models**: Choose between **CPU** (Low resource) and **GPU** (NVIDIA/CUDA) models.
- **Configurable**: Built-in UI to manage your Twitch tokens safely.
- **Secure**: Uses OAuth2 tokens and SSL-encrypted IRC connections.

## Getting Started

### 1. Prerequisites
- **Python**: 3.13 or higher.
- **FFmpeg**: Essential for audio handling. [Download here](https://ffmpeg.org/download.html).

### 2. Installation
Clone the repository:
```bash
git clone https://github.com/Evervin/STT-Twitch.git
cd STT-Twitch
```

Install dependencies (we recommend `uv` but `pip` works too):
```bash
# Option A: Using uv (Recommended)
uv pip install .

# Option B: Standard pip
pip install -r requirements.txt
```

### 3. GPU Acceleration (Optional)
This project requires large external DLLs for NVIDIA GPU acceleration which are **not included** in this repo.
**[Read the libs/README.md](libs/README.md) for download instructions.**

If you skip this, only the **CPU Model** will work.

## Configuration

1. Launch the app: `python main.py`
2. Click **Config Token**.
3. Generate your token at [TwitchTokenGenerator](https://twitchtokengenerator.com/).
   - **Important**: When generating the token, ensure you select the following scopes:
     - `chat:read`
     - `chat:edit`
   - These permissions are required for the bot to read and post in your chat.
4. Paste the generated Access Token into the configuration window.
5. Click **Save & Close**.
6. Toggle **Twitch: ON** and click **START STT**.

## Project Structure

```text
├── main.py            # GUI Entry Point
├── src/
│   ├── STT.py         # Whisper Audio Logic
│   └── twitch.py      # Twitch IRC Logic
├── libs/              # PLACE DLLs HERE (See separate README)
├── config.json        # Your local settings (Ignored by Git)
└── requirements.txt   # Python Dependencies
```

## License

Distributed under the MIT License. See `LICENSE` for details.
