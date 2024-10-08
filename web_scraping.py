import telegram_bot


#------------KADOA API AI SCRAPIN--------------------------------

def kadoa(id, location, web_url,KADOA_WORKFLOW_ID):
    import requests, datetime_convert

    # get Kadoa API key
    with open("tokens.gitignore") as f:
        text = f.readlines()
        KADOA_API_KEY = text[2].strip()

    url = f"https://api.kadoa.com/v4/workflows/{KADOA_WORKFLOW_ID}/data"
    headers = {
        "x-api-key": KADOA_API_KEY
    }
    try:
        response = requests.get(url, headers=headers)
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


#--------------SELENIUM CHROME DRIVER SCRAPIN--------------------------------

def selenium_geodnet(id,location,url):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    import time

    # Initialize Chrome WebDriver using webdriver-manager
    options = webdriver.ChromeOptions()

    # Optional: Run Chrome in headless mode (without GUI)
    # Uncomment the following line to enable headless mode
    # options.add_argument('--headless')

    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    try:
        # Navigate to the URL
        print(f"🔍 Loading URL: {url}")
        driver.get(url)

        # Wait for 30 seconds to allow the page to load completely
        print("⏳ Waiting for 30 seconds to allow the page to load...")
        time.sleep(30)

        # Attempt to find the DIV element with class "leaflet-popup-pane"
        try:
            popup_div = driver.find_element(By.CLASS_NAME, "leaflet-popup-pane")
            print("✅ Successfully found the DIV with class 'leaflet-popup-pane'.")
        except Exception as e:
            error_message = f"⚠️ Error: Could not find the DIV with class 'leaflet-popup-pane' on {url}.\n Exception: {e}"
            print(error_message)
            telegram_bot.send_message(error_message)
            return  # Exit the function if the DIV is not found

        # Retrieve the text content of the DIV
        div_text = popup_div.text
        print(f"📝 Content of 'leaflet-popup-pane' DIV:\n{div_text}")

        # Check if the text "Online:" exists within the DIV's text
        if "Online:" in div_text:
            result_message = f"✅ Device:{id} in {location}: The text 'Online:' was FOUND within the DIV."
            print(result_message)
            telegram_bot.send_message(result_message)
        else:
            result_message = f"⚠️ Device:{id} in {location}: The text 'Online:' was NOT FOUND within the DIV. Check {url}"
            print(result_message)
            telegram_bot.send_message(result_message)

    finally:
        # Close the browser after the operations
        print("🔒 Closing the browser.")
        driver.quit()

