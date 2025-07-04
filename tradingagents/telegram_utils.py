import os
import requests


def send_telegram_message(text: str) -> None:
    """Send a message to a Telegram chat using the bot API."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if not token or not chat_id:
        return
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    try:
        requests.post(url, data={'chat_id': chat_id, 'text': text})
    except Exception:
        pass
