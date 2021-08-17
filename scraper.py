from playwright.sync_api import sync_playwright
import time


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.facebook.com/marketplace")
    time.sleep(100)
    print(page.title())
    browser.close()