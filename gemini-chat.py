#!/usr/bin/python3
import sys
import json
import os
import urllib.request

# load environment variables from .env file
def load_env(file_path=".env"):
    if os.path.exists(file_path):
        with open(file_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    os.environ[key] = value.strip("\"")

# get the directory where the script is located 
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

# load main .env file to get ENV_NAME
load_env(os.path.join(SCRIPT_DIR, ".env"))

# determine which environment-specific .env file to load
ENV = os.getenv("ENV_NAME", "dev").lower()
ENV_FILE = f".env.{ENV}"

# load environment-specific .env file
load_env(os.path.join(SCRIPT_DIR, ENV_FILE))

# set gemini API config
API_KEY = os.getenv("API_KEY")
MODEL = os.getenv("MODEL")

# check if API_KEY and MODEL are set
if not API_KEY or not MODEL:
    print(f"[ERROR] Please set API_KEY and MODEL in your {ENV_FILE} file.")
    sys.exit(1)

# gemini API endpoint
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

# ANSI color codes
COLOR_USER = "\033[94m"    # blue
COLOR_MODEL = "\033[92m"   # green
COLOR_RESET = "\033[0m"    # reset

chat_history = []

def send_message_to_gemini(contents):
    headers = { "Content-Type": "application/json" }
    data = json.dumps({ "contents": contents }).encode("utf-8")

    # send request to gemini API
    req = urllib.request.Request(ENDPOINT, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            return text.strip()
    except Exception as e:
        return f"[ERROR] {e}"

def chat_once(message):
    # priming + user message
    contents = [
        {
            "role": "user",
            "parts": [{ "text": "Jsi chytrý AI asistent. Odpovídej srozumitelně a výstižně." }]
        },
        {
            "role": "user",
            "parts": [{ "text": message }]
        }
    ]
    response = send_message_to_gemini(contents)
    print(f"{COLOR_MODEL}Gemini: {COLOR_RESET}{response}")

def main():
    if len(sys.argv) > 1:
        msg = " ".join(sys.argv[1:])
        chat_once(msg)
    else:
        chat_history.append({
            "role": "user",
            "parts": [{ "text": "Jsi chytrý AI asistent. Odpovídej srozumitelně a výstižně." }]
        })

        while True:
            user_input = input(f"{COLOR_USER}User: {COLOR_RESET}").strip()
            if user_input.lower() in ("exit", "quit"):
                print(f"{COLOR_MODEL}Konec.{COLOR_RESET}")
                break

            # append user input to chat history
            chat_history.append({
                "role": "user",
                "parts": [{ "text": user_input }]
            })

            # send message to gemini
            response_text = send_message_to_gemini(chat_history)

            # append response to chat history
            chat_history.append({
                "role": "model",
                "parts": [{ "text": response_text }]
            })

            # print response
            print(f"{COLOR_MODEL}Gemini: {COLOR_RESET}{response_text}")

if __name__ == "__main__":
    main()
