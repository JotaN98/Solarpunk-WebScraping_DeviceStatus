from requests import get
import datetime_convert
from .. import telegram_bot


#------------KADOA API AI SCRAPIN--------------------------------
# This function gets the data scraped by a "workflow" in the Kadoa AI Web Scraping platform
# KADOA_WORKFLOW_ID: the function needs to receive the id of the specific workflow
# KADOA_API_KEY: needs to be accessible token file

def kadoa(id, location, web_url,KADOA_WORKFLOW_ID):


    # get Kadoa API key
    with open("../tokens.gitignore") as f:
        text = f.readlines()
        KADOA_API_KEY = text[2].strip()

    url = f"https://api.kadoa.com/v4/workflows/{KADOA_WORKFLOW_ID}/data"
    headers = {
        "x-api-key": KADOA_API_KEY
    }
    try:
        response = get(url, headers=headers)
        if response.status_code == 200:
            print("✅ KadoaAPI data retrieved successfully.\n")
            data = response.json()['data'][0]
            message = f"Data retrieved on: {datetime_convert.date_convert(response.json()['executedAt'])}\n"

            if "ago" in data['ONLINE']:
                message += f"⚠️\nDevice: {data['ID']} appears to be offline!\nLocation: {location.upper()}\n Last online: {data['ONLINE']}\n Check the link: {web_url} "
            else:
                message += f"✅\nDevice: {data['ID']}\nLocation: {location.upper()}\nOnline days: {data['ONLINE']}"
        else:
            message = f"❌ Failed to retrieve KadoaAPI data. Status Code: {response.status_code}\n"
            message += f"Response: {response.text}"

        telegram_bot.send_message(message)

    except Exception as e:
        message = f"❌ Exception occurred while retrieving Kadoa workflow data: {e}"
        telegram_bot.send_message(message)

