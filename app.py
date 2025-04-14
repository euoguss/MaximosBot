from flask import Flask, request, jsonify
from services.waha import Waha
from services.calendar import CalendarService
from services.login import NextCloudOAuth
from bot.ai_bot import AIBot
from services.auth_data import *

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "servidor subiu papai"

@app.route("/chatbot/webhook/", methods=["POST"])
def webhook():
    data = request.json
    chat_id = data["payload"]["from"]
    message = data["payload"]["body"].strip().lower()

    if "g@us" in chat_id or "status@broadcast" in chat_id:
        return jsonify({'status': 'success', 'message': 'ignorado'}), 200

    waha = Waha()
    waha.start_typing(chat_id)

    if message == "!login":
        oauth = NextCloudOAuth()
        auth_url, state = oauth.get_authorization()
        store_oauth_state(chat_id, state)
        waha.send_message(chat_id, f"Clique aqui para se logar: {auth_url}")
        waha.stop_typing(chat_id)
        return jsonify({"status": "ok"}), 200

    if message == "!agenda":
        token_data = load_token(chat_id)
        if not token_data:
            waha.send_message(chat_id, "Você ainda não está logado. Envie !login para entrar.")
        else:
            calendar = CalendarService(token_data["access_token"])
            events = calendar.get_events_today()
            if events:
                waha.send_message(chat_id, "Eventos de hoje:\n" + "\n".join(f"• {e}" for e in events))
            else:
                waha.send_message(chat_id, "Você não tem eventos hoje.")
        waha.stop_typing(chat_id)
        return jsonify({"status": "ok"}), 200

    history = waha.get_history_messages(chat_id, 10)
    ai_bot = AIBot()
    response = ai_bot.invoke(history, data["payload"]["body"])
    waha.send_message(chat_id, response)
    waha.stop_typing(chat_id)

    return jsonify({"status": "success"}), 200

@app.route("/oauth/start", methods=["GET"])
def oauth_start():
    chat_id = request.args.get("chat_id")
    oauth = NextCloudOAuth()
    auth_url, state = oauth.get_authorization()
    store_oauth_state(chat_id, state)
    return jsonify({"url": auth_url})

@app.route("/oauth/callback", methods=["GET", "POST"])
def oauth_callback():
    oauth = NextCloudOAuth()
    full_url = request.url
    token_data = oauth.fetch_token(full_url)
    chat_id = get_chat_id_by_state(request.args.get("state"))
    save_token(chat_id, token_data)

    return jsonify(token_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)