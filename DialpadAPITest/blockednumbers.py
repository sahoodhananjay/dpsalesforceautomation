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


class BlockedNumbers:

    def __init__(self,apikey,url):
        self.apikey = apikey
        self.url = url

    def get_blocknumber_list(self):
        api_url = self.url + "?apikey=" + self.apikey
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


    def add_blocked_numbers(self,numberlist):
        api_url = self.url + "/add?apikey=" + self.apikey
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
            "numbers": numberlist
            }

        r = requests.post(api_url, data=json.dumps(body), headers=header)
        soup = BeautifulSoup(r.content, 'html5lib')
        content = soup.get_text()

        if r.status_code == 204:
            json_content = "Successful"
        else:
            json_content = json.loads(soup.text)

        print(r.status_code)
        print(content)

        # response_data = json_content["phone_numbers"]

        return r.status_code,json_content


    def remove_blocked_numbers(self,numberlist):
        api_url = self.url + "/remove?apikey=" + self.apikey
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
            "numbers": numberlist
            }

        r = requests.post(api_url, data=json.dumps(body), headers=header)
        soup = BeautifulSoup(r.content, 'html5lib')
        content = soup.get_text()

        if r.status_code == 204:
            json_content = "Successful"
        else:
            json_content = json.loads(soup.text)

        print(r.status_code)
        print(content)

        # response_data = json_content["phone_numbers"]

        return r.status_code,json_content


