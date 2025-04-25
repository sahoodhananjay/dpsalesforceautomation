import pandas as pd
import numpy as np
from tqdm import tqdm
import requests
import re
from bs4 import BeautifulSoup
import csv
import json
import time
from numpy.random import randint

import warnings
warnings.filterwarnings("ignore")

class UserNumbers:

    def __init__(self,url,office_id,apikey,domain,license,auto_assign,company_area_code,number,new_area_code):
        self.url = url
        self.office_id = office_id
        self.apikey = apikey
        self.domain = domain
        self.license = license
        self.auto_assign = auto_assign
        self.company_area_code = company_area_code
        self.number = number
        self.new_area_code = new_area_code
        #self.authorization = authorization

    def generate_randomuser(self):
        return "testuser_"+str(randint(0,100,1).item())+"@"+self.domain

    def create_user_and_assign_number(self,user):
        #user = self.generate_randomuser()
        #print("Creating new user:",user)
        api_url = self.url +"users?apikey="+self.apikey
        print("API:", api_url)
        header = {
            'authority': 'dialpadbeta.com',
            'User-Agent': 'PostmanRuntime/7.26.8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            #'authorization': self.authorization,
            'referer': 'https://dialpadbeta.com/'
            }
        body = {
            "email": user,
            "license": self.license,
            "office_id": self.office_id,
            "auto_assign": self.auto_assign
        }

        r = requests.post(api_url, data=json.dumps(body), headers=header)
        soup = BeautifulSoup(r.content, 'html5lib')
        content = soup.get_text()
        print(r.status_code)
        print(content)
        json_content = json.loads(soup.text)
        #response_data = json_content["phone_numbers"]

        return r.status_code,json_content

    def assign_number(self,id,target_type,flag):
        api_url = self.url + "numbers/assign?apikey=" + self.apikey
        print("API:", api_url)
        header = {
            'authority': 'dialpadbeta.com',
            'User-Agent': 'PostmanRuntime/7.26.8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            # 'authorization': self.authorization,
            'referer': 'https://dialpadbeta.com/'
        }
        if flag == 'number':
            body = {
                "target_id": id,
                "target_type": target_type,
                "office_id": self.office_id,
                "auto_assign": self.auto_assign,
                "number": self.number
                }
        if flag == 'area_code':
            body = {
                "target_id": id,
                "target_type": target_type,
                "office_id": self.office_id,
                "auto_assign": self.auto_assign,
                "area_code": self.new_area_code
                }
        if flag == 'both':
            body = {
                "target_id": id,
                "target_type": target_type,
                "office_id": self.office_id,
                "auto_assign": self.auto_assign,
                "area_code": self.new_area_code,
                "number": self.number
                }


        r = requests.post(api_url, data=json.dumps(body), headers=header)
        soup = BeautifulSoup(r.content, 'html5lib')
        content = soup.get_text()
        print(r.status_code)
        print(content)
        json_content = json.loads(soup.text)
        # response_data = json_content["phone_numbers"]

        return r.status_code, json_content


    def delete_user(self,id):
        api_url = self.url + "users/"+id+"?apikey=" + self.apikey
        print("API:", api_url)
        header = {
            'authority': 'dialpadbeta.com',
            'User-Agent': 'PostmanRuntime/7.26.8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            #'authorization': self.authorization,
            'referer': 'https://dialpadbeta.com/'
        }

        r = requests.delete(api_url, headers=header)
        soup = BeautifulSoup(r.content, 'html5lib')
        content = soup.get_text()
        print(r.status_code)
        print(content)
        json_content = json.loads(soup.text)
        # response_data = json_content["phone_numbers"]

        return r.status_code, json_content


    def get_user(self,id):
        api_url = self.url + "users/"+id+"?apikey=" + self.apikey
        print("API:", api_url)
        header = {
            'authority': 'dialpadbeta.com',
            'User-Agent': 'PostmanRuntime/7.26.8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            #'authorization': self.authorization,
            'referer': 'https://dialpadbeta.com/'
        }

        r = requests.get(api_url, headers=header)
        soup = BeautifulSoup(r.content, 'html5lib')
        content = soup.get_text()
        print(r.status_code)
        print(content)
        json_content = json.loads(soup.text)
        # response_data = json_content["phone_numbers"]

        return r.status_code, json_content

    def unassign_number(self,number):
        api_url = self.url + "numbers/"+number+"?apikey=" + self.apikey
        print("API:", api_url)
        header = {
            'authority': 'dialpadbeta.com',
            'User-Agent': 'PostmanRuntime/7.26.8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            #'authorization': self.authorization,
            'referer': 'https://dialpadbeta.com/'
        }

        r = requests.delete(api_url, headers=header)
        soup = BeautifulSoup(r.content, 'html5lib')
        content = soup.get_text()
        print(r.status_code)
        print(content)
        json_content = json.loads(soup.text)
        # response_data = json_content["phone_numbers"]

        return r.status_code, json_content




    def test2_assign_num(self):
        user = 'testuser_83@dp.com'
        id = '5655097525403648'
        api_url = self.url + "numbers/assign?apikey=" + self.apikey
        print("API:", api_url)
        header = {
            'authority': 'dialpadbeta.com',
            'User-Agent': 'PostmanRuntime/7.26.8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            # 'authorization': self.authorization,
            'referer': 'https://dialpadbeta.com/'
        }
        body = {
            "target_id": id,
            "target_type": "user"
        }

        r = requests.post(api_url, data=json.dumps(body), headers=header)
        soup = BeautifulSoup(r.content, 'html5lib')
        content = soup.get_text()
        print(r.status_code)
        #print(content)
        json_content = json.loads(soup.text)
        response_data = json_content["error"]
        #print("here:",type(response_data))
        print("there",content)

        if r.status_code == 200:
            if re.search("number", content):
                pattern = re.compile(r"(.*?)\s+(\"number\"\:(.*?))")
                match = pattern.match(content)
                phone = match.group(2)
                print("Auto Assign {} to {}".format(phone, user))
                auto_assigned = True
                return r.status_code, auto_assigned
            else:
                auto_assigned = False
                return r.status_code, auto_assigned
        else:
            message = response_data['message']
            return r.status_code, message












    def check_print(self):
        print("test", 2*2)
        return (2*2)