import json

STATE_FILE = "oauth_state.json"

def store_oauth_state(chat_id, state):
    data = {}
    try:
        with open(STATE_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        pass

    data[state] = chat_id

    with open(STATE_FILE, "w") as file:
        json.dump(data, file, indent=2)

def get_chat_id_by_state(state):
    try:
        with open(STATE_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return None

    chat_id = data.pop(state, None)

    with open(STATE_FILE, "w") as file:
        json.dump(data, file, indent=2)

    return chat_id