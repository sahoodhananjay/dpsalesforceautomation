import pandas as pd
import numpy as np
from selenium.webdriver.common.by import By
from tqdm import tqdm
import requests
import re
from bs4 import BeautifulSoup
import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import warnings
warnings.filterwarnings("ignore")



class XSS_Frontend:

    def __init__(self,url,admin_id,authorization,contact_id):
        self.url = url
        self.admin_id = admin_id
        self.authorization = authorization
        self.contact_id = contact_id

    def native_app_login(self,admin_user,admin_pass,xss_list):

        nativeapp_driver = webdriver.Chrome('./chromedriver')
        nativeapp_driver.get(self.url)
        print(nativeapp_driver.title)
        google_user = nativeapp_driver.find_element_by_id("google-login-button").click()
        user_email = nativeapp_driver.find_element_by_id("identifierId").send_keys(admin_user)
        next_button = nativeapp_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(5)
        user_pass = nativeapp_driver.find_element_by_class_name("whsOnd.zHQkBf").send_keys(admin_pass)
        time.sleep(5)
        next_button = nativeapp_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(10)

        return nativeapp_driver


    def xss_message(self,admin_user,admin_pass,xss_list,nativeapp_driver):
        print("Test Case1: XSS Attack via SMS")
        pass_flag = 0
        nativeapp_driver.refresh()
        nativeapp_driver = webdriver.Chrome('./chromedriver')
        nativeapp_driver.get(self.url)
        print(nativeapp_driver.title)
        google_user = nativeapp_driver.find_element_by_id("google-login-button").click()
        user_email = nativeapp_driver.find_element_by_id("identifierId").send_keys(admin_user)
        next_button = nativeapp_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(5)
        user_pass = nativeapp_driver.find_element_by_class_name("whsOnd.zHQkBf").send_keys(admin_pass)
        time.sleep(5)
        next_button = nativeapp_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(10)
        contact_button = nativeapp_driver.find_element_by_xpath("//*[@id=\"LeftbarSection__listContainerId3\"]/li[1]/a/p/span").click()
        time.sleep(5)

        counter = 1
        for i in xss_list:
            message_text = nativeapp_driver.find_element_by_xpath("//*[@id=\"message-text\"]").send_keys(i)
            message_send = nativeapp_driver.find_element_by_xpath("//*[@id=\"message-text\"]").send_keys(u'\ue007')

            try:
                WebDriverWait(nativeapp_driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="alert"]')))

                alert = nativeapp_driver.switch_to.alert
                alert.accept()
                time.sleep(10)
                alert = nativeapp_driver.find_element_by_id("alert")
                print("alert accepted", alert.text)
                status_code, json_content = self.check_for_message()
                message_data = json_content["description"]
                print("alert accepted")
                print("XSS Security: {}: Fail".format(counter))
                print("Sent: {} and Received: {}".format(i, message_data))
                pass_flag = 0
                return pass_flag
            except TimeoutException:
                pass_flag = 1
                print("no alert")
                print("XSS Security: {}: Pass".format(counter))

            counter += 1
            time.sleep(10)
        return pass_flag


    def xss_edit_contact(self,admin_user,admin_pass,xss_list,contact_number,nativeapp_driver):
        print("Test Case2: XSS Attack via Contact Edit")
        nativeapp_driver.refresh()
        pass_flag = 0
        nativeapp_driver = webdriver.Chrome('./chromedriver')
        nativeapp_driver.get(self.url)
        print(nativeapp_driver.title)
        google_user = nativeapp_driver.find_element_by_id("google-login-button").click()
        user_email = nativeapp_driver.find_element_by_id("identifierId").send_keys(admin_user)
        next_button = nativeapp_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(5)
        user_pass = nativeapp_driver.find_element_by_class_name("whsOnd.zHQkBf").send_keys(admin_pass)
        time.sleep(5)
        next_button = nativeapp_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(10)
        contact_button = nativeapp_driver.find_element_by_xpath(
            "//*[@id=\"LeftbarSection__listContainerId3\"]/li[1]/a/p/span").click()
        time.sleep(5)
        edit_contact = nativeapp_driver.find_element_by_xpath(
            "//*[@id=\"contact-info-container\"]/div/div[1]/div[2]/div[3]").click()
        time.sleep(5)


        counter = 1
        for i in xss_list:

            name = nativeapp_driver.find_element_by_xpath("//*[@id=\"display_name-field\"]").clear()
            time.sleep(1)
            name = nativeapp_driver.find_element_by_xpath("//*[@id=\"display_name-field\"]").send_keys(i)
            time.sleep(1)
            company = nativeapp_driver.find_element_by_xpath("//*[@id=\"company_name-field\"]").clear()
            time.sleep(1)
            company = nativeapp_driver.find_element_by_xpath("//*[@id=\"company_name-field\"]").send_keys(i)
            time.sleep(1)
            role = nativeapp_driver.find_element_by_xpath("//*[@id=\"job_title-field\"]").clear()
            time.sleep(1)
            role = nativeapp_driver.find_element_by_xpath("//*[@id=\"job_title-field\"]").send_keys(i)
            time.sleep(1)
            url = nativeapp_driver.find_element_by_xpath("//*[@id=\"urls-field\"]").clear()
            time.sleep(1)
            url = nativeapp_driver.find_element_by_xpath("//*[@id=\"urls-field\"]").send_keys(i)

            save_button = nativeapp_driver.find_element_by_xpath("//*[@id=\"save-edit-contact-button\"]/div/div").click()

            try:
                WebDriverWait(nativeapp_driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="alert"]')))

                alert = nativeapp_driver.switch_to.alert
                alert.accept()
                time.sleep(10)
                alert = nativeapp_driver.find_element_by_id("alert")
                print("alert accepted", alert.text)
                print("alert accepted")
                print("XSS Security: {}: Fail".format(counter))
                pass_flag = 0
                return pass_flag
            except TimeoutException:
                pass_flag = 1
                print("no alert")
                print("XSS Security: {}: Pass".format(counter))

            edit_contact = nativeapp_driver.find_element_by_xpath(
                "//*[@id=\"contact-info-container\"]/div/div[1]/div[2]/div[5]").click()

            #time.sleep(2)
            counter += 1
            time.sleep(10)


        name = nativeapp_driver.find_element_by_xpath("//*[@id=\"display_name-field\"]").send_keys(contact_number)
        company = nativeapp_driver.find_element_by_xpath("//*[@id=\"company_name-field\"]").clear()
        role = nativeapp_driver.find_element_by_xpath("//*[@id=\"job_title-field\"]").clear()
        url = nativeapp_driver.find_element_by_xpath("//*[@id=\"urls-field\"]").clear()
        save_button = nativeapp_driver.find_element_by_xpath("//*[@id=\"save-edit-contact-button\"]/div/div").click()
        time.sleep(5)
        return pass_flag

    def xss_edit_search(self, admin_user, admin_pass, xss_list, contact_number,nativeapp_driver):
        print("Test Case3: XSS Attack via Search")
        nativeapp_driver.refresh()
        pass_flag = 0
        nativeapp_driver = webdriver.Chrome('./chromedriver')
        nativeapp_driver.get(self.url)
        print(nativeapp_driver.title)
        google_user = nativeapp_driver.find_element_by_id("google-login-button").click()
        user_email = nativeapp_driver.find_element_by_id("identifierId").send_keys(admin_user)
        next_button = nativeapp_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(5)
        user_pass = nativeapp_driver.find_element_by_class_name("whsOnd.zHQkBf").send_keys(admin_pass)
        time.sleep(5)
        next_button = nativeapp_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(10)
        contact_button = nativeapp_driver.find_element_by_xpath(
            "//*[@id=\"LeftbarSection__listContainerId3\"]/li[1]/a/p/span").click()
        time.sleep(5)
        search_button = nativeapp_driver.find_element_by_xpath("//*[@id=\"hd-btn-search\"]/div[2]").click()
        time.sleep(1)

        counter = 1
        for i in xss_list:

            clear_search = nativeapp_driver.find_element_by_xpath("//*[@id=\"search-input\"]").clear()
            input_search = nativeapp_driver.find_element_by_xpath("//*[@id=\"search-input\"]").send_keys(i)
            enter_search = nativeapp_driver.find_element_by_xpath("//*[@id=\"search-input\"]").send_keys(u'\ue007')


            try:
                WebDriverWait(nativeapp_driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="alert"]')))

                alert = nativeapp_driver.switch_to.alert
                alert.accept()
                time.sleep(10)
                alert = nativeapp_driver.find_element_by_id("alert")
                print("alert accepted", alert.text)
                print("alert accepted")
                print("XSS Security: {}: Fail".format(counter))
                pass_flag = 0
                return pass_flag
            except TimeoutException:
                pass_flag = 1
                print("no alert")
                print("XSS Security: {}: Pass".format(counter))

            counter += 1
            time.sleep(3)


        return pass_flag



    def xss_edit_dial(self, admin_user, admin_pass, xss_list, contact_number,nativeapp_driver):
        print("Test Case4: XSS Attack via Dial")
        nativeapp_driver.refresh()
        pass_flag = 0
        nativeapp_driver = webdriver.Chrome('./chromedriver')
        nativeapp_driver.get(self.url)
        print(nativeapp_driver.title)
        google_user = nativeapp_driver.find_element_by_id("google-login-button").click()
        user_email = nativeapp_driver.find_element_by_id("identifierId").send_keys(admin_user)
        next_button = nativeapp_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(5)
        user_pass = nativeapp_driver.find_element_by_class_name("whsOnd.zHQkBf").send_keys(admin_pass)
        time.sleep(5)
        next_button = nativeapp_driver.find_element_by_class_name("VfPpkd-RLmnJb").click()
        time.sleep(10)
        contact_button = nativeapp_driver.find_element_by_xpath(
            "//*[@id=\"LeftbarSection__listContainerId3\"]/li[1]/a/p/span").click()
        time.sleep(5)
        dial_button = nativeapp_driver.find_element_by_xpath("//*[@id=\"leftbar-revamp\"]/div/div/div[1]/div/button[1]").click()
        time.sleep(1)

        counter = 1
        for i in xss_list:

            clear_search = nativeapp_driver.find_element_by_xpath("//*[@id=\"search-input\"]").clear()
            input_search = nativeapp_driver.find_element_by_xpath("//*[@id=\"search-input\"]").send_keys(i)
            enter_search = nativeapp_driver.find_element_by_xpath("//*[@id=\"search-input\"]").send_keys(u'\ue007')
            #dial_search = nativeapp_driver.find_element_by_xpath("//*[@id=\"new-call-make-call\"]").click()

            try:
                WebDriverWait(nativeapp_driver, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="alert"]')))


                alert = nativeapp_driver.switch_to.alert
                alert.accept()
                time.sleep(10)
                alert = nativeapp_driver.find_element_by_id("alert")
                print("alert accepted",alert.text)
                print("XSS Security: {}: Fail".format(counter))
                pass_flag = 0
                return pass_flag
            except TimeoutException:
                pass_flag = 1
                print("no alert")
                print("XSS Security: {}: Pass".format(counter))

            counter += 1
            time.sleep(3)


        return pass_flag


    def xss_edit_status(self, admin_user, admin_pass, xss_list, contact_number,nativeapp_driver):
        print("Test Case5: XSS Attack via Status")
        nativeapp_driver.refresh()
        pass_flag = 0
        time.sleep(15)
        #contact_button = nativeapp_driver.find_element_by_xpath(
        #    "//*[@id=\"LeftbarSection__listContainerId3\"]/li[1]/a/p/span").click()

        #time.sleep(1)

        counter = 1
        for i in xss_list:

            profile_status = nativeapp_driver.find_element_by_xpath("//*[@id=\"hd-status-msg\"]/div/div/div[1]/div/div").click()
            #profile_status = nativeapp_driver.find_element_by_class_name(
            #    "status-message__display").click()
            time.sleep(2)
            #clear_status = nativeapp_driver.find_element_by_class_name("//*[@id=\"popup_x\"]/line[2]").click()
            clear_status = nativeapp_driver.find_element_by_class_name("status-menu__delete").click()
            time.sleep(2)
            profile_status = nativeapp_driver.find_element_by_xpath(
                "//*[@id=\"hd-status-msg\"]/div/div/div[1]/div/div").click()
            input_status = nativeapp_driver.find_element_by_xpath("//*[@id=\"hd-status-msg\"]/div/div/div[1]/div[2]/div[1]/label/div[2]/input").send_keys(i)

            save_status = nativeapp_driver.find_element_by_xpath("//*[@id=\"hd-status-msg\"]/div/div/div[1]/div[2]/div[4]").click()


            try:
                WebDriverWait(nativeapp_driver, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="alert"]')))


                alert = nativeapp_driver.switch_to.alert
                alert.accept()
                time.sleep(10)
                alert = nativeapp_driver.find_element_by_id("alert")
                print("alert accepted",alert.text)
                print("XSS Security: {}: Fail".format(counter))
                pass_flag = 0
                return pass_flag
            except TimeoutException:
                pass_flag = 1
                print("no alert")
                print("XSS Security: {}: Pass".format(counter))

            counter += 1
            time.sleep(5)


        return pass_flag




    def check_for_message(self):
        api_url = "https://dialpadbeta.com/api/contact/"+self.contact_id+"?is_affinity=1&target_key="+self.admin_id+"&cached=1"
        #print("API:", api_url)

        header = {
            'authority': 'dialpadbeta.com',
            'User-Agent': 'PostmanRuntime/7.26.8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.authorization,
            'referer': 'https://dialpadbeta.com/'
        }

        r = requests.get(api_url,headers=header)
        soup = BeautifulSoup(r.content, 'html5lib')
        content = soup.get_text()
        json_content = json.loads(soup.text)
        response_data = json_content["description"]

        return r.status_code, json_content



