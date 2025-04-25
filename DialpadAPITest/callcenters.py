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

class CallCenters:

    def __init__(self,url,apikey,callcenter):
        self.url = url
        self.apikey = apikey
        self.callcenter = callcenter


    def get_callcenter_by_id(self):
        api_url = self.url + self.callcenter+"?apikey=" + self.apikey
        print("API:", api_url)
        header = {
            'authority': 'dialpadbeta.com',
            'User-Agent': 'PostmanRuntime/7.26.8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            # 'authorization': self.authorization,
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

    def get_callcenter_operators(self):
        api_url = self.url + self.callcenter+"/operators?apikey=" + self.apikey
        print("API:", api_url)
        header = {
            'authority': 'dialpadbeta.com',
            'User-Agent': 'PostmanRuntime/7.26.8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            # 'authorization': self.authorization,
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


    def remove_callcenter_operator(self,id):
        api_url = self.url + self.callcenter+"/operators?apikey=" + self.apikey
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
            "user_id": id
            }

        r = requests.delete(api_url, data=json.dumps(body), headers=header)
        soup = BeautifulSoup(r.content, 'html5lib')
        content = soup.get_text()
        print(r.status_code)
        print(content)
        json_content = json.loads(soup.text)
        # response_data = json_content["phone_numbers"]

        return r.status_code, json_content


    def add_callcenter_operator(self,id):
        api_url = self.url + self.callcenter+"/operators?apikey=" + self.apikey
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
            "keep_paid_numbers": True,
            "license_type": "agents",
            "role": "operator",
            "skill_level": 100,
            "user_id": id
            }

        r = requests.post(api_url, data=json.dumps(body), headers=header)
        soup = BeautifulSoup(r.content, 'html5lib')
        content = soup.get_text()
        print(r.status_code)
        print(content)
        json_content = json.loads(soup.text)
        # response_data = json_content["phone_numbers"]

        return r.status_code, json_content
