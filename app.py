from flask import Flask, request, jsonify

from services.waha import Waha
from services.calendar import CalendarService
from services.login import NextCloudOAuth
from bot.ai_bot import AIBot
from services.tokenSaver import save_token, load_token
from services.oauthState import store_oauth_state, get_chat_id_by_state


app= Flask(__name__)

@app.route("/")
def index():
    return "servidor subiu papai"

@app.route("/chatbot/webhook/", methods=["POST"])
def webhook():
    data= request.json

    waha= Waha()
    ai_bot= AIBot()
    oauth = NextCloudOAuth()

    chat_id= data["payload"]["from"]
    received_message= data["payload"]["body"]
    is_group= "g@us" in chat_id
    is_status= "status@broadcast" in chat_id

    if is_group or is_status:
        return jsonify({'status': 'success', 'message': 'Mensagem de grupo/status ignorada.'}), 200
    
    waha.start_typing(chat_id)

    if received_message.lower().strip() == "!login":
        auth_url, state= oauth.get_authorization()
        store_oauth_state(chat_id, state)
        waha.send_message(chat_id, f"Clique aqui para se logar: {auth_url}")
        return jsonify({"status": "ok"}), 200

    if received_message.lower().strip() == "!agenda":
        token_data = load_token(chat_id)
        if not token_data:
            response = "Voce ainda não esta logado. Envie !login para entrar"
        else:
            calendar = CalendarService(token_data["acess_token"])
            events= calendar.get_events_today()

            if events:
                response= "Eventos de hoje são: ".join(f"{event}" for event in events)
        waha.send_message(chat_id, response)
        return jsonify({"status": "ok"}), 200

    history_messages= waha.get_history_messages(chat_id, 10)

    response_message= ai_bot.invoke(history_messages, received_message)

    waha.send_message(chat_id, response_message)

    waha.stop_typing(chat_id)                                               
    
    return jsonify({"status": "success"}), 200


@app.route("/oauth/start", methods=["GET"])
def oauth_start():
    oauth = NextCloudOAuth()
    chat_id = request.args.get("chat_id")
    auth_url, state = oauth.get_authorization()
    store_oauth_state(chat_id, state)
    return jsonify({"url": auth_url})


@app.route("/oauth/callback")
def oauth_callback():
    oauth= NextCloudOAuth()
    full_url= request.url
    token_data= oauth.fetch_token(full_url)
    chat_id = get_chat_id_by_state(request.args.get("state"))
    save_token(chat_id, token_data)
    return jsonify(token_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

