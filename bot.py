from flask import Flask
import threading
import time
import requests

# ========== WEB SERVER FOR KEEP-ALIVE ==========
app = Flask(__name__)

@app.route('/')
@app.route('/health')
def health_check():
    return "Bot is alive!", 200

def run_webserver():
    app.run(host='0.0.0.0', port=8080)

# ========== YOUR BING SEARCH BOT ==========
def run_bot():
    searches = ["cats", "dogs", "weather", "news", "sports", "movies"]
    count = 0
    
    print("🤖 Bot started! Searching Bing...")
    
    while True:
        for term in searches:
            count += 1
            print(f"🔍 Search #{count}: {term}")
            try:
                response = requests.get(f"https://www.bing.com/search?q={term}")
                print(f"✅ Status: {response.status_code}")
            except Exception as e:
                print(f"❌ Error: {e}")
            time.sleep(100)  # 100 seconds between searches

# Start both in parallel
if __name__ == "__main__":
    # Start web server in background thread
    threading.Thread(target=run_webserver, daemon=True).start()
    # Start bot in main thread
    run_bot()