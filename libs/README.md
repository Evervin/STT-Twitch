# External Libraries (DLLs)

The required NVIDIA CUDA and cuDNN libraries are **too large** to be hosted on GitHub.
The `libs/` folder acts as a placeholder for where you must place these files locally to run the **GPU Model**.

### 📥 Required Files
- `cublas64_12.dll`
- `cublasLt64_12.dll`
- `cudnn64_9.dll` (or simpler: the contents of `libs` from the standalone release)

### 🔗 Where to download?
1. Go to [whisper-standalone-win releases](https://github.com/Purfview/whisper-standalone-win/releases/tag/libs).
2. Download **Twitch-STT-Libs.zip** (or whichever archive contains the required DLLs, usually `libs.zip` or `win_v2`).
3. Extract the **DLL files** directly into this `libs/` folder.

### ⚠️ Note
If you only plan to use the **CPU Model**, you can ignore this folder.
