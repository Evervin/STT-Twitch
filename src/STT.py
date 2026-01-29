import os
import sys
# Finds the 'libs' folder relative to this script
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dll_dir = os.path.join(project_root, "libs")
if os.path.exists(dll_dir):
    # Fix 1: Add to Python's DLL search (for Python 3.8+)
    os.add_dll_directory(dll_dir)
    # Fix 2: Add to System PATH (for the underlying C++ libraries)
    os.environ["PATH"] = dll_dir + os.pathsep + os.environ["PATH"]
import sounddevice as sd
import numpy as np
import queue
import threading
from faster_whisper import WhisperModel, download_model

global output_text
global is_running
global run_staus
global model_choice

model_choice = "CPU"
output_text = ""
is_running = False
#Settings
sample_rate = 16000
block_duration = 0.5  # seconds
frames_per_block = int(sample_rate * block_duration)
channels = 1

audio_queue = queue.Queue()
audio_buffer = []
def LoadModel():
    global model
    local_model_path = os.path.join(os.path.dirname(__file__), "models", "small.en")
    if model_choice == "CPU":
        model =  WhisperModel(local_model_path, device="cpu", compute_type="int8")
    elif model_choice == "GPU":
        model =  WhisperModel(local_model_path, device="cuda", compute_type="int8_float16")
def audio_callback(indata, frames, time, status):  
    if status:
        print(status)
    audio_queue.put(indata.copy())

def recorder():
        with sd.InputStream(samplerate=sample_rate, channels=channels, callback=audio_callback, blocksize=frames_per_block):
            while is_running:
                sd.sleep(1000)

def is_silent(audio_block, threshold=0.025):
    energy = np.sqrt(np.mean(audio_block**2))
    return energy < threshold

def transcriber():
    global audio_buffer
    global output_text

    silent_blocks = 0

    while is_running:
        block = audio_queue.get()
        if is_silent(block):
            silent_blocks += 1
            
            if silent_blocks >= 5 and len(audio_buffer) > 0:
                audio_data = np.concatenate(audio_buffer).flatten().astype(np.float32)
                audio_buffer = []  # Clear buffer
                silent_blocks = 0  # Reset counter
                
                # TRANSCRIBE
                segments, _ = model.transcribe(audio_data, language="en", beam_size=5)
                full_sentence = [segment.text for segment in segments]
                if full_sentence:
                    output_text = "".join(full_sentence).strip()
                    print(f"{output_text}",end="\n--|end of transcription|--\n")    

        else:
            # This block has SPEECH
            silent_blocks = 0  # Reset silence counter
            audio_buffer.append(block)  # Store it

if __name__ == "__main__":
    is_running = True
    LoadModel()
    threading.Thread(target=recorder, daemon=True).start()
    transcriber()


"""       
 chunk based transcription where we process fixed-size chunks regardless of silence
        total_frames = sum(len(b) for b in audio_buffer)
        if total_frames >= frames_per_chunk:
            audio_data = np.concatenate(audio_buffer)[:frames_per_chunk]
            audio_buffer = []

            audio_data = audio_data.flatten().astype(np.float32)
        
            #transcription without timestamps
            segments, _ = model.transcribe(
                audio_data,
                language="en",
                beam_size=5
            )
            for segment in segments:
                print(f"[{segment.text}")
-------------------------------------------------------------------------------
            old segment logic
                # for segment in segments:
                #     output_text = segment.text + ""
                # print(f"{output_text}")
                # print("---- End of This Transcription Sequence----")
"""
