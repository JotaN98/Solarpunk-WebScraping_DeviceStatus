import requests
import websocket
import json
from bs4 import BeautifulSoup

# WebSocket handshake URL
ws_url = "https://console.geodnet.com/sockjs/info?t=1728033839262"
xhr_url = "https://console.geodnet.com/sockjs/259/m51l1etw/xhr_send?t=1728033576301"

#https://console.geodnet.com/sockjs/info?t=1728033839262
# Function to establish WebSocket connection
def on_message(ws, message):
    print("Received message: ", message)


def on_error(ws, error):
    print("Error: ", error)


def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed with message:", close_msg)


def on_open(ws):
    print("WebSocket connection opened")


# Function to scrape dynamically loaded sidebar
def scrape_sidebar():
    # Set headers to replicate the XHR request
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-US,en;q=0.9,pt;q=0.8,pt-PT;q=0.7,es;q=0.6",
        "content-type": "text/plain",
        "origin": "https://console.geodnet.com",
        "referer": "https://console.geodnet.com/map?mount=A0EE9",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        "cookie": "__hstc=63041136.8d10ed25a1dfbe5074fafc33708371e9.1727881955528.1727881955528.1727881955528.1; hubspotutk=8d10ed25a1dfbe5074fafc33708371e9; __hssrc=1; x_mtok=jY28EDN86C8SfjwMq"
    }

    # Data payload to simulate the XHR POST request
    payload = json.dumps(["YOUR_PAYLOAD_DATA_HERE"])

    # Send XHR POST request
    response = requests.post(xhr_url, headers=headers, data=payload)

    if response.status_code == 200:
        print("XHR request successful")
        # Parse the dynamically loaded sidebar content
        parse_sidebar(response.text)
    else:
        print(f"XHR request failed with status code {response.status_code}")


# Function to parse the sidebar content
def parse_sidebar(html_content):
    # Use BeautifulSoup to parse the HTML or JSON response
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the sidebar element with the class "ww_map_sidebar"
    sidebar = soup.find("div", class_="ww_map_sidebar")

    if sidebar:
        print("Sidebar content:")
        print(sidebar.prettify())
    else:
        print("Sidebar not found in the response")


# Main function to run the script
def main():
    # Establish WebSocket connection
    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

    # Perform the XHR request to load sidebar content
    scrape_sidebar()


if __name__ == "__main__":
    main()
