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



class SQL_Injection_Frontend:

    def __init__(self,url,admin_id,authorization,contact_id):
        self.url = url
        self.admin_id = admin_id
        self.authorization = authorization
        self.contact_id = contact_id


    def native_app_login(self,admin_user,admin_pass,sql_injection_list):

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


    def sql_edit_search(self, admin_user, admin_pass, sql_list, contact_number,nativeapp_driver):
        print("Test Case1: SQL Injection Attack via Search")
        nativeapp_driver.refresh()
        pass_flag = 0
        time.sleep(10)
        contact_button = nativeapp_driver.find_element_by_xpath(
            "//*[@id=\"LeftbarSection__listContainerId3\"]/li[1]/a/p/span").click()
        time.sleep(5)
        search_button = nativeapp_driver.find_element_by_xpath("//*[@id=\"hd-btn-search\"]/div[2]").click()
        time.sleep(1)

        counter = 1
        for i in sql_list:

            clear_search = nativeapp_driver.find_element_by_xpath("//*[@id=\"search-input\"]").clear()
            input_search = nativeapp_driver.find_element_by_xpath("//*[@id=\"search-input\"]").send_keys(i)
            time.sleep(5)
            enter_search = nativeapp_driver.find_element_by_xpath("//*[@id=\"search-input\"]").send_keys(u'\ue007')


            try:
                WebDriverWait(nativeapp_driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="alert"]')))

                # alert = nativeapp_driver.switch_to.alert
                # alert.accept()
                # time.sleep(10)
                alert = nativeapp_driver.find_element_by_id("alert")
                print("alert accepted", alert.text)
                print("alert accepted")
                print("SQL Security: {}: Pass".format(counter))
                pass_flag = 1
                return pass_flag
            except TimeoutException:
                pass_flag = 0
                print("no alert")
                print("SQL Security: {}: Fail".format(counter))

            counter += 1
            time.sleep(3)


        return pass_flag


    def sql_edit_dial(self, admin_user, admin_pass, sql_list, contact_number,nativeapp_driver):
        print("Test Case2: SQL Injection Attack via Dial")
        nativeapp_driver.refresh()
        pass_flag = 0
        time.sleep(10)
        contact_button = nativeapp_driver.find_element_by_xpath(
            "//*[@id=\"LeftbarSection__listContainerId3\"]/li[1]/a/p/span").click()
        time.sleep(5)
        dial_button = nativeapp_driver.find_element_by_xpath("//*[@id=\"leftbar-revamp\"]/div/div/div[1]/div/button[1]").click()
        time.sleep(1)

        counter = 1
        for i in sql_list:

            clear_search = nativeapp_driver.find_element_by_xpath("//*[@id=\"search-input\"]").clear()
            input_search = nativeapp_driver.find_element_by_xpath("//*[@id=\"search-input\"]").send_keys(i)
            time.sleep(5)
            enter_search = nativeapp_driver.find_element_by_xpath("//*[@id=\"search-input\"]").send_keys(u'\ue007')
            #dial_search = nativeapp_driver.find_element_by_xpath("//*[@id=\"new-call-make-call\"]").click()

            try:
                WebDriverWait(nativeapp_driver, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="alert"]')))


                #alert = nativeapp_driver.switch_to.alert
                #alert.accept()
                #time.sleep(10)
                alert = nativeapp_driver.find_element_by_id("alert")
                print("alert accepted",alert.text)
                print("SQL Security: {}: Pass".format(counter))
                pass_flag = 1
                return pass_flag
            except TimeoutException:
                pass_flag = 0
                print("no alert")
                print("SQL Security: {}: Fail".format(counter))

            counter += 1
            time.sleep(3)


        return pass_flag

