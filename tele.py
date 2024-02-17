import requests
from threading import Thread

from secretos import telegram as telesecs

yo = telesecs["chats"]["yo"]


def asyncronous(f):
    """decorator to disengage function from the main thread"""
    def wrap(*args, **kwargs):
        thread = Thread(target=f, args=args, kwargs=kwargs)
        thread.start()
        return thread
    return wrap


@asyncronous
def send_message(bot, chat, text):
    bot_id = telesecs["bots"].get(bot, {}).get("bot_id", "")
    chat_id = telesecs["chats"][chat]
    url = f"https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={text}&parse_mode=Markdown&disable_web_page_preview=true"
    requests.post(url)


if __name__ == "__main__":
    send_message("archi", "yo", "Bon dia from DavidRusca's website")

