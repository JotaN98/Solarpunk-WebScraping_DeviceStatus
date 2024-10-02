from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup Selenium with Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run headless, without opening a browser window

# Create a new instance of the Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Open the web page
driver.get('https://console.geodnet.com/map?mount=A0EE9')

# Wait for the page to load and JavaScript to render
driver.implicitly_wait(10)  # You can adjust the wait time depending on how long the page takes to load

# Use the full XPath to find the target element
element = driver.find_element(By.XPATH, '/html/body/div[3]/div[5]/div/aside/div[7]/div[2]/div/div/div[2]/div/div[1]')

# Get the text content of the element
content = element.text
print("Scraped content:", content)

# Close the browser
driver.quit()
