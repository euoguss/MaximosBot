oauth_states = {}

def store_oauth_state(chat_id, state):
    oauth_states[state]= chat_id

def get_chat_id_by_state(state):
    return oauth_states.pop(state, None)