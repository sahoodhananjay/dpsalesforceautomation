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

class DialpadApi:

    def __init__(self,url):
        self.url = url


    def get_company_details(self,apikey):
        api_url = self.url + "company?apikey="+apikey
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

    def create_company(self,apikey,acct_type,admin_email,domain,tmo_order_id,name,authorization):
        #api_url = self.url + "company?apikey=" + apikey
        api_url = self.url + "company"
        print("API:", api_url)
        header = {
            'authority': 'dialpadbeta.com',
            'User-Agent': 'PostmanRuntime/7.26.8',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': authorization,
            'referer': 'https://dialpadbeta.com/'
        }
        body = {
            "account_type": acct_type,
            "admin_email": admin_email,
            "billing_contact": {
                "address_line_1": "1 Z CROSS ST",
                "address_line_2": "SAN FRANCISCO",
                "city": "SAN FRANCISCO",
                "country": "CA",
                "postal_code": "94112",
                "region": "None"
            },
            "country": "us",
            "domain": domain,
            "licenses": {
                "additional_number_line_delta": "2",
                "contact_center_line_delta": "2",
                "fax_line_delta": "2",
                "magenta_line_delta": "2",
                "room_line_delta": "2",
                "sell_line_delta": "2",
                "talk_line_delta": "2",
                "tmobile_order_id": tmo_order_id,
                "tollfree_additional_number_line_delta": "2",
                "tollfree_room_line_delta": "2",
                "uberconference_line_delta": "2"
            },
            "name": name,
            "plan_period": "monthly",
            "tmobile_billing_account": "bc-test-tmobile-api",
            "tmobile_dealer_code": "dc-test-tmobile-api",
            "tmobile_dealer_email": "testtmobileapi@g.com"
        }

        r = requests.post(api_url, data=json.dumps(body), headers=header)

        soup = BeautifulSoup(r.content, 'html5lib')
        content = soup.get_text()
        print(r.status_code)
        print(content)
        json_content = json.loads(soup.text)
        # response_data = json_content["phone_numbers"]

        return r.status_code, json_content
