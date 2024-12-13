import time, log_keeper
from playwright.sync_api import sync_playwright


# ------------------- Playwright Web Scraping Function ------------------- #
def playwright_geodnet(id, location, url, wait):
    with sync_playwright() as p:
        try:
            # Launch a headless browser
            browser = p.webkit.launch(headless=True)
            page = browser.new_page()

            # Navigate to the URL
            print(f"🔍 Loading URL: {url}")
            page.goto(url)

            # Wait for the specified element to appear on the page
            print(f"⏳ Waiting for {wait} seconds to allow the page to load...")
            page.wait_for_selector(".leaflet-popup-content-wrapper", timeout=wait * 1000)

            try:
                # Attempt to find the DIV element with class "leaflet-popup-content-wrapper"
                popup_div = page.query_selector(".leaflet-popup-content-wrapper")
                if popup_div:
                    print("✅ Successfully found the DIV 'leaflet-popup-content-wrapper'.")
                    div_text = popup_div.inner_text()

                    print(f"📝 Content of 'leaflet-popup-content-wrapper' DIV:\n{div_text}")

                    # Check if the text "ago" exists within the DIV's text (e.g., 'Last online 1 hour ago')
                    if "ago" in div_text.lower():
                        result_message = (
                            f"Warning! | Device: {id} appears to be offline! | "
                            f"Location: {location.upper()} | {find_online_line(div_text)} | Check the link: {url}"
                        )
                        print(f"⚠️ {result_message}")
                        log_keeper.write_log(result_message)
                    else:
                        result_message = (
                            f"Device: {id} | Location: {location.upper()} | {find_online_line(div_text)}."
                        )
                        print(f"✅ {result_message}")
                        log_keeper.write_log(result_message)
                else:
                    raise Exception("DIV element not found.")

            except Exception as e:
                error_message = f"Error: Could not find the 'leaflet-popup-content-wrapper' on {url} | {e}"
                print(f"❌ {error_message}")
                # Records in the log if the DIV was not found
                log_keeper.write_log(error_message.splitlines()[0])

        except Exception as e:
            print(f"❌ An error occurred: {e}")

        finally:
            # Close the browser after the operations
            print("🔒 Closing the browser.")
            browser.close()

#finds the line that contains 'online' text
def find_online_line(text):
    for line in text.splitlines():
        if "online" in line.lower():
            return line