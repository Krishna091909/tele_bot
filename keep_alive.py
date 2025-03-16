import requests
import asyncio

# Your Render/Flask URL
FLASK_URL = "https://tele-bot-t5yd.onrender.com"

async def keep_alive():
    while True:
        try:
            requests.get(FLASK_URL)
            print("Keep-alive ping sent!")
        except Exception as e:
            print(f"Failed to ping: {e}")
        await asyncio.sleep(600)  # Ping every 10 minutes

if __name__ == "__main__":
    asyncio.run(keep_alive())
