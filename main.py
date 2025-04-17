from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from services.waha import Waha
from services.calendar import CalendarService
from services.login import NextCloudOAuth
from bot.ai_bot import AIBot
from services.auth_data import *

app = FastAPI()

@app.get("/")
async def index():
    return "servidor subiu papai"

@app.post("/chatbot/webhook/")
async def webhook(request: Request):
    data = await request.json()
    chat_id = data["payload"]["from"]
    message = data["payload"]["body"].strip().lower()

    if "g@us" in chat_id or "status@broadcast" in chat_id:
        return JSONResponse({"status": "success", "message": "ignorado"})

    waha = Waha()
    waha.start_typing(chat_id)

    if message == "!login":
        oauth = NextCloudOAuth()
        auth_url, state = oauth.get_authorization()
        store_oauth_state(chat_id, state)
        waha.send_message(chat_id, f"Clique aqui para se logar: {auth_url}")
        waha.stop_typing(chat_id)
        return JSONResponse({"status": "ok"})

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
        return JSONResponse({"status": "ok"})

    history = waha.get_history_messages(chat_id, 10)
    ai_bot = AIBot()
    response = ai_bot.invoke(history, data["payload"]["body"])
    waha.send_message(chat_id, response)
    waha.stop_typing(chat_id)

    return JSONResponse({"status": "success"})

@app.get("/oauth/start")
async def oauth_start(chat_id: str):
    oauth = NextCloudOAuth()
    auth_url, state = oauth.get_authorization()
    store_oauth_state(chat_id, state)
    return {"url": auth_url}

@app.get("/oauth/callback")
async def oauth_callback(request: Request):
    oauth = NextCloudOAuth()
    full_url = str(request.url)
    token_data = oauth.fetch_token(full_url)
    chat_id = get_chat_id_by_state(request.query_params.get("state"))
    save_token(chat_id, token_data)
    return token_data
