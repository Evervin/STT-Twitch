import tkinter as tk
import src.STT as STT
import src.twitch as Twitch
import threading

rec_thread = None
trans_thread = None
outputTXT = ""
twitch_thread = None
runTwitchMsg = False
import os
import sys
import traceback

# CRASH DIAGNOSTICS
def handle_exception(exc_type, exc_value, exc_traceback):
    log_path = os.path.join(os.path.dirname(__file__), "app_crash_report.txt")
    with open(log_path, "w") as f:
        f.write("--- INTERNAL APP CRASH REPORT ---\n")
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)
    print(f"CRASH LOG WRITTEN TO: {log_path}")
    sys.exit(1)

sys.excepthook = handle_exception

def get_path(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)



def toggle_twitch():
    global runTwitchMsg
    runTwitchMsg = not runTwitchMsg
    if runTwitchMsg:
        twitch_btn_toggle.config(text="Twitch: ON", bg="purple", fg="white")
    else:
        twitch_btn_toggle.config(text="Twitch: OFF", bg="SystemButtonFace", fg="black")

def save_config(window, token_entry):
    new_token = token_entry.get().strip()
    Twitch.TOKEN = new_token
    Twitch.save_token(new_token)
    print("Configuration Saved!")
    window.destroy()

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y-60}")

def update_labels():
    output_lbl.config(text=STT.output_text)
    if STT.is_running:
        
        statlbl.place(x=140, y=50)
        statlbl.config(text="STATUS: Running")
        start_btn.config(state="disabled")
        stop_btn.config(state="normal")
        twitch_btn_toggle.config(state="disabled")
    elif (rec_thread and rec_thread.is_alive()) or (trans_thread and trans_thread.is_alive()):
        statlbl.place(x=90, y=50)
        statlbl.config(text="STATUS: Processing Shutdown. . .")
        twitch_btn_toggle.config(state="disabled")
    else:
        statlbl.place(x=140, y=50)
        statlbl.config(text="STATUS: Standby")
        start_btn.config(state="normal")
        stop_btn.config(state="disabled")
        twitch_btn_toggle.config(state="normal")

    master.after(100, update_labels)  # Schedule the function to run again after 1 second

def set_model(choice):
    # Disable buttons to prevent double-clicks and show loading state
    for child in launcher.winfo_children():
        if isinstance(child, tk.Button):
            child.config(state="disabled")
    launcher.title(f"Loading {choice} Model...")
    launcher.update() # Force UI refresh
    
    try:
        STT.model_choice = choice
        STT.LoadModel()
        launcher.destroy()
    except Exception as e:

        import traceback
        error_details = traceback.format_exc()
        from tkinter import messagebox
        messagebox.showerror("Model Load Error", f"A crash occurred during model loading:\n\n{error_details}")

def start_transcription():
    global rec_thread, trans_thread, twitch_thread
    STT.is_running = True

    rec_thread = threading.Thread(target=STT.recorder, daemon=True)
    rec_thread.start()

    trans_thread = threading.Thread(target=STT.transcriber, daemon=True)
    trans_thread.start()

    # Launch Twitch Thread if enabled
    if runTwitchMsg:
        twitch_thread = threading.Thread(target=Twitch.send_twitch_message, daemon=True)
        twitch_thread.start()

def stop_transcription():
    STT.is_running = False

def ConfigWindowOpen():
    configWindow = tk.Toplevel(master)
    configWindow.title("Configuration")
    center_window(configWindow, 400, 200)
    
    tk.Label(configWindow, text="Paste Twitch Access Token:", font=("Arial", 10)).pack(pady=10)
    AccessTokenEntry = tk.Entry(configWindow, width=40)
    AccessTokenEntry.insert(0, Twitch.TOKEN) # Show current token
    AccessTokenEntry.pack(pady=5)

    tk.Button(configWindow, text="Save & Close", command=lambda: save_config(configWindow, AccessTokenEntry)).pack(pady=20)

if __name__ == "__main__":
    launcher = tk.Tk()
    launcher.title("Select Model")
    icon_p = get_path("icon.ico")
    if os.path.exists(icon_p):
        try:
            launcher.iconbitmap(icon_p)
        except:
            pass
            
    center_window(launcher, 300, 150)

    lbl = tk.Label(launcher, text="Select STT Model", font=("Arial Bold", 14)).pack(pady=10)
    cpu_btn = tk.Button(launcher, text="CPU Model(UNIVERSAL USAGE)", command=lambda: set_model("CPU")).pack(pady=5)
    gpu_btn = tk.Button(launcher, text="GPU Model(NVIDIA ONLY)", command=lambda: set_model("GPU")).pack(pady=5)
    
    launcher.mainloop()

    # Main application window
    try:
        master = tk.Tk()
        master.title("STT Twitch Chat integration")
        
        master_icon = get_path("icon.ico")
        if os.path.exists(master_icon):
            try:
                master.iconbitmap(master_icon)
            except:
                pass
                
        center_window(master, 400, 250)
        
        lbl = tk.Label(master, text="STT V.0.1", font=("Arial Bold", 14))
        lbl.place(x=150, y=15)
        
        statlbl = tk.Label(master, text=f"STATUS:{STT.is_running}", font=("Arial", 10))
        statlbl.place(x=140, y=50)
        
        config_btn = tk.Button(master, text="Config Token", command=ConfigWindowOpen)
        config_btn.place(x=20, y=15)

        stop_btn = tk.Button(master, text="Stop All", command=stop_transcription, state="disabled")
        stop_btn.place(x=20, y=85)
        
        twitch_btn_toggle = tk.Button(master, text="Twitch: OFF", command=toggle_twitch)
        twitch_btn_toggle.place(x=280, y=15, width=100)

        start_btn = tk.Button(master, text="START STT", command=start_transcription, font=("Arial Bold", 10), bg="green", fg="white")
        start_btn.place(x=280, y=85, width=100)
        
        output_lbl = tk.Label(master, text="", wraplength=380, height=5, justify="left")
        output_lbl.place(x=10, y=120)

        master.after(100, update_labels)
        
        def on_closing():
            STT.is_running = False
            master.destroy()
            sys.exit(0)

        master.protocol("WM_DELETE_WINDOW", on_closing)
        master.mainloop()
    except Exception as e:
        import traceback
        from tkinter import messagebox
        error_msg = traceback.format_exc()
        messagebox.showerror("Critical Error", f"Application crashed:\n\n{error_msg}")


