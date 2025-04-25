# dpsalesforceautomation

This repository is a collection of automated test scripts tailored for Dialpad integration with Salesforce. The scripts are designed to capture edge cases and complex user scenarios that are difficult to test manually. The suite enhances test coverage, improves reliability, and ensures the stability of mission-critical workflows in Salesforce environments.


**Key Features:**

- Automated testing of edge cases and non-deterministic behavior
- Regression suite for critical Salesforce components
- Scalable and maintainable test architecture
- Integration-ready with CI/CD pipelines

**Dialpad Feature Test**
1. Blocked Numbers Public APIs
2. CallCenter Public APIs
3. Screenpop Public APIs
4. User number Public APIs
5. SQL Injection in Dialpad Webapp
6. XSS threat validation of Dialpad Webapp

Usage: pytest .\test_user_number.py -s -v -m quicktest

**Salesforce Features Test:**

1. Dialpad Call Logging:
   
Jira: https://dialpad.atlassian.net/browse/DP-98062

Usage: pytest .\test_SF_DCL_TASK_Mapping.py -s -v -m quicktest

DP-133459 was reported based on test scenarios captured in SF_DCL_TASK_Mapping
