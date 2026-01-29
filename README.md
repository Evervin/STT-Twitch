# STT Twitch Chat Integration

A powerful Speech-to-Text (STT) application that integrates directly with Twitch chat, allowing streamers to dictate messages in real-time. Built using `faster-whisper` for high-performance transcription and `tkinter` for a simple, user-friendly interface.

## 🚀 Features

- **Real-time Transcription**: Converts speech to text with low latency using Whisper models.
- **Twitch Integration**: Automatically sends transcribed text to your Twitch chat as a message.
- **Model Flexibility**: Choose between CPU (universal) and GPU (NVIDIA only) models for optimal performance.
- **Stealth IRC Connection**: Secure and efficient connection to Twitch servers.
- **Easy Configuration**: Simple UI for managing your Twitch Access Token.

## 📋 Prerequisites

- **Python**: 3.13 or higher recommended.
- **FFmpeg**: Required for audio processing (ensure it's in your system PATH).
- **GPU Usage**: Requires an NVIDIA GPU with CUDA support for the GPU model.

## 🛠️ Installation

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/Evervin/STT-Twitch
    cd STT-Twitch-App
    ```

2.  **Install dependencies**:
    It is recommended to use a virtual environment.
    ```bash
    uv pip install .
    ```
    *Note: If you are not using `uv`, you can use `pip install -r requirements.txt`.*

3.  **External Libraries (CUDA support)**:
    Due to file size limits, some CUDA DLLs (like `cublasLt64_12.dll`) and Whisper models are excluded from this repository.
    -   **CUDA DLLs**: If you have an NVIDIA GPU, download the **win V2 installation** from the [whisper-standalone-win releases](https://github.com/Purfview/whisper-standalone-win/releases/tag/libs). Extract the contents and place the DLLs in the `libs/` directory.
    -   **Whisper Models**: The application will attempt to download models automatically, or you can manually place them in `src/models/`.

## ⚙️ Configuration

1.  Launch the application.
2.  Click the **Config Token** button.
3.  Paste your Twitch Access Token (start with `oauth:`). You can obtain one from [TwitchTokenGenerator](https://twitchtokengenerator.com/).
4.  Click **Save & Close**.

## 🎮 Usage

1.  **Select Model**: When prompted, choose either **CPU** or **GPU** model based on your hardware.
2.  **Enable Twitch**: Click the **Twitch: OFF** button to toggle it to **Twitch: ON** if you want messages sent to chat.
3.  **Start STT**: Click **START STT** to begin recording and transcribing.
4.  **Stop**: Click **Stop All** to end the session.

## 📂 Project Structure

- `main.py`: Entry point for the GUI application.
- `src/STT.py`: Logic for audio recording and Whisper transcription.
- `src/twitch.py`: Logic for Twitch IRC connection and message sending.
- `libs/`: Directory for external DLL dependencies.

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
