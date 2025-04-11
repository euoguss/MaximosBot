import requests

class Waha:

    def __init__(self):
        self.__api_url = "http://waha.codegus.space"

    def send_message(self, chat_id, message):
        url = f"{self.__api_url}/api/sendText"
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "session": "default",
            "chatId": chat_id,
            "text": message,
        }
        requests.post(
            url=url,
            json=payload,
            headers=headers,
        )
    
    def get_history_messages(self, chat_id, limit):
        url = f"{self.__api_url}/api/default/chats/{chat_id}/messages?limit{limit}&downloadMedia=false"
        headers = {
            "Content-Type" : "application/json",
        }
        reponse = requests.get(
            url=url,
            headers=headers,
        )
        return reponse.json()

    def start_typing(self, chat_id):
        url = f"{self.__api_url}/api/startTyping"
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "session": "default",
            "chatId": chat_id,
        }
        requests.post(
            url=url,
            json=payload,
            headers=headers,
        )

    def stop_typing(self, chat_id):
        url = f"{self.__api_url}/api/startTyping"
        headers = {
            "Content-Type": "application/json",
        }
        payload = {
            "session": "default",
            "chatId": chat_id,
        }
        requests.post(
            url=url,
            json=payload,
            headers=headers,
        )
