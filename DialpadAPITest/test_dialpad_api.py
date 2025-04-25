import unittest
unittest.TestLoader.sortTestMethodsUsing = None
import sys
import time
from dialpad_api import DialpadApi
import pytest
import allure
import re

url = 'https://dialpadbeta.com/api/v2/'
#apikey = '8RX3V2YpvLHwk9tdJGpPK8ChushNmbhLaG5dtWBS2S2dZySdKbdaFc6p2jEVh4Zs69FjKUWBYzdTDPk8YAMstgnXmDg2QUDE8jDr'
#authorization = 'Bearer WtKU86s3tKWSWsdf7aPfLtcPZ8kuadHKZm2y9ZbvTxAUcW4UukbC8C3KaV76yHENRXPX5XaD23dheXESp3ACp24ypTZW3rCLDh84'
apikey = '9Ca5AXkhnJtqGtd5JvAMEtXmGnPtjZQExrn3frmBRUMSBtENCcGcdxzAEaphcqbPLZ4S6e3PyCTmML2nACNwPgBrbTmWzvyhGy8H'
authorization = 'Bearer 9Ca5AXkhnJtqGtd5JvAMEtXmGnPtjZQExrn3frmBRUMSBtENCcGcdxzAEaphcqbPLZ4S6e3PyCTmML2nACNwPgBrbTmWzvyhGy8H'
acct_type = 'standard'
admin_email = 'autoapiuser1@gmail.com'
domain = 'autoapi'
tmo_order_id = 'order-test-tmobile-api'
name = 'AutoAPI'



class TestDialpadApi(unittest.TestCase):

    #@pytest.mark.quicktest
    def test_test1_get_company_detail(self):

        company_id = '5217081372442624'
        company_name = 'autoTest'
        dialpadapi = DialpadApi(url)
        response_code,response_content = dialpadapi.get_company_details(apikey)
        self.assertEqual(200, response_code, "Test1 Get Company Details Failed. Response mismatch")


    #@pytest.mark.quicktest
    def test_test2_create_company(self):

        dialpadapi = DialpadApi(url)
        response_code,response_content = dialpadapi.create_company(apikey,acct_type,admin_email,domain,tmo_order_id,name,authorization)
        self.assertEqual(200, response_code, "Test2 Create Company Failed. Response mismatch")
        apikey_response = response_content['api_key']
        print("1", apikey_response['access_token'])
        print("2", apikey_response['target_id'])
        print("3", apikey_response['token_type'])
        company_response = response_content['company']
        print("4", company_response['account_type'])
        print("5", company_response['domain'])
        print("6", company_response['id'])
        print("7", company_response['state'])
        office_response = response_content['office']
        print("8", office_response['office_id'])
        print("9", office_response['name'])
        print("10", office_response['state'])
        plan_response = response_content['plan']
        print("11", plan_response['tmobile_order_id'])
        print("12", plan_response['sell_lines'])
        print("13", plan_response['talk_lines'])

