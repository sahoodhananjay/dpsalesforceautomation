import unittest
unittest.TestLoader.sortTestMethodsUsing = None
import sys
import time
from sql_injection_frontend import SQL_Injection_Frontend
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.keys import Keys



url = 'https://dialpadbeta.com/app'
authorization = 'Bearer FAmAydvJ7CzH3CEQ33yhUPJ7dCuCL7BsuL8Hs9hpVUyLUdK9eLrJhhnsrtRUrAGXrytuPWyVDuqpbP3PC57ee68yesCj5F9PZQNk'
admin_user = 'testdialpad14@gmail.com'
admin_pass = 'Dial@1234'
admin_id = 'aglzfnV2LWJldGFyGAsSC1VzZXJQcm9maWxlGICAsI3GwIIJDA'
contact_id = 'aglzfnV2LWJldGFyFAsSB0NvbnRhY3QYgICwjabcugsM'
contact_number = "(401) 295-3682"
driver_context = []

sql_injection_list = [
                     'Testdialpad1 AND 1=1#',
                     'Testdialpad1 OR 1=1#',
                     'Testdialpad1 AND 89=89#',
                     'Testdialpad1 OR 89=89#',
                     '(609) 201-3445 +AND+1=1#',
                     '(609) 201-3445 aNd 1=1#',
                     '(609) 201-3445 AND%201=1%23'
                     ]

#dialpad123' AND 1=1#
#dialpad123' OR 1=1#
#dialpad123' AND 89=89#
#dialpad123' OR 89=89#
#dialpad123'+AND+1=1#
#dialpad123' aNd 1=1#
#dialpad123%27%20AND%201=1%23

class TestSQL_Injection_Frontend(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Running SetUP Login")
        sql_injection = SQL_Injection_Frontend(url, admin_id, authorization, contact_id)
        driver = sql_injection.native_app_login(admin_user, admin_pass, sql_injection_list)
        driver_context.append(driver)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Assess SQL Injection threat on the Search input fields." + "\n" +
                        '\nFollowing SQL Injection threats were run:' + "\n" +
                        '1. Testdialpad1 AND 1=1#' + "\n" +
                        '2. Testdialpad1 OR 1=1#' + "\n" +
                        '3. Testdialpad1 AND 89=89#' + "\n" +
                        '4. Testdialpad1 OR 89=89#' + "\n" +
                        '5. (609) 201-3445 +AND+1=1#' + "\n" +
                        "6. (609) 201-3445 aNd 1=1#" + "\n" +
                        '7. (609) 201-3445 AND%201=1%23'
                        )
    @pytest.mark.sql
    def test_sql_frontend_search(self):
        sql_injection = SQL_Injection_Frontend(url, admin_id, authorization, contact_id)
        statuscode = sql_injection.sql_edit_search(admin_user, admin_pass, sql_injection_list, contact_number, driver_context[0])
        print("Main: Test1 Response:", statuscode)
        self.assertEqual(1, statuscode, "Test1: SQL Injection threat found")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Assess SQL Injection threat on the User Dial input fields" + "\n" +
                        '\nFollowing XSS threats were run:' + "\n" +
                        '1. Testdialpad1 AND 1=1#' + "\n" +
                        '2. Testdialpad1 OR 1=1#' + "\n" +
                        '3. Testdialpad1 AND 89=89#' + "\n" +
                        '4. Testdialpad1 OR 89=89#' + "\n" +
                        '5. (609) 201-3445 +AND+1=1#' + "\n" +
                        "6. (609) 201-3445 aNd 1=1#" + "\n" +
                        '7. (609) 201-3445 AND%201=1%23'
                        )
    @pytest.mark.sql
    def test_sql_frontend_dial(self):
        sql_injection = SQL_Injection_Frontend(url, admin_id, authorization, contact_id)
        statuscode = sql_injection.sql_edit_dial(admin_user, admin_pass, sql_injection_list, contact_number, driver_context[0])
        print("Main: Test2 Response:", statuscode)
        self.assertEqual(1, statuscode, "Test2: SQL Injection threat found")

    @classmethod
    def tearDownClass(cls):
        driver_context[0].quit()