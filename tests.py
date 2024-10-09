import asyncio, time
from playwright.async_api import async_playwright


async def scrape_map_popup():
    # Launch Playwright in headless mode
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Go to the target URL
        await page.goto('https://console.geodnet.com/map?mount=A0EE9', wait_until='networkidle', timeout=120000)
        time.sleep(120)
        # Wait for the map and leaflet panel to load by waiting for the leaflet-popup-pane div to appear
        try:
            # Wait for the element with class 'leaflet-popup-pane' to load (up to 60 seconds)
            print("Waiting for the popup to appear...")
            await page.wait_for_selector('leaflet-popup-content', state='visible', timeout=60000)
            print("Popup found and visible.")
            # Scrape the text inside the 'leaflet-popup-pane' div
            popup_content = await page.inner_text('div.leaflet-popup-pane')

            print("Scraped Text from the Popup:")
            print(popup_content)

        except Exception as e:
            print(f"An error occurred: {e}")

        # Close the browser
        await browser.close()


# Run the async function
asyncio.run(scrape_map_popup())
