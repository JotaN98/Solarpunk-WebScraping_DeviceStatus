import requests

def send_message(message):
    #Sends a message to a specified Telegram chat using the Telegram Bot API.

    with open("tokens.gitignore") as f:
        text = f.readlines()
        # Configuration for Telegram
        bot_token = text[0].strip()  # BOT API TOKEN
        chat_id = text[1].strip()  # CHAT ID

    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
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
