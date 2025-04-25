import unittest
unittest.TestLoader.sortTestMethodsUsing = None
import sys
import time
from callcenters import CallCenters
import pytest
import allure
import re

url = 'https://dialpadbeta.com/api/v2/callcenters/'
office_id = '5594532661428224'
apikey = 'ULLc7YuA4S47aCKzKufM5NbBZr8jgqgvjJLDrwHfZjSQYwBJ2DGxsexzEVNVevsMvxTZwLn5cLA7mTT95HZhS7HhQq4M2H4yUhg9'
callcenter_id = '6472213307064320'
name = 'AutoCC'
phonelist = ['+16095687833','+16092013441']
operator_names = ['Testdialpad','PD']
operator_id = ['4522934864969728','5955753775202304']

class TestCallCenter(unittest.TestCase):

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.callcenter
    def test_test1_get_callcenter_id(self):
        callcenter = CallCenters(url,apikey,callcenter_id)
        get_callcenter_code,get_callcenter_content = callcenter.get_callcenter_by_id()
        if get_callcenter_code == 200:
            self.assertTrue(True,"Test1: Get Call Center by id. Response did not match")
            callcenter_name = get_callcenter_content["name"]
            callcenter_office_id = get_callcenter_content["office_id"]
            callcenter_phone1 = get_callcenter_content["phone_numbers"][0]
            callcenter_phone2 = get_callcenter_content["phone_numbers"][1]

            if (callcenter_name == name) and (callcenter_office_id == office_id) and (callcenter_phone1 in phonelist) and (callcenter_phone2 in phonelist):
                print("The call center name is {} and it belongs to office id {}. The call center has phone numbers {} and {}".format(callcenter_name,callcenter_office_id,callcenter_phone1,callcenter_phone2))
            else:
                print("The call center has mismatched data")

        else:
            message = get_callcenter_content['error']['message']
            print("The user was not created. Received error response: {}: {}".format(get_callcenter_code, message))

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.callcenter
    def test_test2_get_callcenter_operators(self):
        callcenter = CallCenters(url, apikey, callcenter_id)
        get_callcenter_code, get_callcenter_content = callcenter.get_callcenter_operators()

        if get_callcenter_code == 200:
            self.assertTrue(True, "Test2: Get Call Center Operators. Response did not match")

            callcenter_operator1_name = get_callcenter_content["users"][0]["first_name"]
            callcenter_operator1_id = get_callcenter_content["users"][0]["id"]
            callcenter_operator2_name = get_callcenter_content["users"][1]["first_name"]
            callcenter_operator2_id = get_callcenter_content["users"][1]["id"]

            if (callcenter_operator1_name in operator_names) and (callcenter_operator2_name in operator_names) and (callcenter_operator1_id in operator_id) and (callcenter_operator2_id in operator_id):
                print("The call center has operators {} and {}".format(callcenter_operator1_name,callcenter_operator2_name))

        else:
            message = get_callcenter_content['error']['message']
            print("The user was not created. Received error response: {}: {}".format(get_callcenter_code, message))
            self.assertTrue(False)

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.callcenter
    def test_test3_remove_callcenter_operators(self):
        callcenter = CallCenters(url, apikey, callcenter_id)
        get_callcenter_code, get_callcenter_content = callcenter.remove_callcenter_operator(operator_id[1])

        if get_callcenter_code == 200:
            self.assertTrue(True, "Test3: Remove Call Center Operator. Response did not match")
            get_callcenter_operator_code, get_callcenter_operator_content = callcenter.get_callcenter_operators()
            if (len(get_callcenter_operator_content["users"]) == 1):
                print("The operator with id {} has been successfully removed from the call center".format(operator_id[1]))

        else:
            message = get_callcenter_content['error']['message']
            print("The user was not created. Received error response: {}: {}".format(get_callcenter_code, message))
            self.assertTrue(False)

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.callcenters
    def test_test4_add_callcenter_operators(self):
        callcenter = CallCenters(url, apikey, callcenter_id)
        get_callcenter_code, get_callcenter_content = callcenter.add_callcenter_operator(operator_id[1])

        if get_callcenter_code == 200:
            self.assertTrue(True, "Test4: Add Call Center Operator. Response did not match")
            get_callcenter_operator_code, get_callcenter_operator_content = callcenter.get_callcenter_operators()
            if (len(get_callcenter_operator_content["users"]) == 2):
                print(
                    "The operator with id {} has been successfully added from the call center".format(operator_id[1]))

        else:
            message = get_callcenter_content['error']['message']
            print("The user was not created. Received error response: {}: {}".format(get_callcenter_code, message))
            self.assertTrue(False)

