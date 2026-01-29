import socket
import ssl
import time
import requests
import json
import os
import src.STT as STT

# Global variables to hold user data
CONFIG_FILE = "config.json"

def save_token(token):
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump({"token": token}, f)
        print("Token saved to config.json")
    except Exception as e:
        print(f"Error saving token: {e}")

def load_token():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                data = json.load(f)
                return data.get("token", "")
        except Exception as e:
            print(f"Error loading token: {e}")
    return ""

TOKEN = load_token()
USER_NAME = ""

def get_username_from_token(token):
    clean_token = token.replace("oauth:", "")
    url = "https://id.twitch.tv/oauth2/validate"
    headers = {"Authorization": f"OAuth {clean_token}"}
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()['login']
    except:
        return None
    return None

def send_twitch_message():
    global TOKEN, USER_NAME
    
    # Validation check
    if not TOKEN:
        print("Twitch Error: No Token Provided")
        return

    USER_NAME = get_username_from_token(TOKEN)
    if not USER_NAME:
        print("Twitch Error: Invalid Token")
        return

    target_channel = f"#{USER_NAME.lower()}"
    
    # STEALTH SSL SETUP
    context = ssl.create_default_context()
    raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = context.wrap_socket(raw_sock, server_hostname="irc.chat.twitch.tv")

    try:
        sock.connect(("irc.chat.twitch.tv", 443)) # Stealth port
        sock.send(f"PASS {TOKEN if TOKEN.startswith('oauth:') else 'oauth:'+TOKEN}\r\n".encode("utf-8"))
        sock.send(f"NICK {USER_NAME.lower()}\r\n".encode("utf-8"))
        sock.send(f"JOIN {target_channel}\r\n".encode("utf-8"))
        sock.setblocking(False)

        print(f"Twitch Bot: Connected to {target_channel}")
        last_sent = ""

        while STT.is_running:
            # 1. PING/PONG Keep-alive
            try:
                data = sock.recv(1024).decode("utf-8")
                if data.startswith("PING"):
                    sock.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            except (BlockingIOError, ssl.SSLWantReadError):
                pass 

            # 2. Check and Send STT
            current_text = STT.output_text.strip()
            if current_text and current_text != last_sent:
                message = f"PRIVMSG {target_channel} :{current_text}\r\n"
                sock.send(message.encode("utf-8"))
                last_sent = current_text
                print(f"Twitch Sent: {current_text}")

            time.sleep(0.5) 
            
    except Exception as e:
        print(f"Twitch Connection Lost: {e}")
    finally:
        sock.close()