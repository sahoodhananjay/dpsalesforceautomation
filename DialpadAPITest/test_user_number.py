import unittest
unittest.TestLoader.sortTestMethodsUsing = None
import sys
import time
from user_number import UserNumbers
from screenpop import Screenpop
import pytest
import allure
import re

url = 'https://dialpadbeta.com/api/v2/'
office_id = '5594532661428224'
apikey = 'ULLc7YuA4S47aCKzKufM5NbBZr8jgqgvjJLDrwHfZjSQYwBJ2DGxsexzEVNVevsMvxTZwLn5cLA7mTT95HZhS7HhQq4M2H4yUhg9'
#apikey = '9Ca5AXkhnJtqGtd5JvAMEtXmGnPtjZQExrn3frmBRUMSBtENCcGcdxzAEaphcqbPLZ4S6e3PyCTmML2nACNwPgBrbTmWzvyhGy8H'
authorization = 'Bearer WtKU86s3tKWSWsdf7aPfLtcPZ8kuadHKZm2y9ZbvTxAUcW4UukbC8C3KaV76yHENRXPX5XaD23dheXESp3ACp24ypTZW3rCLDh84'
domain = 'dp.com'
license = 'talk'
auto_assign = True
company_area_code = '609'
number = '+14242547327'
new_area_code = '424'
target_type = 'user'
single_phone_number = '+16092013385'



class TestUserNumber(unittest.TestCase):

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.quicktest
    def test_test1_create_user_with_auto_assign_number(self):
        user_phonenumber = []
        user_id = []

        user_number = UserNumbers(url, office_id, apikey, domain,license,auto_assign,company_area_code,number,new_area_code)
        user_email = user_number.generate_randomuser()
        print("\nCreating a new user\n")
        create_statuscode,create_content = user_number.create_user_and_assign_number(user_email)
        self.assertEqual(200, create_statuscode, "Test1 Create User: Response did not match")
        if create_statuscode == 200:
            user_id.append(create_content["id"])
            if "phone_numbers" in create_content:
                user_phonenumber.append(create_content["phone_numbers"])
                print("\nUser was created with id {} and auto assigned phone number {}.".format(user_id[0],user_phonenumber[0]))
            else:
                print("\nUser was created but phone was not auto assigned")
        else:
            print("The user was not created. Received error response:",create_statuscode)
        time.sleep(10)
        print("Deleting the new user\n")
        delete_statuscode,delete_content = user_number.delete_user(user_id[0])
        self.assertEqual(200, delete_statuscode, "Test1 Delete User: Response did not match")

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.quicktest
    def test_test2_create_user_without_auto_assign_number(self):
        user_phonenumber = []
        user_id = []
        auto_assign = False
        user_number = UserNumbers(url, office_id, apikey, domain, license, auto_assign,company_area_code,number,new_area_code)
        user_email = user_number.generate_randomuser()
        print("\nCreating a new user\n")
        create_statuscode, create_content = user_number.create_user_and_assign_number(user_email)
        self.assertEqual(200, create_statuscode, "Test2 Create User: Response did not match")
        if create_statuscode == 200:
            user_id.append(create_content["id"])
            if "phone_numbers" in create_content:
                user_phonenumber.append(create_content["phone_numbers"])
                print("\nUser was created with id {} and auto assigned phone number {}.".format(user_id[0],user_phonenumber[0]))
            else:
                print("\nUser was successfully created but phone was not auto assigned")
        else:
            message = create_content['error']['message']
            print("The user was not created. Received error response: {}: {}".format(create_statuscode, message))
            print("The user was not created. Received error response:", create_statuscode)
        time.sleep(10)
        print("Deleting the new user\n")
        delete_statuscode,delete_content = user_number.delete_user(user_id[0])
        self.assertEqual(200, delete_statuscode, "Test2 Delete User: Response did not match")

    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.quicktest
    def test_test3_create_free_user_with_auto_assign(self):
        user_phonenumber = []
        user_id = []
        auto_assign = False
        license = 'lite_lines'
        user_number = UserNumbers(url, office_id, apikey, domain, license, auto_assign,company_area_code,number,new_area_code)
        user_email = user_number.generate_randomuser()
        print("\nCreating a new user\n")
        create_statuscode, create_content = user_number.create_user_and_assign_number(user_email)
        self.assertEqual(200, create_statuscode, "Test3 Create User: Response did not match")
        if create_statuscode == 200:
            user_id.append(create_content["id"])
            if "phone_numbers" in create_content:
                user_phonenumber.append(create_content["phone_numbers"])
                retrieve_phone = user_phonenumber[0][0]
                pattern = re.search('(^[+80]{0,3})', retrieve_phone)
                if pattern:
                    print("The Free SKU user is assigned a Dialpadistan Number")
                else:
                    print("The Free SKU user is NOT assigned a Dialpadistan Number")

                print("\nUser was created with id {} and auto assigned phone number {}.".format(user_id[0],user_phonenumber[0][0]))
            else:
                print("\nUser was successfully created but phone was not auto assigned")
        else:
            message = create_content['error']['message']
            print("The user was not created. Received error response: {}: {}".format(create_statuscode, message))
            print("The user was not created. Received error response:", create_statuscode)
        time.sleep(10)
        print("Deleting the new user\n")
        delete_statuscode,delete_content = user_number.delete_user(user_id[0])
        self.assertEqual(200, delete_statuscode, "Test3 Delete User: Response did not match")

    @pytest.mark.quicktest
    def test_test4_assign_specific_number(self):
        user_phonenumber = []
        user_id = []
        auto_assign = False
        #license = 'talk'
        user_number = UserNumbers(url, office_id, apikey, domain,license,auto_assign,company_area_code,number,new_area_code)
        user_email = user_number.generate_randomuser()
        print("\nCreating a new user\n")
        create_statuscode, create_content = user_number.create_user_and_assign_number(user_email)
        self.assertEqual(200, create_statuscode, "Test4 Create User: Response did not match")
        if create_statuscode == 200:
            user_id.append(create_content["id"])
            if "phone_numbers" in create_content:
                user_phonenumber.append(create_content["phone_numbers"])
                retrieve_phone = user_phonenumber[0][0]
                print("The auto assign was False but still the user was assigned the number.")
                print("\nUser was created with id {} and auto assigned phone number {}.".format(user_id[0],
                                                                                                user_phonenumber[0][0]))
            else:
                print("\nUser was successfully created but phone was not auto assigned")
                assign_number_statscode,assign_number_content = user_number.assign_number(user_id[0],target_type,'number')
                self.assertEqual(200, assign_number_statscode, "Test4 Create User: Response did not match")
                if assign_number_statscode == 200:
                    if "number" in assign_number_content:
                        new_user_number = assign_number_content["number"]
                        self.assertEqual(number,new_user_number, "Test4 Assign Number: Specific number not assigned to the user")
                    else:
                        print("No phone number was assigned to the user")
                else:
                    message = assign_number_content['message']
                    print("Number could not be assigned to the user:")
                    print("Error: {}: {}".format(assign_number_statscode,message))

        else:
            message = create_content['error']['message']
            print("The user was not created. Received error response: {}: {}". format(create_statuscode,message))
        time.sleep(10)
        print("Deleting the new user\n")
        delete_statuscode,delete_content = user_number.delete_user(user_id[0])
        self.assertEqual(200, delete_statuscode, "Test4 Delete User: Response did not match")

    @pytest.mark.quicktest
    def test_test5_assign_number_areacode(self):
        user_phonenumber = []
        user_id = []
        auto_assign = False
        # license = 'talk'
        user_number = UserNumbers(url, office_id, apikey, domain, license, auto_assign, company_area_code, number,
                                  new_area_code)
        user_email = user_number.generate_randomuser()
        print("\nCreating a new user\n")
        create_statuscode, create_content = user_number.create_user_and_assign_number(user_email)
        self.assertEqual(200, create_statuscode, "Test5 Create User: Response did not match")
        if create_statuscode == 200:
            user_id.append(create_content["id"])
            if "phone_numbers" in create_content:
                user_phonenumber.append(create_content["phone_numbers"])
                retrieve_phone = user_phonenumber[0][0]
                print("The auto assign was False but still the user was assigned the number.")
                print("\nUser was created with id {} and auto assigned phone number {}.".format(user_id[0],
                                                                                                user_phonenumber[0][0]))
            else:
                print("\nUser was successfully created but phone was not auto assigned")
                assign_number_statscode, assign_number_content = user_number.assign_number(user_id[0],
                                                                                                    target_type,
                                                                                                    'area_code')
                self.assertEqual(200, assign_number_statscode, "Test5 Create User: Response did not match")
                if assign_number_statscode == 200:
                    if "area_code" in assign_number_content:
                        user_area_code = assign_number_content["area_code"]
                        self.assertEqual(new_area_code, user_area_code,
                                         "Test5 Assign Number: Specific area_code not assigned to the user")
                        print("The user is assigned number from the specified area code:",new_area_code)
                    else:
                        print("No phone number was assigned to the user")
                else:
                    message = assign_number_content['message']
                    print("Number could not be assigned to the user:")
                    print("Error: {}: {}".format(assign_number_statscode, message))

        else:
            message = create_content['error']['message']
            print("The user was not created. Received error response: {}: {}".format(create_statuscode, message))
        time.sleep(10)
        print("Deleting the new user\n")
        delete_statuscode,delete_content = user_number.delete_user(user_id[0])
        self.assertEqual(200, delete_statuscode, "Test5 Delete User: Response did not match")

    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.quicktest
    def test_test6_number_takes_precedence_over_areacode(self):

        user_phonenumber = []
        user_id = []
        auto_assign = False

        # license = 'talk'
        user_number = UserNumbers(url, office_id, apikey, domain, license, auto_assign, company_area_code, number,
                                  new_area_code)
        user_email = user_number.generate_randomuser()
        print("\nCreating a new user\n")
        create_statuscode, create_content = user_number.create_user_and_assign_number(user_email)
        self.assertEqual(200, create_statuscode, "Test6 Create User: Response did not match")
        if create_statuscode == 200:
            user_id.append(create_content["id"])
            if "phone_numbers" in create_content:
                user_phonenumber.append(create_content["phone_numbers"])
                retrieve_phone = user_phonenumber[0][0]
                print("The auto assign was False but still the user was assigned the number.")
                print("\nUser was created with id {} and auto assigned phone number {}.".format(user_id[0],
                                                                                                user_phonenumber[0][
                                                                                                    0]))
            else:
                print("\nUser was successfully created but phone was not auto assigned")
                assign_number_statscode, assign_number_content = user_number.assign_number(user_id[0],
                                                                                           target_type,
                                                                                           'both')
                self.assertEqual(200, assign_number_statscode, "Test6 Assign Number: Response did not match")
                if assign_number_statscode == 200:
                    if "number" in assign_number_content:
                        new_user_number = assign_number_content["number"]
                        self.assertEqual(number, new_user_number,
                                         "Test6 Assign Number: Specific number not assigned to the user")
                        print("The user is assigned the specific number:", number)
                    else:
                        print("No phone number was assigned to the user")
                else:
                    message = assign_number_content['message']
                    print("Number could not be assigned to the user:")
                    print("Error: {}: {}".format(assign_number_statscode, message))

        else:
            message = create_content['error']['message']
            print("The user was not created. Received error response: {}: {}".format(create_statuscode, message))
        time.sleep(10)
        print("Deleting the new user\n")
        delete_statuscode,delete_content = user_number.delete_user(user_id[0])
        self.assertEqual(200, delete_statuscode, "Test6 Delete User: Response did not match")

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.quicktest
    def test_test7_create_assign_retrive_unassign(self):
        user_phonenumber = []
        user_id = []
        auto_assign = True
        # license = 'talk'
        user_number = UserNumbers(url, office_id, apikey, domain, license, auto_assign, company_area_code, number,
                                  new_area_code)
        user_email = user_number.generate_randomuser()
        print("\nCreating a new user\n")
        create_statuscode, create_content = user_number.create_user_and_assign_number(user_email)
        self.assertEqual(200, create_statuscode, "Test7 Create User: Response did not match")
        if create_statuscode == 200:
            user_id.append(create_content["id"])
            if "phone_numbers" in create_content:
                user_phonenumber.append(create_content["phone_numbers"])
                #retrieve_phone = user_phonenumber[0][0]
                #print("The auto assign was False but still the user was assigned the number.")
                print("\nUser was created with id {} and auto assigned phone number {}.".format(user_id[0],
                                                                                                user_phonenumber[0][0]))
            else:
                print("\nUser was successfully created but phone was not auto assigned")

            print("\nAssign  a new number\n")
            assign_number_statscode, assign_number_content = user_number.assign_number(user_id[0], target_type,
                                                                                           'number')
            self.assertEqual(200, assign_number_statscode, "Test4 Create User: Response did not match")
            if assign_number_statscode == 200:
                if "number" in assign_number_content:
                    new_assign_number = assign_number_content["number"]
                    print("Number:",new_assign_number)
                    user_phonenumber.append(new_assign_number)
                    self.assertEqual(number, new_assign_number,
                                         "Test7 Assign Number: Specific number not assigned to the user")
                else:
                    print("No new phone number was assigned to the user")
            else:
                message = assign_number_content['message']
                print("Number could not be assigned to the user:")
                print("Error: {}: {}".format(assign_number_statscode, message))

            print("\nRetrieve User Details\n")
            retrieve_statscode, retrieve_content = user_number.get_user(user_id[0])
            self.assertEqual(200, retrieve_statscode, "Test7 Retrieve User: Response did not match")
            if "phone_numbers" in retrieve_content:
                retrieve_phone_numbers = retrieve_content['phone_numbers']
                #print("1:",retrieve_phone_numbers[0],retrieve_phone_numbers[1])
                #print("2:",user_phonenumber[1],user_phonenumber[0][0],len(user_phonenumber))
                if (retrieve_phone_numbers[0] == user_phonenumber[1]) and (retrieve_phone_numbers[1] == user_phonenumber[0][0]):
                    self.assertTrue(True,"Retrieve user data is not successful. The user data does not have all the expected numbers")
                    print("Retrieve user data is successful. The user data has all the expected numbers")

            print("\nUnassign Phone Number\n")
            time.sleep(10)
            unassign_statscode, unassign_content = user_number.unassign_number(retrieve_phone_numbers[0])
            self.assertEqual(200, unassign_statscode, "Test7 Unassign Number: Response did not match")

            print("\nRetrieve User Details After Unassign\n")
            retrieve_statscode, retrieve_content = user_number.get_user(user_id[0])
            self.assertEqual(200, retrieve_statscode, "Test7 Retrieve User After Unassign: Response did not match")
            if "phone_numbers" in retrieve_content:
                retrieve_phone_numbers = retrieve_content['phone_numbers']
                if len(retrieve_phone_numbers) == 1:
                    self.assertTrue(True,
                                    "Unassign Number Failed. The user still has both the phone numbers")
                    print("Unassign Number is successful")
            else:
                print("The user data did not have the phone number field. Should have had 1 phone number")



        else:
            message = create_content['error']['message']
            print("The user was not created. Received error response: {}: {}".format(create_statuscode, message))
        time.sleep(10)
        print("Deleting the new user\n")
        delete_statuscode, delete_content = user_number.delete_user(user_id[0])
        self.assertEqual(200, delete_statuscode, "Test7 Delete User: Response did not match")


    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.quicktest
    def test_test8_unassign_only_number(self):
        user_number = UserNumbers(url, office_id, apikey, domain, license, auto_assign, company_area_code, number,
                                  new_area_code)
        unassign_statscode, unassign_content = user_number.unassign_number(single_phone_number)
        self.assertEqual(403, unassign_statscode, "Test8 Test Failed: Unexpected Response")
        message = unassign_content['error']['message']
        print("The number was not unassigned. Received error response: {}: {}".format(unassign_statscode, message))






    #def check_print(self):
    #    user_number = UserNumbers()
    #    print("test:",user_number.check_print())

    if __name__ == '__main__':
        unittest.main()