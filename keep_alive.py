import requests
import time

# Your Render/Flask URL
FLASK_URL = "https://your-app.onrender.com/"

while True:
    try:
        requests.get(FLASK_URL)
        print("Keep-alive ping sent!")
    except Exception as e:
        print(f"Failed to ping: {e}")
    time.sleep(600)  # Ping every 10 minutes
