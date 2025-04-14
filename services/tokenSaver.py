import json
import os

FILE_PATH = "data/tokens.json"

def save_token(chat_id, token_data):
    tokens = {}
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            tokens = json.load(f)
    tokens[chat_id] = token_data
    with open(FILE_PATH, "w") as f:
        json.dump(tokens, f, indent=2)

def load_token(chat_id):
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            tokens = json.load(f)
        return tokens.get(chat_id)
    return None
