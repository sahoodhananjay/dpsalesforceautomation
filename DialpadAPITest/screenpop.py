
import pandas as pd
import numpy as np
from tqdm import tqdm
import requests
import re
from bs4 import BeautifulSoup
import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import warnings
warnings.filterwarnings("ignore")

class Screenpop:

    def __init__(self,url,client_id,redirect_uri,scope,authorization,client_secret):
        self.url = url
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.authorization = authorization
        self.client_secret = client_secret



    def check_print(self):
        print("test", 2*2)
        return (2*2)


    def get_access_code(self,expect):

        received_access_code = []
        api_url = self.url+"authorize?client_id="+self.client_id+"&redirect_uri="+self.redirect_uri+"&scope="+self.scope
        #print("API:", api_url)
        print("Auth:", self.authorization)
        header = {
                  'authority': 'dialpadbeta.com',
                  'User-Agent': 'PostmanRuntime/7.26.8',
                  'accept': 'application/json, text/javascript, */*; q=0.01',
                  'accept-language': 'en-US,en;q=0.9',
                  'authorization': self.authorization,
                  'referer': 'https://dialpadbeta.com/'
                 }
        r = requests.get(api_url, headers=header)
        soup = BeautifulSoup(r.content, 'html5lib')
        #print(soup)
        if expect:
            consents = soup.find("div", {"id": "consent_bottom_btns"})
            allow_access_url = consents.find("button", {"id": "consent_bottom_btns_allow"})
            pattern = re.compile(r"<button aria-pressed.*?code=(.*?)&")
            match = pattern.match(str(allow_access_url))
            if match:
                received_access_code.append(match.group(1))
                #print("Access Code Found",match.group(1))
            else:
                print('Access Code Not Found')

            return received_access_code
        else:
            consents = soup.find("div", {"class": "message"})
            return ((consents.text).strip())

    def get_api_key(self,received_access_code):
        received_api_key = []
        api_url = self.url + "token?client_id=" + self.client_id + "&client_secret=" + self.client_secret + "&code=" + received_access_code
        header = {
            'authority': 'dialpadbeta.com',
            'User-Agent': 'PostmanRuntime/7.26.8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.authorization,
            'referer': 'https://dialpadbeta.com/'
        }
        r = requests.post(api_url, headers=header)
        soup = BeautifulSoup(r.content, 'html5lib')

        content = soup.get_text()
        pattern = re.compile(r"\{\"access_token\"\: \"(.*?)\"")
        match = pattern.match(content)
        if match:
            received_api_key.append(match.group(1))
            #print("Api Key", match.group(1))
        else:
            print('API Key Not Found')

        return received_api_key

    def get_screenpop_url(self, user,type, received_api_key):
        url = 'https://dialpadbeta.com/api/v2/users/'
        #hardcoded_api_key = '6C58yhKUuHyMEDGeNXGMTUrw3b5RU269YJe9uYSr4RQbZq3fkPktztc3NQyy4QPryB7pTeFcdXnmSVgYdCqFNchXZSjgFCGh5gyb'
        #api_url = url + self.user + "/screenpop?apikey=" + hardcoded_api_key
        api_url = url + user + "/screenpop?apikey=" + received_api_key
        #print("API URL:",api_url)
        header = {
            'authority': 'dialpadbeta.com',
            'User-Agent': 'PostmanRuntime/7.26.8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.authorization,
            'referer': 'https://dialpadbeta.com/'
        }
        body = {"screen_pop_uri": "https://yahoo.com"}

        r = requests.post(api_url, data=json.dumps(body), headers=header)
        soup = BeautifulSoup(r.content, 'html5lib')
        content = soup.get_text()
        json_content = json.loads(soup.text)
        print(r.status_code)
        #print(content)

        received_response_code = r.status_code
        responsecode = re.search('200', str(r.status_code))
        receivedtype = re.search(type, content)
        if (responsecode and receivedtype):
            print("Test Passed. Received 200 Ok Response and Type as {}".format(type))
            return received_response_code
        else:
            #message = json_content['error']['message']
            print("Test failed with error {} and Type as {}".format(received_response_code,type))
            #print("Error Resposne:",message)
            return received_response_code

    def login_to_csr(self,admin_user,admin_pass):
        csr_driver = webdriver.Chrome('./chromedriver')
        csr_driver.get("https://dialpadbeta.com/csr/oauth_app/"+self.client_id)
        print(csr_driver.title)
        google_user = csr_driver.find_element_by_id("google-login-button").click()
        user_email = csr_driver.find_element_by_id("identifierId").send_keys(admin_user)
        next_button = csr_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(5)
        user_pass = csr_driver.find_element_by_class_name("whsOnd.zHQkBf").send_keys(admin_pass)
        time.sleep(5)
        next_button = csr_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(10)

        return


    def test1_check_for_screenpop_url(self, id, type, user, passw, responsecode, screen_pop_url,api_key):
        driver = webdriver.Chrome('./chromedriver')
        driver.get("https://dialpadbeta.com/app")
        print("Launched URL:", driver.title)
        google_user = driver.find_element_by_id("google-login-button").click()
        user_email = driver.find_element_by_id("identifierId").send_keys(user)
        next_button = driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(5)
        user_pass = driver.find_element_by_class_name("whsOnd.zHQkBf").send_keys(passw)
        time.sleep(5)
        next_button = driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(10)
        #received_access_code = get_access_code(url,client_id,redirect_uri,scope,authorization)
        time.sleep(5)
        # received_api_key = get_api_key(url,client_id,client_secret,received_access_code[0],authorization)
        time.sleep(5)

        screenpop_url_status = self.get_screenpop_url(id, type, api_key)
        time.sleep(20)

        if screenpop_url_status == int(responsecode):
            driver.switch_to.window(driver.window_handles[1])
            print("Current ScreenPOP URL: ", driver.current_url)
            open_url = driver.current_url
            is_screenpop_url_lunched = re.search(screen_pop_url, open_url)
            if is_screenpop_url_lunched:
                print("Screenpop url successfully started")
                return screenpop_url_status
        else:
            print("Screenpop url failed to start. Response: ", screenpop_url_status)
            return screenpop_url_status

        driver.quit()

    def test2_check_when_scope_not_enabled(self,admin_user,admin_pass):
        csr_driver = webdriver.Chrome('./chromedriver')
        csr_driver.get("https://dialpadbeta.com/csr/oauth_app/" + self.client_id)
        print(csr_driver.title)
        google_user = csr_driver.find_element_by_id("google-login-button").click()
        user_email = csr_driver.find_element_by_id("identifierId").send_keys(admin_user)
        next_button = csr_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(5)
        user_pass = csr_driver.find_element_by_class_name("whsOnd.zHQkBf").send_keys(admin_pass)
        time.sleep(5)
        next_button = csr_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(10)
        scope_button = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/div[3]/label[5]/input").get_property("checked")
        if scope_button:
            print("The screen_pop Scope is enabled. Lets disable it.")
            disable_scope_button = csr_driver.find_element_by_xpath(
                "//*[@id=\"csr-main\"]/div[5]/form/div[3]/label[5]/input").click()
            time.sleep(5)
            save_button = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/input[1]").click()
            time.sleep(5)
            accessmessage = self.get_access_code(False)
            print("Scope was already enabled:",accessmessage)
            scope_button = csr_driver.find_element_by_xpath(
                "//*[@id=\"csr-main\"]/div[5]/form/div[3]/label[5]/input").click()
            save_button = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/input[1]").click()
            time.sleep(5)
            csr_driver.quit()
            return accessmessage
        else:
            print("The screen_pop Scope is already disabled")
            accessmessage = self.get_access_code(False)
            scope_button = csr_driver.find_element_by_xpath(
                "//*[@id=\"csr-main\"]/div[5]/form/div[3]/label[5]/input").click()
            print("Scope was already disabled:",accessmessage)
            save_button = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/input[1]").click()
            csr_driver.quit()
            return accessmessage

    def test3_check_talk_license_enabled(self,admin_user,admin_pass):
        csr_driver = webdriver.Chrome('./chromedriver')
        csr_driver.get("https://dialpadbeta.com/csr/oauth_app/" + self.client_id)
        print(csr_driver.title)
        google_user = csr_driver.find_element_by_id("google-login-button").click()
        user_email = csr_driver.find_element_by_id("identifierId").send_keys(admin_user)
        next_button = csr_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(5)
        user_pass = csr_driver.find_element_by_class_name("whsOnd.zHQkBf").send_keys(admin_pass)
        time.sleep(5)
        next_button = csr_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(10)
        license_button_lite = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/div[5]/label[1]/input").get_property("checked")
        license_button_talk = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/div[5]/label[2]/input").get_property("checked")
        license_button_sell = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/div[5]/label[3]/input").get_property("checked")
        license_button_support = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/div[5]/label[4]/input").get_property("checked")

        print("Enable License only for Talk Users")

        if license_button_lite:
            license_bttns_lite = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/div[5]/label[1]/input").click()
        if license_button_sell:
            license_bttns_sell = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/div[5]/label[3]/input").click()
        if license_button_support:
            license_bttns_support = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/div[5]/label[4]/input").click()

        save_button = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/input[1]").click()
        time.sleep(5)

        if license_button_talk:
            accessmessage = self.get_access_code(False)
            print("Talk license already enabled:", accessmessage)
            license_bttns_talk = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/div[5]/label[2]/input").click()
            save_button = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/input[1]").click()
            time.sleep(5)
            csr_driver.quit()
            return accessmessage
        else:
            license_bttns_talk = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/div[5]/label[2]/input").click()
            save_button = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/input[1]").click()
            time.sleep(5)
            accessmessage = self.get_access_code(False)
            print("Talk license already disabled:", accessmessage)
            license_bttns_talk = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/div[5]/label[2]/input").click()
            save_button = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/input[1]").click()
            time.sleep(5)
            csr_driver.quit()
            return accessmessage

    def test4_check_redirectserver_not_enabled(self,admin_user,admin_pass):
        csr_driver = webdriver.Chrome('./chromedriver')
        csr_driver.get("https://dialpadbeta.com/csr/oauth_app/" + self.client_id)
        print(csr_driver.title)
        google_user = csr_driver.find_element_by_id("google-login-button").click()
        user_email = csr_driver.find_element_by_id("identifierId").send_keys(admin_user)
        next_button = csr_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(5)
        user_pass = csr_driver.find_element_by_class_name("whsOnd.zHQkBf").send_keys(admin_pass)
        time.sleep(5)
        next_button = csr_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(10)
        redirectserver_btns = csr_driver.find_element_by_xpath("//*[@id=\"redirect_uris\"]").clear()
        save_button = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/input[1]").click()
        time.sleep(5)
        accessmessage = self.get_access_code(False)
        print("No redirect server url configured:", accessmessage)
        redirectserver_btns = csr_driver.find_element_by_xpath("//*[@id=\"redirect_uris\"]").send_keys(self.redirect_uri)
        save_button = csr_driver.find_element_by_xpath("//*[@id=\"csr-main\"]/div[5]/form/input[1]").click()
        time.sleep(5)
        csr_driver.quit()
        return accessmessage

    def test5_check_for_screenpop_url_with_cti(self, id, type, user, passw, responsecode, screen_pop_url,api_key,salesforce,salesforce_user,salesforce_pass):
        driver = webdriver.Chrome('./chromedriver')
        driver.get(salesforce)
        print("Launched URL:", driver.title)
        time.sleep(10)
        #zendeskLogin = driver.find_element_by_xpath("//*[@id=\"username\"]").send_keys(salesforce_user)
        #zendeskPass = driver.find_element_by_xpath("//*[@id=\"password\"]").send_keys(salesforce_pass)
        #zendeskSignin = driver.find_element_by_xpath("//*[@id=\"Login\"]").click()
        #time.sleep(45)
        #size = driver.find_element_by_tag_name("iframe")
        #print("Num of iFrames:",size)
        #cti = driver.switch_to.frame(driver.find_element_by_css_selector("iframe[title=\"Dialpad Lightining\"]"))
        #cti = driver.find_element_by_xpath("/html/body/div[5]/div[1]/section/div[2]/div[1]/div[4]/ul/li/div/div/button/span").click()
        #time.sleep(5)
        salesorce_cti = driver.find_element_by_xpath("//*[@id=\"su-google-connect\"]/div").click()
        time.sleep(10)
        driver.switch_to.window(driver.window_handles[1])
        user_email = driver.find_element_by_xpath("//*[@id=\"identifierId\"]").send_keys(user)
        next_button = driver.find_element_by_xpath("//*[@id=\"identifierNext\"]/div/button/div[2]").click()
        time.sleep(5)
        user_pass = driver.find_element_by_xpath("//*[@id=\"password\"]/div[1]/div/div[1]/input").send_keys(passw)
        time.sleep(5)
        next_button = driver.find_element_by_xpath("//*[@id=\"passwordNext\"]/div/button/div[2]").click()
        time.sleep(10)
        #received_access_code = get_access_code(url,client_id,redirect_uri,scope,authorization)
        time.sleep(5)
        # received_api_key = get_api_key(url,client_id,client_secret,received_access_code[0],authorization)
        time.sleep(5)

        screenpop_url_status = self.get_screenpop_url(id, type, api_key)
        time.sleep(20)

        if screenpop_url_status == int(responsecode):
            driver.switch_to.window(driver.window_handles[1])
            print("Current ScreenPOP URL: ", driver.current_url)
            open_url = driver.current_url
            is_screenpop_url_lunched = re.search(screen_pop_url, open_url)
            if is_screenpop_url_lunched:
                print("Screenpop url successfully started")
                return screenpop_url_status
        else:
            print("Screenpop url failed to start. Response: ", screenpop_url_status)
            return screenpop_url_status

        driver.quit()

    def test6_check_for_screenpop_url_as_admin_for_nonadmin(self,non_admin_user_id,type,api_key):
        screenpop_url_status = self.get_screenpop_url(non_admin_user_id,type, api_key)
        print("Received Response:")
        print(screenpop_url_status)
        return screenpop_url_status

    def test7_check_for_screenpop_url_as_nonadmin(self,non_admin_user_id,type):
        access_code = self.get_access_code(True)
        print("Non Admin Access Code:", access_code[0])
        api_key = self.get_api_key(access_code[0])
        print("Non Admin API Key:", api_key[0])
        screenpop_url_status = self.get_screenpop_url(non_admin_user_id, type, api_key[0])
        return screenpop_url_status

    def test8_check_for_screenpop_url_as_nonadmin_for_admin(self, user,type):
        access_code = self.get_access_code(True)
        print("Non Admin Access Code:",access_code[0])
        api_key = self.get_api_key(access_code[0])
        print("Non Admin API Key:", api_key[0])
        screenpop_url_status = self.get_screenpop_url(user, type, api_key[0])
        return screenpop_url_status








