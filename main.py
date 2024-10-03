from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Setup webdriver
options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Navigate to the URL
driver.get("https://console.geodnet.com/map?mount=A0EE9")

# Wait for the page to load fully
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
print("Page loaded successfully!")

# Relative XPaths for the blue dot
blue_dot_xpath_options = [
    "/html/body/div[3]/div[5]/div/div[2]/div[1]/div[4]/div[81]/div",
    "/html/body/div[3]/div[5]/div/div[2]/div[1]/div[4]/div[82]/div"
]

blue_dot = None

# Loop through possible XPaths to find the blue dot
for xpath in blue_dot_xpath_options:
    try:
        blue_dot = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
        print(f"Blue dot found using XPath: {xpath}")
        break
    except Exception as e:
        print(f"Couldn't find blue dot using XPath: {xpath} - {e}")

if not blue_dot:
    print("Failed to locate the blue dot.")
    driver.quit()
    exit()

# Scroll into view and click the blue dot using JavaScript
driver.execute_script("arguments[0].scrollIntoView(true);", blue_dot)
driver.execute_script("arguments[0].click();", blue_dot)
print("Clicked on the blue dot!")

# Wait for the side panel to load
side_panel_xpath = "/html/body/div[3]/div[5]/div/aside"
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, side_panel_xpath)))
print("Side panel loaded successfully!")

# Now attempt to find the "last data packet date" with scrolling
data_field_xpath = '//*[@id="__blaze-root"]/div[5]/div/aside/div[7]/div[2]/div/div/div[2]/div/div[2]'
#//*[@id="__blaze-root"]/div[5]/div/aside/div[7]/div[2]/div/div/div[2]/div')
#'//*[@id="__blaze-root"]/div[5]/div/aside/div[7]/div[2]/div/div/div[2]/div/div[1]')

# Attempt to scroll and find the element
for attempt in range(10):  # Try scrolling down 10 times
    try:
        # Attempt to locate the data field using XPath
        data_field = WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.XPATH, data_field_xpath)))
        last_packet_date = data_field.text
        print(f"Last Data Packet Date: {last_packet_date}")
        break
    except Exception as e:
        print(f"Data field not found yet. Attempt {attempt + 1}: {e}")
        # Scroll down the side panel
        driver.execute_script("document.querySelector('aside').scrollTop += 300;")  # Adjust scroll amount as needed
        time.sleep(1)  # Wait a moment for the scroll to take effect

# If the element is still not found, print the page source for debugging
if 'last data packet date' not in driver.page_source.lower():
    print("Last data packet date not found in the page source.")
  #  print(driver.page_source)  # Print the entire page source for debugging

# Close the browser
driver.quit()
