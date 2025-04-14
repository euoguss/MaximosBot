import requests

class Waha:
    def __init__(self):
        self.__api_url = "https://waha.codegus.space"

    def send_message(self, chat_id, message):
        url = f"{self.__api_url}/api/sendText"
        headers = {"Content-Type": "application/json"}
        payload = {
            "session": "default",
            "chatId": chat_id,
            "text": message,
        }
        response = requests.post(url=url, json=payload, headers=headers)
        print(f"[send_message] {response.status_code} - {response.text}")

    def get_history_messages(self, chat_id, limit):
        url = f"{self.__api_url}/api/default/chats/{chat_id}/messages?limit={limit}&downloadMedia=false"
        headers = {"Content-Type": "application/json"}
        response = requests.get(url=url, headers=headers)
        try:
            return response.json()
        except Exception as e:
            print(f"[get_history_messages] JSON decode error: {e}")
            return None

    def start_typing(self, chat_id):
        url = f"{self.__api_url}/api/startTyping"
        headers = {"Content-Type": "application/json"}
        payload = {
            "session": "default",
            "chatId": chat_id,
        }
        response = requests.post(url=url, json=payload, headers=headers)
        print(f"[start_typing] {response.status_code} - {response.text}")

    def stop_typing(self, chat_id):
        url = f"{self.__api_url}/api/stopTyping"
        headers = {"Content-Type": "application/json"}
        payload = {
            "session": "default",
            "chatId": chat_id,
        }
        response = requests.post(url=url, json=payload, headers=headers)
        print(f"[stop_typing] {response.status_code} - {response.text}")
