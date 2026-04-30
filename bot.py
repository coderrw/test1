from flask import Flask
import threading
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

app = Flask(__name__)

@app.route('/')
@app.route('/health')
def health():
    return "Bot is alive!", 200

def run_webserver():
    app.run(host='0.0.0.0', port=8080)

# ========== TEST ACCOUNT CREDENTIALS ==========
EMAIL = "famryan1@outlook.com"
PASSWORD = "google@1"

def login_to_microsoft(driver):
    print("🔐 Logging into Microsoft...")
    
    driver.get("https://rewards.microsoft.com")
    time.sleep(3)
    
    if "points" in driver.page_source.lower():
        print("✅ Already logged in!")
        return True
    
    driver.get("https://login.live.com")
    time.sleep(3)
    
    try:
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "loginfmt"))
        )
        email_input.send_keys(EMAIL)
        driver.find_element(By.ID, "idSIButton9").click()
        time.sleep(3)
        
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "passwd"))
        )
        password_input.send_keys(PASSWORD)
        driver.find_element(By.ID, "idSIButton9").click()
        time.sleep(5)
        
        print("✅ Login successful!")
        return True
        
    except Exception as e:
        print(f"❌ Login failed: {e}")
        return False

def run_bot():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0')
    options.binary_location = "/usr/bin/chromium"
    
    driver = webdriver.Chrome(options=options)
    
    if not login_to_microsoft(driver):
        print("⚠️ Login failed - continuing without login")
    
    searches = ["cats", "dogs", "weather", "news", "sports", "movies"]
    count = 0
    
    print("🤖 Bot started! Searching Bing...")
    
    while True:
        for term in searches:
            count += 1
            print(f"🔍 Search #{count}: {term}")
            try:
                driver.get(f"https://www.bing.com/search?q={term}")
                time.sleep(2)
                print(f"✅ Searched: {term}")
            except Exception as e:
                print(f"❌ Error: {e}")
            time.sleep(100)

if __name__ == "__main__":
    threading.Thread(target=run_webserver, daemon=True).start()
    run_bot()
