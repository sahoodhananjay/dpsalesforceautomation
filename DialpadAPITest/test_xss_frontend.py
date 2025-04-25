import unittest
unittest.TestLoader.sortTestMethodsUsing = None
import sys
import time
from xss_frontend import XSS_Frontend
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

xss_list = [
           '<script>alert(123);</script>',
           '<ScRipT>alert("XSS");</ScRipT>',
           '<script>alert(123)</script>',
           '<script>alert("hellox worldss");</script>',
           '<script>alert(\'XSS\')</script>',
           '<script>alert(\'XSS\');</script>',
           '<script>alert(\'XSS\')</script>',
           '\'><script>alert(\'XSS\')</script>',
           '<script>alert(/XSS/)</script>',
           '<script>alert(/XSS/)</script>',
           '</script><script>alert(1)</script>',
           '<ScRiPt>alert(1)</sCriPt>',
           '<IMG SRC=jAVasCrIPt:alert(\'XSS\')>',
           '<IMG SRC=\'javascript:alert(\'XSS\');\'>',
           '<IMG SRC=javascript:alert(&quot;XSS&quot;)>',
           '<IMG SRC=javascript:alert(\'XSS\')>'
           '<img src=xss onerror=alert(1)>',
           '<iframe src="javascript:alert(`xss`)">',
           '<iframe %00 src="&Tab;javascript:prompt(1)&Tab;"%00>',
           '<iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>',
           '<iframe/src="data:text/html;&Tab;base64&Tab;,PGJvZHkgb25sb2FkPWFsZXJ0KDEpPg==">'

           ]


class TestXSS_Frontend(unittest.TestCase):

    @classmethod
    @allure.description("Launching URL: https://dialpadbeta.com/app.")
    def setUpClass(cls):
        print("Running SetUP Login")
        xssfrontend = XSS_Frontend(url, admin_id, authorization, contact_id)
        driver = xssfrontend.native_app_login(admin_user, admin_pass, xss_list)
        driver_context.append(driver)

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Assess XSS vulnerabilities on the User Message input field." + "\n" +
                        "\nPlease Note: Since the Allure Report site suffers from XSS threat, the opening and closing bracets (< and \\\>) are removed from payloads. For e.g #16 is because of XSS attack" + "\n" +
                        "XSS Payload Source: https://pravinponnusamy.medium.com/xss-payloads-7079c53c8559." + "\n" +
                        '\nFollowing XSS threats were run:' + "\n" +
                        '1. script alert(123); script'  + "\n" +
                        '2. ScRipT alert(\"XSS\"); ScRipT ' + "\n" +
                        '3. script alert("hellox worldss"); script' + "\n" +
                        '4. script alert(\'XSS\') script' + "\n" +
                        '5. script alert(\'XSS\'); script' + "\n" +
                        "6. \'> script alert(\'XSS\') script" + "\n" +
                        '7. script alert(/XSS/) script' + "\n" +
                        '8. script script>alert(1) script' + "\n" +
                        '9. ScRiPt alert(1) sCriPt' + "\n" +
                        '10. IMG SRC=jAVasCrIPt:alert(\'XSS\')' + "\n" +
                        '11. IMG SRC=\'javascript:alert(\'XSS\');\'' + "\n" +
                        '12. IMG SRC=javascript:alert(&quot;XSS&quot;)' + "\n" +
                        '13. IMG SRC=javascript:alert(\'XSS\')' + "\n" +
                        '14. img src=xss onerror=alert(1)' + "\n" +
                        '15. iframe src="javascript:alert(`xss`)"' + "\n" +
                        '16. iframe %00 src="&Tab;javascript:prompt(1)&Tab;"%00' + "\n" +
                        '17. <iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>' + "\n" +
                        '18. iframe/src="data:text/html;&Tab;base64&Tab;,PGJvZHkgb25sb2FkPWFsZXJ0KDEpPg=="'

                        )


    @pytest.mark.xss
    def test_xss_frontend_message(self):
        xssfrontend = XSS_Frontend(url, admin_id, authorization,contact_id)
        statuscode = xssfrontend.xss_message(admin_user, admin_pass,xss_list,driver_context[0])
        print("Main: Test1 Response:", statuscode)
        #expected_respose = 'Invalid scopes'
        self.assertEqual(1,statuscode,"Test1: XSS threat found")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Assess XSS vulnerabilities on the User Contact input fields." + "\n" +
                         "\nPlease Note: Since the Allure Report site suffers from XSS threat, the opening and closing bracets (< and \\\>) are removed from payloads. For e.g #16 is because of XSS attack" + "\n" +
                        "XSS Payload Source: https://pravinponnusamy.medium.com/xss-payloads-7079c53c8559." + "\n" +
                        '\nFollowing XSS threats were run:' + "\n" +
                        '1. script alert(123); script'  + "\n" +
                        '2. ScRipT alert(\"XSS\"); ScRipT ' + "\n" +
                        '3. script alert("hellox worldss"); script' + "\n" +
                        '4. script alert(\'XSS\') script' + "\n" +
                        '5. script alert(\'XSS\'); script' + "\n" +
                        "6. \'> script alert(\'XSS\') script" + "\n" +
                        '7. script alert(/XSS/) script' + "\n" +
                        '8. script script>alert(1) script' + "\n" +
                        '9. ScRiPt alert(1) sCriPt' + "\n" +
                        '10. IMG SRC=jAVasCrIPt:alert(\'XSS\')' + "\n" +
                        '11. IMG SRC=\'javascript:alert(\'XSS\');\'' + "\n" +
                        '12. IMG SRC=javascript:alert(&quot;XSS&quot;)' + "\n" +
                        '13. IMG SRC=javascript:alert(\'XSS\')' + "\n" +
                        '14. img src=xss onerror=alert(1)' + "\n" +
                        '15. iframe src="javascript:alert(`xss`)"' + "\n" +
                        '16. iframe %00 src="&Tab;javascript:prompt(1)&Tab;"%00' + "\n" +
                        '17. <iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>' + "\n" +
                        '18. iframe/src="data:text/html;&Tab;base64&Tab;,PGJvZHkgb25sb2FkPWFsZXJ0KDEpPg=="'

                        )
    @pytest.mark.xss
    def test_xss_frontend_contact(self):
        xssfrontend = XSS_Frontend(url, admin_id, authorization, contact_id)
        statuscode = xssfrontend.xss_edit_contact(admin_user, admin_pass, xss_list,contact_number,driver_context[0])
        print("Main: Test2 Response:", statuscode)
        self.assertEqual(1, statuscode, "Test2: XSS threat found")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Assess XSS vulnerabilities on the Search input fields." + "\n" +
                        "\nPlease Note: Since the Allure Report site suffers from XSS threat, the opening and closing bracets (< and \\\>) are removed from payloads. For e.g #16 is because of XSS attack" + "\n" +
                        "XSS Payload Source: https://pravinponnusamy.medium.com/xss-payloads-7079c53c8559." + "\n" +
                        '\nFollowing XSS threats were run:' + "\n" +
                        '1. script alert(123); script' + "\n" +
                        '2. ScRipT alert(\"XSS\"); ScRipT ' + "\n" +
                        '3. script alert("hellox worldss"); script' + "\n" +
                        '4. script alert(\'XSS\') script' + "\n" +
                        '5. script alert(\'XSS\'); script' + "\n" +
                        "6. \'> script alert(\'XSS\') script" + "\n" +
                        '7. script alert(/XSS/) script' + "\n" +
                        '8. script script>alert(1) script' + "\n" +
                        '9. ScRiPt alert(1) sCriPt' + "\n" +
                        '10. IMG SRC=jAVasCrIPt:alert(\'XSS\')' + "\n" +
                        '11. IMG SRC=\'javascript:alert(\'XSS\');\'' + "\n" +
                        '12. IMG SRC=javascript:alert(&quot;XSS&quot;)' + "\n" +
                        '13. IMG SRC=javascript:alert(\'XSS\')' + "\n" +
                        '14. img src=xss onerror=alert(1)' + "\n" +
                        '15. iframe src="javascript:alert(`xss`)"' + "\n" +
                        '16. iframe %00 src="&Tab;javascript:prompt(1)&Tab;"%00' + "\n" +
                        '17. <iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>' + "\n" +
                        '18. iframe/src="data:text/html;&Tab;base64&Tab;,PGJvZHkgb25sb2FkPWFsZXJ0KDEpPg=="'

                        )
    @pytest.mark.xss
    def test_xss_frontend_search(self):
        xssfrontend = XSS_Frontend(url, admin_id, authorization, contact_id)
        statuscode = xssfrontend.xss_edit_search(admin_user, admin_pass, xss_list, contact_number,driver_context[0])
        print("Main: Test2 Response:", statuscode)
        self.assertEqual(1, statuscode, "Test3: XSS threat found")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Assess XSS vulnerabilities on the User Dial input fields" + "\n" +
                        "\nPlease Note: Since the Allure Report site suffers from XSS threat, the opening and closing bracets (< and \\\>) are removed from payloads. For e.g #16 is because of XSS attack" + "\n" +
                        "XSS Payload Source: https://pravinponnusamy.medium.com/xss-payloads-7079c53c8559." + "\n" +
                        '\nFollowing XSS threats were run:' + "\n" +
                        '1. script alert(123); script' + "\n" +
                        '2. ScRipT alert(\"XSS\"); ScRipT ' + "\n" +
                        '3. script alert("hellox worldss"); script' + "\n" +
                        '4. script alert(\'XSS\') script' + "\n" +
                        '5. script alert(\'XSS\'); script' + "\n" +
                        "6. \'> script alert(\'XSS\') script" + "\n" +
                        '7. script alert(/XSS/) script' + "\n" +
                        '8. script script>alert(1) script' + "\n" +
                        '9. ScRiPt alert(1) sCriPt' + "\n" +
                        '10. IMG SRC=jAVasCrIPt:alert(\'XSS\')' + "\n" +
                        '11. IMG SRC=\'javascript:alert(\'XSS\');\'' + "\n" +
                        '12. IMG SRC=javascript:alert(&quot;XSS&quot;)' + "\n" +
                        '13. IMG SRC=javascript:alert(\'XSS\')' + "\n" +
                        '14. img src=xss onerror=alert(1)' + "\n" +
                        '15. iframe src="javascript:alert(`xss`)"' + "\n" +
                        '16. iframe %00 src="&Tab;javascript:prompt(1)&Tab;"%00' + "\n" +
                        '17. <iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>' + "\n" +
                        '18. iframe/src="data:text/html;&Tab;base64&Tab;,PGJvZHkgb25sb2FkPWFsZXJ0KDEpPg=="'

                        )
    @pytest.mark.xss
    def test_xss_frontend_dial(self):
        xssfrontend = XSS_Frontend(url, admin_id, authorization, contact_id)
        statuscode = xssfrontend.xss_edit_dial(admin_user, admin_pass, xss_list, contact_number,driver_context[0])
        print("Main: Test4 Response:", statuscode)
        self.assertEqual(1, statuscode, "Test4: XSS threat found")

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("Assess XSS vulnerabilities on the User Status input field" + "\n" +
                        "\nPlease Note: Since the Allure Report site suffers from XSS threat, the opening and closing bracets (< and \\\>) are removed from payloads. For e.g #16 is because of XSS attack" + "\n" +
                        "XSS Payload Source: https://pravinponnusamy.medium.com/xss-payloads-7079c53c8559." + "\n" +
                        '\nFollowing XSS threats were run:' + "\n" +
                        '1. script alert(123); script' + "\n" +
                        '2. ScRipT alert(\"XSS\"); ScRipT ' + "\n" +
                        '3. script alert("hellox worldss"); script' + "\n" +
                        '4. script alert(\'XSS\') script' + "\n" +
                        '5. script alert(\'XSS\'); script' + "\n" +
                        "6. \'> script alert(\'XSS\') script" + "\n" +
                        '7. script alert(/XSS/) script' + "\n" +
                        '8. script script>alert(1) script' + "\n" +
                        '9. ScRiPt alert(1) sCriPt' + "\n" +
                        '10. IMG SRC=jAVasCrIPt:alert(\'XSS\')' + "\n" +
                        '11. IMG SRC=\'javascript:alert(\'XSS\');\'' + "\n" +
                        '12. IMG SRC=javascript:alert(&quot;XSS&quot;)' + "\n" +
                        '13. IMG SRC=javascript:alert(\'XSS\')' + "\n" +
                        '14. img src=xss onerror=alert(1)' + "\n" +
                        '15. iframe src="javascript:alert(`xss`)"' + "\n" +
                        '16. iframe %00 src="&Tab;javascript:prompt(1)&Tab;"%00' + "\n" +
                        '17. <iframe width="100%" height="166" scrolling="no" frameborder="no" allow="autoplay" src="https://w.soundcloud.com/player/?url=https%3A//api.soundcloud.com/tracks/771984076&color=%23ff5500&auto_play=true&hide_related=false&show_comments=true&show_user=true&show_reposts=false&show_teaser=true"></iframe>' + "\n" +
                        '18. iframe/src="data:text/html;&Tab;base64&Tab;,PGJvZHkgb25sb2FkPWFsZXJ0KDEpPg=="'

                        )
    @pytest.mark.xss
    def test_xss_frontend_astatus(self):
        xssfrontend = XSS_Frontend(url, admin_id, authorization, contact_id)
        statuscode = xssfrontend.xss_edit_status(admin_user, admin_pass, xss_list, contact_number, driver_context[0])
        print("Main: Test4 Response:", statuscode)
        self.assertEqual(1, statuscode, "Test4: XSS threat found")

    @classmethod
    def tearDownClass(cls):
        driver_context[0].quit()

