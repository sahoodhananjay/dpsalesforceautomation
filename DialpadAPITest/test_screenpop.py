import unittest
unittest.TestLoader.sortTestMethodsUsing = None
import sys
import time
from screenpop import Screenpop
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


url = 'https://dialpadbeta.com/oauth2/'
client_id = 'jsT5NxGpNA2qk2Ny79fJnQUpw'
redirect_uri = 'https://www.dialpadbeta.com'
screen_pop_url = 'yahoo.com'
scope = 'screen_pop'
authorization = 'Bearer ZMd5a5j8LZAN9dngG5C6KUwjRccrZww33DrKwwQaWuVtTaTbtAGFTZacqwuGVrQUqMvt4QfDXJ24UZLjkdRJHNN39y7F7sXvkZ4C'
#authorization = 'ULLc7YuA4S47aCKzKufM5NbBZr8jgqgvjJLDrwHfZjSQYwBJ2DGxsexzEVNVevsMvxTZwLn5cLA7mTT95HZhS7HhQq4M2H4yUhg9'
client_secret = 'cawLuSXkP43KGStBEfnJwLnA4uKacChuU9EQ3x9S5kVczDhW85'
user = '4522934864969728'
second_office_user_id = '5006542366310400'
second_office_user_auth = 'Bearer rEavdcMAWbtbrnrhkd44xKyH9vUB6LjKb2PzkkhDeBjpV8kPkGNXTymFkmtLRymLmhTWw57CStxdq7tBnpKeThhgcdSmDwSRBsp6'
expected_type = 'harness'
non_admin_user = 'dpautouser1@gmail.com'
non_admin_pass = 'Dial@1234'
admin_user = 'dsahoo@dialpad.com'
admin_pass = 'March05@2012'
salesforce = 'https://dialpadbeta.com/salesforcecallcenter'
salesforce_user = 'qa@dialpad.com.lightning'
salesforce_pass = 'Ugses5Gsly'
received_access_code = []
received_api_key = []
response_code = 200


class TestScreenpop(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Running SetUP")
        screenpop = Screenpop(url, client_id, redirect_uri, scope, authorization, client_secret)
        accesscode = screenpop.get_access_code(True)
        print("Main: Access Code:", accesscode[0])
        received_access_code.append(accesscode[0])
        apikey = screenpop.get_api_key(accesscode[0])
        print("Main: API Key:", apikey[0])
        received_api_key.append(apikey[0])

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.quicktest
    def test_test1_check_for_screenpop_url(self):
        screenpop = Screenpop(url, client_id, redirect_uri, scope, authorization, client_secret)
        statuscode = screenpop.test1_check_for_screenpop_url(user,expected_type,non_admin_user,non_admin_pass,200,screen_pop_url,received_api_key[0])
        print("Main: Test1 Response:",statuscode)
        self.assertEqual(200,statuscode,"Test1: Response did not match")

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.quicktest
    def test_test2_check_when_scope_not_enabled(self):
        screenpop = Screenpop(url,client_id,redirect_uri,scope,authorization,client_secret)
        statuscode = screenpop.test2_check_when_scope_not_enabled(admin_user,admin_pass)
        print("Main: Test2 Response:",statuscode)
        expected_respose = 'Invalid scopes'
        self.assertTrue(expected_respose in statuscode)

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.quicktest
    def test_test3_check_talk_license_enabled(self):
        screenpop = Screenpop(url,client_id,redirect_uri,scope,authorization,client_secret)
        statuscode = screenpop.test3_check_talk_license_enabled(admin_user,admin_pass)
        print("Main: Test3 Response:",statuscode)
        expected_respose = 'integration requires one of the following licenses: Talk'
        self.assertTrue(expected_respose in statuscode)

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.quicktest
    def test_test4_check_redirectserver_not_enabled(self):
        screenpop = Screenpop(url,client_id,redirect_uri,scope,authorization,client_secret)
        statuscode = screenpop.test4_check_redirectserver_not_enabled(admin_user,admin_pass)
        print("Main: Test4 Response:",statuscode)
        expected_respose = 'Invalid redirect URI'
        self.assertTrue(expected_respose in statuscode)

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.quicktest
    def test_test5_check_for_screenpop_url_with_cti(self):
        expected_type = 'salesforce'
        screenpop = Screenpop(url, client_id, redirect_uri, scope, authorization, client_secret)
        statuscode = screenpop.test5_check_for_screenpop_url_with_cti(user,expected_type,non_admin_user,non_admin_pass,200,screen_pop_url,received_api_key[0],salesforce,salesforce_user,salesforce_pass)
        print("Main: Test5 Response:",statuscode)
        self.assertEqual(200,statuscode,"Test5: Response did not match")

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.quicktest
    def test_test6_check_for_screenpop_url_as_admin_for_nonadmin(self):
        screenpop = Screenpop(url, client_id, redirect_uri, scope, authorization, client_secret)
        statuscode = screenpop.test6_check_for_screenpop_url_as_admin_for_nonadmin(second_office_user_id,expected_type,received_api_key[0])
        print("Main: Test6 Response:", statuscode)
        self.assertEqual(200, statuscode, "Test6: Response did not match")

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.quicktest
    def test_test7_check_for_screenpop_url_as_nonadmin(self):
        authorization = second_office_user_auth
        screenpop = Screenpop(url, client_id, redirect_uri, scope, authorization, client_secret)
        statuscode = screenpop.test7_check_for_screenpop_url_as_nonadmin(second_office_user_id,expected_type)
        print("Main: Test7 Response:", statuscode)
        self.assertEqual(200, statuscode, "Test7: Response did not match")

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.quicktest
    def test_test8_check_for_screenpop_url_as_nonadmin_for_admin(self):
        authorization = second_office_user_auth
        screenpop = Screenpop(url, client_id, redirect_uri, scope, authorization, client_secret)
        statuscode = screenpop.test8_check_for_screenpop_url_as_nonadmin_for_admin(user,expected_type)
        print("Main: Test8 Response:", statuscode)
        self.assertEqual(404, statuscode, "Test8: Response did not match")



    #def test_check_print(self):
    #    screenpop = Screenpop(url,client_id,redirect_uri,scope,authorization,client_secret)
    #    accesscode = screenpop.get_access_code(False)
    #    print("Y")










if __name__ == '__main__':
    unittest.main()















