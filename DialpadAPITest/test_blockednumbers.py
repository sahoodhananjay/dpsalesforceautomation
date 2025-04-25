import unittest
unittest.TestLoader.sortTestMethodsUsing = None
import sys
import time
from blockednumbers import BlockedNumbers
import pytest
import allure
import re

url = 'https://dialpadbeta.com/api/v2/blockednumbers'
office_id = '5594532661428224'
apikey = 'ULLc7YuA4S47aCKzKufM5NbBZr8jgqgvjJLDrwHfZjSQYwBJ2DGxsexzEVNVevsMvxTZwLn5cLA7mTT95HZhS7HhQq4M2H4yUhg9'
numberlist = ['+16095687840','+16095577901']


class TestBlockedNumbers(unittest.TestCase):

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.blockednumber
    def test_test1_get_blockednumber_list(self):
        blocked_numbers = BlockedNumbers(apikey,url)
        print("\nGet The Blocked Number List\n")
        blocked_numbers_code,blocked_numbers_content = blocked_numbers.get_blocknumber_list()
        #self.assertEqual(200, blocked_numbers_code, "Test1: Get Blocked Number List: Response did not match")
        if blocked_numbers_code == 200:
            self.assertTrue(True,"Test1: Get Blocked Number List: Response did not match")

        else:
            message = blocked_numbers_content['error']['message']
            print("Received error response: {}: {}".format(blocked_numbers_code, message))
            self.assertTrue(False)

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.blockednumber
    def test_test2_add_blockednumbers(self):
        blocked_numbers = BlockedNumbers(apikey, url)
        print("\nAdd New Blocked Numbers\n")
        blocked_numbers_code, blocked_numbers_content = blocked_numbers.add_blocked_numbers(numberlist)
        # self.assertEqual(200, blocked_numbers_code, "Test1: Get Blocked Number List: Response did not match")

        if blocked_numbers_code == 204:

            self.assertTrue(True, "Test2: Add Blocked Number : Response did not match")
            print("Check if correct numbers were blocked.")
            add_blocked_numbers_code, add_blocked_numbers_content = blocked_numbers.get_blocknumber_list()
            numbers = add_blocked_numbers_content['items']
            # print("numbers:",len(numbers),numbers[0]['number'])
            num1 = numbers[0]['number']
            num2 = numbers[1]['number']
            if (num1 in numberlist) and (num2 in numberlist):
                self.assertTrue(True, "Test2: Blocked Number Not Present")
                print("Both numbers {} and {} are successfully blocked".format(num1, num2))
        else:
            message = blocked_numbers_content['error']['message']
            print("Received error response: {}: {}".format(blocked_numbers_code, message))
            self.assertTrue(False)

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.blockednumbers
    def test_test3_remove_blockednumbers(self):
        blocked_numbers = BlockedNumbers(apikey, url)
        print("\nRemove Blocked Numbers\n")
        blocked_numbers_code, blocked_numbers_content = blocked_numbers.remove_blocked_numbers(numberlist)
        # self.assertEqual(200, blocked_numbers_code, "Test1: Get Blocked Number List: Response did not match")

        if blocked_numbers_code == 204:

            self.assertTrue(True, "Test3: Remove Blocked Number : Response did not match")
            print("Check if correct numbers were unblocked.")
            remove_blocked_numbers_code, remove_blocked_numbers_content = blocked_numbers.get_blocknumber_list()
            self.assertEqual(200, remove_blocked_numbers_code, "Test3: Remove Blocked Number List: Response did not match")
        else:
            message = blocked_numbers_content['error']['message']
            print("Received error response: {}: {}".format(blocked_numbers_code, message))
            self.assertTrue(False)



