import time
from playwright.sync_api import Cookie, StorageState, sync_playwright
import shutil
from datetime import datetime
import random
import os
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient
from random import randint
import  moongodb


client = MongoClient("mongodb+srv://admin:nCbtgwbAaUx3afAs@cluster0.ztfid.mongodb.net/FB?retryWrites=true&w=majority")
db = client.FB

class Scraper:
    def __init__(self,db,browser,url="",distance='250km'):
        self.db = db
        self.url = url
        self.filter_selector = '//*[@id="seo_filters"]/div/div[1]/div/span'
        self.location_selector= "//input[@aria-label='Enter a town or city']"
        self.location_selector_sub= "//div[@role='option']"
        self.distance_selector = "//div/span[contains(text(),'60 kilometres')]"
        self.select_vehciles = "//span[contains(text(),'Vehicles')]"
        self.index = 0
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
        self.banner = '//div[@id="seo_banner"]'
        self.browser = browser
        # self.browser.pages()[0].close()
        self.page = self.browser.new_page()
        # self.page.set_default_timeout(240000)
        self.page.set_default_timeout(240000)
  

    def fetchnew(self,filename,element_list =  []):
        file_names,count_,count_none = self.get_filenames(element_list)
        self.index = 0
        file_name = ''
        # print(file_names)
        if filename in file_names:
            # print("yes it in")
            file_name_list = []
            outputs_html = [ element.inner_html() for element in element_list]
            for element_html in outputs_html:

                if '<div></div>' not in element_html:
                    soup = BeautifulSoup(element_html ,"html.parser")
                    src = soup.find('img').attrs['src']
                    if re.match(r"^(data:image\/png)",src):
                        # print('outlier-loader')
                        pass
                    else:
                        file_name = src.split('_n.')[0].split('/')[-1]+'_n'
                        # print(f"file_name : {file_name}")
                    file_name_list.append(file_name)
                else:
                    file_name_list.append(file_name)
            self.index = file_name_list.index(filename)+1
            # print(f'index : {self.index}')
            # print(len(element_list))
            # print(type(element_list))
        else:
            # arrow down
            self.page.click(self.banner)
            self.page.wait_for_load_state("networkidle");
            for i in list(range(0,count_none)):
                self.page.keyboard.press("PageDown")
                self.page.wait_for_load_state("networkidle");
                time.sleep(random.uniform(0, 2))
                self.page.keyboard.press("PageDown")
                time.sleep(random.uniform(0, 2))
                self.page.wait_for_load_state("networkidle");
                time.sleep(random.uniform(0, 2))
                self.page.keyboard.press("PageDown")
                time.sleep(random.uniform(0, 2))
                self.page.wait_for_load_state("networkidle");
                time.sleep(random.uniform(0, 2))
                self.page.keyboard.press("PageDown")
                time.sleep(random.uniform(0, 2))
                self.page.wait_for_load_state("networkidle");
                time.sleep(random.uniform(0, 2))
            # fetch itmes again
            elements = self.page.query_selector_all('//*/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[6]/div/div/div')
            # compare list then append
            len_elments = len(elements)
            root_elments = count_
            # take to elment list
            if root_elments < len_elments:
                element_list.extend(elements[root_elments-1:len_elments])
            # call fetchnew
            self.fetchnew(filename,element_list)
        return element_list

    def fetech_db(self):
        # get last item
        file_name = ''
        cursor = db.vehicles.find_one()
        print(cursor.get('brand'))
        file = cursor.get('file_name')
        db.vehicles.delete_many({})
        return file
    
    # def feed_db(self):
        
    def get_filenames(self,elements_list):
        count_none = 0
        count_ = 0
        file_image_names = []
        for element in elements_list:

            # print(element.inner_html())
            if element.inner_html()== '<div></div>':
                count_none+=1
            else:
                img = element.inner_html()
                # print(img)
                soup = BeautifulSoup(img ,"html.parser")
                src = soup.find('img').attrs['src']
                # print(soup.find('img'))
                file_name_jpg = src.split('_n.')[0].split('/')[-1]+'_n'
                # file_name_png = src.split('.png')[0].split('/')[-1]
                if re.match(r"^(data:image\/png)",file_name_jpg):
                    # print('outlier-loader')
                    pass
                elif re.match(r"(\d+_)(\d+_)(\d+_n)", file_name_jpg):
                    # print('yes')
                    file_image_names.append(file_name_jpg)
                    count_+=1
        return file_image_names, count_,count_none

    def scrape_newest(self):
        self.page.wait_for_load_state()
        self.page.goto(self.url,wait_until="networkidle")
        self.page.click(self.filter_selector)
        self.page.wait_for_load_state("networkidle");
        self.page.click(self.distance_selector,force=True)
        self.page.wait_for_load_state()
        self.page.click(self.distance_selector_sub,force=True)
        self.page.wait_for_load_state()
        self.page.click(self.apply_btn,force=True)
        self.page.wait_for_load_state("networkidle");
        self.page.click(self.banner)
        self.page.wait_for_load_state("networkidle");
        """
        fetch mongo db :
            if last update one is from yesterday:
                 reset database
                 fill scraped data in last 2 hours
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
        time.sleep(random.uniform(0, 3))
        self.page.keyboard.press("PageDown")
        self.page.wait_for_load_state("networkidle");
        time.sleep(random.uniform(0, 3))
        elements_xlist = self.page.query_selector_all('//*/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div[6]/div/div/div')
        # file_ = '239554633_4643887242311324_4332611350569084027_n'
        file_ = self.fetech_db()
        elements_list= self.fetchnew(filename=file_,element_list=elements_xlist)
        outputs = elements_list[0:self.index]
        outputs_html = [ element.inner_html() for element in outputs]
        outputs_text = [element.inner_text() for element in outputs]
        self.fetch_data(outputs_html,outputs_text)


    def write_data(self,data):
        for x,data_point in enumerate(data):
            # print(data_point)
            result=db.vehicles.insert_one(data_point)
            #Step 4: Print to the console the ObjectID of the new document
    def close_connection(self):
        self.page.close()
        # self.browser.close()
    
    def fetch_data(self,outputs_html=[],outputs_text=[]):
        self.page.close()
        last_time = ''
        data = []
        for i,element in enumerate(outputs_html):
            # self.browser.clear_cookies()
            # self.browser.clear_permissions()
            # page.set_default_timeout(240000)
            # page.set_default_timeout(240000)
            # print(f'{i}')
            page = self.browser.new_page()
            page.set_default_timeout(240000)
            if '<div></div>' not in element:
        
                soup = BeautifulSoup(element ,"html.parser")
                src = soup.find('img').attrs['src']
                if re.match(r"^(data:image\/png)",src):
                    print('outlier-loader')
                    pass
                else:
                    link = 'https://www.facebook.com'+soup.find('a').attrs['href']
                    link = "/".join(link.split('/')[0:6])
                    # print(link)
                    file_name = src.split('_n.')[0].split('/')[-1]+'_n'
                    # print('--------------------------')
                    # print(f"src :{src}")
                    # print(f"file_name : {file_name}")
                    page.goto(link,wait_until="networkidle")
                    page.wait_for_load_state()
                    if 'unavailable_product' not in page.url:
                        price , brand , location, distance = None,None,None,None
                        try :
                            page.wait_for_selector("//span[contains(text(),'Listed')]")
                            listed_time = page.inner_text("//span[contains(text(),'Listed')]")
                            location_listed = page.inner_text("//span[contains(text(),'Listed')]/a/span")
                            subtract = listed_time.replace(location_listed,'')
                            time_listed = re.sub(r'^(Listed)|(\sin)', '', subtract)
                            last_time = time_listed
                            if len(outputs_text[i].split('\n'))==4:
                                price , brand , location, distance = outputs_text[i].split('\n')
                                data.append({
                                        'brand' : brand,
                                        'img_src': src,
                                        'file_name': file_name,
                                        'marketplace_link':link,
                                        'time' : last_time,
                                        'price': price,
                                        'location' : location ,
                                        'distance' : distance
                                    })
                            elif len(outputs_text[i].split('\n'))==3:
                                price , brand , location = outputs_text[i].split('\n')
                                data.append({
                                        'brand' : brand,
                                        'img_src': src,
                                        'file_name': file_name,
                                        'marketplace_link':link,
                                        'time' : last_time,
                                        'price': price,
                                        'location' : location ,
                                        'distance' : distance
                                    })
                                # print('-------------------------')
                                # print({
                                #         'brand' : brand,
                                #         'img_src': src,
                                #         'marketplace_link':link,
                                #         'time' : last_time,
                                #         'price': price,
                                #         'location' : location ,
                                #         'distance' : distance
                                #     })
                            # page.close()
                        except:
                            if len(outputs_text[i].split('\n'))==4:
                                price , brand , location, distance = outputs_text[i].split('\n')
                               
                                data.append({
                                        'brand' : brand,
                                        'img_src': src,
                                        'file_name':file_name,
                                        'marketplace_link':link,
                                        'time' : last_time,
                                        'price': price,
                                        'location' : location ,
                                        'distance' : distance
                                    })

                            elif len(outputs_text[i].split('\n'))==3:
                                price , brand , location = outputs_text[i].split('\n')
                                data.append({
                                        'brand' : brand,
                                        'img_src': src,
                                        'file_name': file_name,
                                        'marketplace_link':link,
                                        'time' : last_time,
                                        'price': price,
                                        'location' : location ,
                                        'distance' : distance
                                    })
                                # print('-------------------------')
                                # print({
                                #         'brand' : brand,
                                #         'img_src': src,
                                #         'marketplace_link':link,
                                #         'time' : last_time,
                                #         'price': price,
                                #         'location' : location ,
                                #         'distance' : distance
                                #     })
            else:
                # print("no")
                pass
            page.close()
        self.browser.close()
        # self.browser.close()
        print(data)
        self.write_data(data)



def browserRun(browser_dir={},choise=1):
    dir_path = ''
    browser = None
    with sync_playwright() as p:
        dir_path = browser_dir.get('chrome_dir')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        browser = p.chromium.launch_persistent_context(user_data_dir='./data',headless=True,permissions=['geolocation'],geolocation={'latitude':37.8136,"longitude":144.9631})
        # else:
        #     shutil.rmtree(f'./{dir_path}')
        # browser = p.webkit.launch_persistent_context(user_data_dir=f'{dir_path}',headless=False)
        # browser = p.webkit.launch(headless=False)
        # elif choise==2:
        #     dir_path = browser_dir.get('chrome_dir')
        #     if not os.path.exists(dir_path):
        #         os.makedirs(dir_path)
        #     # browser = p.webkit.launch(headless=False)
        #     # browser = p.webkit.launch_persistent_context(user_data_dir=f'{dir_path}',headless=False)
        #     # browser = p.firefox.launch(headless=False)
        # else:
        #     dir_path = browser_dir.get('chrome_dir')
        #     if not os.path.exists(dir_path):
        #         os.makedirs(dir_path)
        #     # browser = p.webkit.launch(headless=False)
        #     browser = p.webkit.launch_persistent_context(user_data_dir=f'{dir_path}',headless=False)
        #     # browser = p.webkit.launch(headless=False)
        sc = Scraper(browser=browser,url='https://www.facebook.com/marketplace/melbourne/vehicles?sortBy=creation_time_descend&exact=false',db=db)
        elements = sc.scrape_newest()

def main():
    start = time.time()
    browser_dir = {
    'firefox_dir' : "./data/firefox",
    'chrome_dir' : "./data/chrome",
    'webkit_dir' : "./data/webkit"
    }
    choise = random.randint(1,3)
    print(choise)
    browserRun(browser_dir=browser_dir,choise=choise)
    end = time.time()
    print(end - start)

main()
