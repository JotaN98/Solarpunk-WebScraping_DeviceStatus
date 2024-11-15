from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time, log_keeper


#finds the line that contains 'online' text
def find_online_line(text):
    for line in text.splitlines():
        if "online" in line.lower():
            return line

#--------------SELENIUM CHROME DRIVER SCRAPIN--------------------------------

def selenium_geodnet(id,location,url,wait,driver_manager):

    # Initialize Chrome WebDriver using webdriver-manager
    options = webdriver.ChromeOptions()

    # Optional: Run Chrome in headless mode (without GUI)
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')  # Required in some Linux environments
    options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
    options.add_argument('--disable-gpu')  # Disable GPU hardware acceleration (useful for Linux)
    options.add_argument('--disable-software-rasterizer')  # Ensures no GPU processing is done
    options.add_argument("--enable-logging")
    options.add_argument("--v=1")

    try:
        # Initialize the Chrome driver
        service = ChromeService(driver_manager)
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        print(f"{e}")
        exit()

    try:
        # Navigate to the URL
        print(f"🔍 Loading URL: {url}")
        driver.get(url)

        # Wait for {wait} seconds to allow the page to load completely
        print(f"⏳ Waiting for {wait} seconds to allow the page to load...")
        time.sleep(wait)

        # Attempt to find the DIV element with class "leaflet-popup-content-wrapper"
        try:
            print(f"PAGE SOURCE {driver.page_source}")

            popup_div = driver.find_element(By.CLASS_NAME, "leaflet-popup-content-wrapper")
            print("✅ Successfully found the DIV 'leaflet-popup-content-wrapper'.")
        except Exception as e:
            error_message = f"Error: Could not find the 'leaflet-popup-content-wrapper' on {url} | {e}"
            print(f"❌ {error_message}")
            #records in the log if the DIV was not found
            log_keeper.write_log(error_message.splitlines()[0])
            return  # Exit the function if the DIV is not found

        # Retrieve the text content of the DIV
        div_text = popup_div.text
        print(f"📝 Content of 'leaflet-popup-pane' DIV:\n{div_text}")

        # Check if the text "ago" exists within the DIV's text (i.e. 'Last online 1 hour ago')
        if "ago" in div_text:
            result_message = f"Warning! | Device: {id} appears to be offline! | Location: {location.upper()} | {find_online_line(div_text)} | Check the link: {url}"
            print(f"⚠️ {result_message}")
            log_keeper.write_log(result_message)
        else:
            result_message = f"Device: {id} | Location: {location.upper()} | {find_online_line(div_text)}."
            print(f"✅ {result_message}")
            log_keeper.write_log(result_message)
    except Exception as e:
        print(f"{e}")
    finally:
        # Close the browser after the operations
        try:
            print("🔒 Closing the browser.")
            driver.quit()
        except Exception as e:
            print(f"{e}")
