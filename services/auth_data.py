import json
import os

DATA_FILE = "data/auth_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                data = json.load(f)
            except Exception:
                data = {"states": {}, "tokens": {}}
    else:
        data = {"states": {}, "tokens": {}}
    if "states" not in data:
        data["states"] = {}
    if "tokens" not in data:
        data["tokens"] = {}
    return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def store_oauth_state(chat_id, state):
    data = load_data()
    data["states"] = {k: v for k, v in data["states"].items() if v != chat_id}
    data["states"][state] = chat_id
    save_data(data)

def get_chat_id_by_state(state):
    data = load_data()
    chat_id = data["states"].pop(state, None)
    save_data(data)
    return chat_id

def save_token(chat_id, token_data):
    data = load_data()
    data["tokens"][chat_id] = token_data
    save_data(data)

def load_token(chat_id):
    data = load_data()
    return data["tokens"].get(chat_id)
