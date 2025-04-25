import os
from requests.auth import HTTPBasicAuth
import requests
import json
from datetime import datetime, date, timedelta
import time
import re
from bs4 import BeautifulSoup
import datetime, calendar
import pandas as pd
import numpy as np
import csv
import itertools
import sys
import warnings
warnings.filterwarnings("ignore")

class DialpadCallLog_Task_Mapping:
    details = {}

    def __init__(self, account, lead, contact, opportunity, case, client_id, client_secret, username, password,sf_instance):
        self.account = account
        self.lead = lead
        self.contact = contact
        self.opportunity = opportunity
        self.case = case
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.sf_instance = sf_instance

        ## Salesforce Authentication: Get Token
        token_url = "https://test.salesforce.com/services/oauth2/token?grant_type=password&client_id="+ self.client_id + "&client_secret="+ self.client_secret + "&username=" + self.username +"&password="+ self.password
        token_response = requests.post(token_url, auth=HTTPBasicAuth(self.username, self.password))
        token_response_soup = BeautifulSoup(token_response.content, 'html5lib')
        token_response_content = token_response_soup.get_text()
        json_token_response_content = json.loads(token_response_soup.text)
        #print(json_content)
        DialpadCallLog_Task_Mapping.details['access_token'] = json_token_response_content['access_token']

        ## Create a new DCL object:
        dcl_url = self.sf_instance + "/services/data/v56.0/sobjects/Dialpad__Call_Log__c"
        body = {
            "Dialpad__ParentObjectId__c": None,
            "Dialpad__RelatedObjectIds__c": None,
            "Dialpad__Status__c": "Completed",
            "Dialpad__Subject__c": "DCL Task Mapping Automation",
            "Dialpad__Type__c": "Call",
            "Dialpad__TaskSubtype__c": "Call",
            "Dialpad__CallId__c": "0000001",
            "Dialpad__Salesforce_Task__c": True,
            "Dialpad__IsDialpadCallLog__c": True
        }
        #print("Token:",json_token_response_content['access_token'])
        dcl_url_response = requests.post(dcl_url, data=json.dumps(body), headers={"content-type": "application/json; charset=UTF-8",'Authorization': 'Bearer '+DialpadCallLog_Task_Mapping.details['access_token']})
        dcl_url_soup = BeautifulSoup(dcl_url_response.content, 'html5lib')
        dcl_url_content = dcl_url_soup.get_text()
        json_dcl_url_content = json.loads(dcl_url_soup.text)
        print("Create DCL Respons:",json_dcl_url_content)
        DialpadCallLog_Task_Mapping.details['dcl_id'] = json_dcl_url_content['id']

        ## Get Task id from the new DCL object:
        dcl_task_url = self.sf_instance + "/services/data/v56.0/query/?q=SELECT Dialpad__Linked_Task_ID__c FROM Dialpad__Call_Log__c WHERE Id = \'"+ DialpadCallLog_Task_Mapping.details['dcl_id']+"\'"
        #print("Request:",dcl_task_url)
        dcl_task_url_response = requests.get(dcl_task_url, data=json.dumps(body),
                                         headers={"content-type": "application/json; charset=UTF-8",'Authorization': 'Bearer ' + DialpadCallLog_Task_Mapping.details['access_token']})
        dcl_task_url_soup = BeautifulSoup(dcl_task_url_response.content, 'html5lib')
        dcl_task_url_response_content = dcl_task_url_soup.get_text()
        json_dcl_task_url_response_content = json.loads(dcl_task_url_soup.text)
        print("Get TASK ID From DCL:",json_dcl_task_url_response_content)
        if len(json_dcl_task_url_response_content['records'][0]['Dialpad__Linked_Task_ID__c']) == 0:
            print("**** ERROR: DCL Does Not Have TASK ID ****")
        else:
            DialpadCallLog_Task_Mapping.details['dcl_task_id'] = json_dcl_task_url_response_content['records'][0]['Dialpad__Linked_Task_ID__c']

    def test_getDCLDetails(self,sf_instance):
        ## Get DCL Details:
        dcl_url = sf_instance + "/services/data/v56.0/query/?q=SELECT Dialpad__Linked_Task_ID__c,Dialpad__ParentObjectId__c,Dialpad__RelatedObjectIds__c FROM Dialpad__Call_Log__c WHERE Id = \'" + DialpadCallLog_Task_Mapping.details['dcl_id'] + "\'"
        print("Request:", dcl_url)
        dcl_url_response = requests.get(dcl_url, headers={"content-type": "application/json; charset=UTF-8", 'Authorization': 'Bearer ' + DialpadCallLog_Task_Mapping.details['access_token']})
        dcl_url_soup = BeautifulSoup(dcl_url_response.content, 'html5lib')
        dcl_url_response_content = dcl_url_soup.get_text()
        json_dcl_url_response_content = json.loads(dcl_url_soup.text)
        print("Get ParentID & RelatedID From DCL:", json_dcl_url_response_content)
        taskid = json_dcl_url_response_content['records'][0]['Dialpad__Linked_Task_ID__c']
        parentid = json_dcl_url_response_content['records'][0]['Dialpad__ParentObjectId__c']
        relatedid = json_dcl_url_response_content['records'][0]['Dialpad__RelatedObjectIds__c']

        return taskid, parentid, relatedid

    def test_getTaskDetails(self,sf_instance):
        ## Get Task Details:
        task_url = sf_instance + "/services/data/v56.0/query/?q=SELECT WhatId,WhoId FROM Task WHERE Id = \'" + DialpadCallLog_Task_Mapping.details['dcl_task_id'] + "\'"
        #print("Request:", task_url)
        task_url_response = requests.get(task_url, headers={"content-type": "application/json; charset=UTF-8", 'Authorization': 'Bearer ' + DialpadCallLog_Task_Mapping.details['access_token']})
        task_url_soup = BeautifulSoup(task_url_response.content, 'html5lib')
        task_url_response_content = task_url_soup.get_text()
        json_task_url_response_content = json.loads(task_url_soup.text)
        print("Get WHOID & WHATID From TASK:",json_task_url_response_content)
        whatid = json_task_url_response_content['records'][0]['WhatId']
        whoid = json_task_url_response_content['records'][0]['WhoId']

        return whoid,whatid

    def test_updated_dcl(self,sf_instance,parentid,relatedid):
        ## Update DCL object:
        dcl_url = sf_instance + "/services/data/v56.0/sobjects/Dialpad__Call_Log__c/"+ DialpadCallLog_Task_Mapping.details['dcl_id']
        body = {
            "Dialpad__ParentObjectId__c": parentid,
            "Dialpad__RelatedObjectIds__c": relatedid
        }
        # print("Token:",json_token_response_content['access_token'])
        dcl_url_response = requests.patch(dcl_url, data=json.dumps(body), headers={"content-type": "application/json; charset=UTF-8", 'Authorization': 'Bearer ' + DialpadCallLog_Task_Mapping.details['access_token']})

        print("Update DCL Response Code:", dcl_url_response.status_code)
        if dcl_url_response.status_code != 204:
            return "Failed to update DCL"
        else:
            return "Successfully updated DCL"

    def soql_query_task(self,sf_instance):
        ## Get Task SOQL Query:
        soql_task_url = sf_instance + "/services/data/v56.0/query/?q=SELECT Id,WhatId,WhoId FROM Task WHERE Subject = \'DCL Task Mapping Automation\'"
        # print("Request:", task_url)
        soql_task_url_response = requests.get(soql_task_url, headers={"content-type": "application/json; charset=UTF-8", 'Authorization': 'Bearer ' +DialpadCallLog_Task_Mapping.details['access_token']})
        soql_task_url_soup = BeautifulSoup(soql_task_url_response.content, 'html5lib')
        soql_task_url_response_content = soql_task_url_soup.get_text()
        json_soql_task_url_response_content = json.loads(soql_task_url_soup.text)
        print("SOQL TASK Query Response:", json_soql_task_url_response_content)

        return json_soql_task_url_response_content




