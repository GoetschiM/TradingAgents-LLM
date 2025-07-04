import os
import requests


def send_telegram_message(text: str, chunk_size: int = 4000) -> None:
    """Send a message to a Telegram chat using the bot API.

    Telegram limits messages to 4096 characters, so longer messages are split
    into chunks.
    """
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        for i in range(0, len(text), chunk_size):
            requests.post(url, data={"chat_id": chat_id, "text": text[i : i + chunk_size]})
    except Exception:
        pass
