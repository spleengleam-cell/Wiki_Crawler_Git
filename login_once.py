from playwright.sync_api import sync_playwright
import os
import time

EDGE_USER_DATA_DIR = r"C:\WikiProfile"
AUTH_FILE = "auth.json"
LOGIN_URL = "https://sites.google.com/view/kopievonfitreisengroupwiki/fit-group-wiki?authuser=0"

os.makedirs(EDGE_USER_DATA_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch_persistent_context(
        user_data_dir=EDGE_USER_DATA_DIR,
        channel="msedge",
        headless=False,   # Must be false to log in manually
        args=["--disable-blink-features=AutomationControlled"]
    )

    page = browser.new_page()
    print("➡ Opening wiki login page...")
    page.goto(LOGIN_URL)

    print("\n=================================================")
    print("PLEASE LOG IN MANUALLY IN THE EDGE WINDOW")
    print("DO NOT CLOSE THIS TERMINAL — I AM WATCHING FOR LOGIN")
    print("=================================================\n")

    # Wait until the wiki domain is loaded (login complete)
    while True:
        current_url = page.url
        print(f"🔄 Current URL: {current_url}")
        if "sites.google.com/view/kopievonfitreisengroupwiki" in current_url:
            break
        time.sleep(2)

    print("✅ Login detected! Saving session...")
    browser.storage_state(path=AUTH_FILE)
    print(f"✅ Saved auth session to {AUTH_FILE}")

    browser.close()
    print("\n🎉 Login complete. You can now run scrape_wiki.py")
