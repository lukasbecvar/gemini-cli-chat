# Gemini CLI Chat
Super simple dependency-free Python script for interacting with the Google Gemini API directly from your command line.

## Features
- **Two Modes:** Use it for a single query or in an interactive chat session.
- **Conversation History:** Remembers the context of your conversation.
- **Easy to Read:** Uses colored output to distinguish between user input and model responses.
- **No Dependencies:** Runs using only the standard Python library.

## Setup
1.  **Get a Gemini API Key:** You need an API key from Google AI Studio. You can get one [here](https://aistudio.google.com/app/apikey).
2.  **Add Your Key to the env config:** Open the `.env` file and replace the placeholder value of the `API_KEY` variable with your own key. 
```sh
# gemini API token
API_KEY="API_KEY"

# gemini model
MODEL="gemini-1.5-flash"
```

### Interactive Chat Mode
To start a continuous conversation with the model, run the script without any arguments:
```sh
./gemini-chat.py
```
Type your message, press Enter, and wait for the model's response. To end the session, type `exit` or `quit`.

### Single Message Mode
To send a single message and get a quick response, pass your message as a command-line argument:
```sh
./gemini-chat.py "What is the capital of the Czech Republic?"
```

## License
This software is licensed under the [MIT license](LICENSE). 
