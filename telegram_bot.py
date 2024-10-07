import requests

# Configuration for Telegram
TELEGRAM_BOT_TOKEN = 'BOT_TOKEN'  # Replace with your bot's API token
TELEGRAM_CHAT_ID = 'CHAT_ID'  # Replace with your chat ID

def send_message(message):
    """
    Sends a message to a specified Telegram chat using the Telegram Bot API.
    """
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'  # Optional: Enables Markdown formatting
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("✅ Telegram message sent successfully.")
        else:
            print(f"❌ Failed to send Telegram message. Status Code: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Exception occurred while sending Telegram message: {e}")
