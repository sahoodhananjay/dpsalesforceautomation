import unittest
unittest.TestLoader.sortTestMethodsUsing = None
import sys
import time
from SF_DCL_TASK_Mapping import DialpadCallLog_Task_Mapping
import pytest
import warnings
warnings.filterwarnings("ignore")

## Input test parameters

account = ["0012g00000GIzQLAA1","0012g00000XbMXnAAN"]
lead = ["00Q2g000001vSQpEAM","00QD10000051AjGMAU"]
contact = ["003D100000YHTUkIAP","0032g00000JZll3AAD"]
opportunity = ["0062g000006fMgPAAU","0062g000006AU2jAAG"]
case = ["500D10000071kl1IAA","500D10000076e1fIAA"]
client_id = "3MVG9lJB4lV8F4SjmARl5MZK9SAOilZcsIvqIcAi_dywh5X9wziXqwVfd0EI2GkJT5.MWvjEdpTJs6zpFvBYp"
client_secret = "B1D82F34744A98877E348E2BDF3FE61761C67997A616658F80779B3B95F2D12E"
username = "dsahoo@dialpad.com.dfs.qa"
password = "P@$$word654321"
sf_instance = "https://dialpad-qa-dfs--qasandbox.sandbox.my.salesforce.com"

class TestSF_DCL_TASK_Mapping(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Running SetUP")
        sf_connection = DialpadCallLog_Task_Mapping(account,lead,contact,opportunity,case,client_id,client_secret,username,password,sf_instance)

    @pytest.mark.quicktestnorun
    def test_test_getTaskDetails(self):
        whoid,whatid = DialpadCallLog_Task_Mapping.test_getTaskDetails(self,sf_instance)
        print("Test0 TASK: WHOID & WHATID:",whoid,whatid)

    @pytest.mark.quicktestnorun
    def test_test_getDCLDetails(self):
        taskid, parentid, relatedid = DialpadCallLog_Task_Mapping.test_getDCLDetails(self, sf_instance)
        print("Test0 DCL: TASKID, PARENTID & RELATEDID:", taskid, parentid, relatedid)

    @pytest.mark.quicktest
    def test_test1(self):
        ## Change parentid from null to Account and relatedid from null to Opportuntiy
        parentid = "0012g00000GIzQLAA1"      #Account
        relatedid = "0062g000006fMgPAAU"     #Opportunity
        result = DialpadCallLog_Task_Mapping.test_updated_dcl(self, sf_instance,parentid,relatedid)
        print("Test1:", result)
        if "Successfully" in result:
            soql_task = DialpadCallLog_Task_Mapping.soql_query_task(self, sf_instance)
            task_count = soql_task['totalSize']
            count = 0
            while count != task_count:
                whatid = soql_task['records'][count]['WhatId']
                if whatid in [parentid,relatedid]:
                    print("Task with RelateTo as {} was successfully created".format(whatid))
                else:
                    print("No Task with RelateTo as {} was created".format(whatid))
                count += 1
        else:
            pass

    @pytest.mark.quicktest
    def test_test2(self):
        ## Change parentid to Contact and relatedid to Case
        parentid = "003D100000YHTUkIAP"  # Contact
        relatedid = "500D10000071kl1IAA"  # Case
        result = DialpadCallLog_Task_Mapping.test_updated_dcl(self, sf_instance, parentid, relatedid)
        print("Test2:", result)
        if "Successfully" in result:
            soql_task = DialpadCallLog_Task_Mapping.soql_query_task(self, sf_instance)
            task_count = soql_task['totalSize']
            count = 0
            while count != task_count:
                whatid = soql_task['records'][count]['WhatId']
                whoid = soql_task['records'][count]['WhoId']
                if (whatid in [parentid,relatedid]) and (whoid in [parentid,relatedid]):
                    print("Task has both ParentID and RelateToID")
                else:
                    print("No Task with RelateTo as {} was created".format(whatid))
                count += 1
        else:
            pass