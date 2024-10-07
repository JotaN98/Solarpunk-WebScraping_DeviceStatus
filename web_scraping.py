from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time, telegram_bot


def geodnet(url):
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
            error_message = f"❌ Error: Could not find the DIV with class 'leaflet-popup-pane'. Exception: {e}"
            print(error_message)
            telegram_bot.send_message(error_message)
            return  # Exit the function if the DIV is not found

        # Retrieve the text content of the DIV
        div_text = popup_div.text
        print(f"📝 Content of 'leaflet-popup-pane' DIV:\n{div_text}")

        # Check if the text "Online:" exists within the DIV's text
        if "Online:" in div_text:
            result_message = "✅ Result: The text 'Online:' was FOUND within the DIV."
            print(result_message)
            telegram_bot.send_message(result_message)
        else:
            result_message = "⚠️ Result: The text 'Online:' was NOT FOUND within the DIV."
            print(result_message)
            telegram_bot.send_message(result_message)

    finally:
        # Close the browser after the operations
        print("🔒 Closing the browser.")
        driver.quit()

