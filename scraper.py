import time
from playwright.sync_api import StorageState, sync_playwright
from datetime import datetime
import random

class Scraper:
    def __init__(self,browser,url="",distance='100km'):
        self.url = url
        self.filter_selector = '//*[@id="seo_filters"]/div/div[1]/div/span'
        self.location_selector= "//input[@aria-label='Enter a town or city']"
        self.location_selector_sub= "//div[@role='option']"
        self.distance_selector = "//div/span[contains(text(),'60 kilometres')]"
        self.select_vehciles = "//span[contains(text(),'Vehicles')]"
        self.distatnce_map = {
            "1km":1,
            "2km":2,
            "5km":3,
            "10km":4,
            "20km":5,
            "40km":6,
            "60km":7,
            "80km":8,
            "100km":9,
            "250km":10,
            "500km":11
        }
        self.distance = distance
        self.distance_selector_sub = f"//div/div[1]/div/div[4]/div/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div[{self.distatnce_map.get(self.distance)}]"
        self.apply_btn = "//span[contains(text(),'Apply')]"
        self.short = "//span[contains(text(),'Sort by')]"
        self.dateListed = "//span[contains(text(),'Date listed: Newest first')]"
        self.banner = '//div/i[@aria-label="Facebook Marketplace. Buy or sell cars, motorcycles, boats, motor homes, caravans and other vehicles."]'
        self.browser = browser
        self.page = self.browser.new_page()
        self.page.set_default_timeout(240000)
        self.page.set_default_timeout(240000)
            # self.page.goto("https://www.facebook.com/marketplace")
            # time.sleep(100)
            # print(page.title())
            # browser.close()

    def fetchnew(self,filename='',element_list =  []):
        file_names = []
        if filename in file_names:
            return element_list
        else:
            # arrow down
            self.page.keyboard.press("PageDown")
            self.page.wait_for_load_state("networkidle");
            self.page.keyboard.press("PageDown")
            self.page.wait_for_load_state("networkidle");
            self.page.keyboard.press("PageDown")
            self.page.wait_for_load_state("networkidle");
            self.page.keyboard.press("PageDown")
            self.page.wait_for_load_state("networkidle");
            time.sleep(random.uniform(0, 3)
)
            # fetch itmes again
            elements = self.page.query_selector_all('//*/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[6]/div/div/div')
            # compare list then append
            len_elments = len(elements)
            root_elments = len(element_list)
            # take to elment list
            if root_elments < len_elments:
                element_list.append(elements[root_elments-1:len_elments])
            # call fetchnew
            self.fetchnew(filename,element_list)

    def scrape_newest(self):
        self.page.wait_for_load_state()
        self.page.goto(self.url,wait_until="networkidle")
        # self.page.click(self.select_vehciles,force=True)
        # self.page.wait_for_load_state("networkidle");
        # time.sleep(4)
        self.page.click(self.filter_selector)
        self.page.wait_for_load_state("networkidle");
        # self.page.wait_for_selector(self.location_selector)
        # self.page.click(self.location_selector)
        # self.page.keyboard.type("Sydney", delay=500)
        # self.page.wait_for_load_state()
        # self.page.click(self.location_selector)
        # self.page.wait_for_load_state()
        # self.page.click(self.location_selector_sub)
        # self.page.wait_for_load_state()
        self.page.click(self.distance_selector,force=True)
        self.page.wait_for_load_state()
        self.page.click(self.distance_selector_sub,force=True)
        self.page.wait_for_load_state()
        self.page.click(self.apply_btn,force=True)
        self.page.wait_for_load_state("networkidle");
        # self.page.click("text=Sort by")
        # self.page.wait_for_load_state("networkidle");
        # self.page.click(self.dateListed)
        # self.page.wait_for_load_state("networkidle");
        # self.page.click(self.short,force=True)
        # self.page.wait_for_load_state("networkidle");
        self.page.click(self.banner)
        self.page.wait_for_load_state("networkidle");
        """
        fetch mongo db :
            if last update one is from yesterday:
                 reset database
            there is no data:
                fill scraped data in last 2 hours
            else
                get last updated item filename from mongodb
                scroll till find that filename
                update the firestore/mongodb
                    image-filename
                    last-updated
                    content
        """
        self.page.keyboard.press("PageDown")
        self.page.wait_for_load_state("networkidle");
        self.page.keyboard.press("PageDown")
        self.page.wait_for_load_state("networkidle");
        self.page.keyboard.press("PageDown")
        self.page.wait_for_load_state("networkidle");
        self.page.keyboard.press("PageDown")
        self.page.wait_for_load_state("networkidle");
        self.page.keyboard.press("PageDown")
        self.page.wait_for_load_state("networkidle");
        self.page.keyboard.press("PageDown")
        self.page.wait_for_load_state("networkidle");
        self.page.keyboard.press("PageDown")
        self.page.wait_for_load_state("networkidle");
        self.page.keyboard.press("PageDown")
        self.page.wait_for_load_state("networkidle");
        self.page.keyboard.press("PageDown")
        self.page.wait_for_load_state("networkidle");
        self.page.keyboard.press("PageDown")
        self.page.wait_for_load_state("networkidle");
        self.page.keyboard.press("PageDown")
        elements = self.page.query_selector_all('//*/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[6]/div/div/div')
        print(f"len is {len(elements)}")
        print(elements[31].inner_html())
        for i,element in enumerate(elements):
            # link = element.query_selector('//div/span/div/div/a').get_attribute('href')
            print(element.inner_html())
            if element.inner_html() != '<div></div>':
                print('yes')
                element.click()
                # self.page.goto("https://www.facebook.com"+link,wait_until="networkidle")
                self.page.wait_for_load_state("networkidle");
                self.page.wait_for_selector("//span[contains(text(),'Listed')]")
                listed_time = self.page.inner_text("//span[contains(text(),'Listed')]")
                print(f"------------------------------{i}-----item")
                print(listed_time)
                self.page.click('//*/div/div[1]/div/div[2]/div/div[1]/div/div[1]/div/i')
                # self.page.wait_for_load_state("networkidle");
                print(element)
                tex = element.inner_text()
                print(tex)
            else:
                print("no")
        print(f"len is {len(elements)}")

    def close_connection(self):
        self.page.close()
        self.browser.close()

start = time.time()
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    sc = Scraper(browser=browser,url='https://www.facebook.com/marketplace/melbourne/vehicles?sortBy=creation_time_descend&exact=false')
    sc.scrape_newest()
    sc.close_connection()
end = time.time()
print(end - start)