# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 15:19:29 2018

@author: amrit.patel
"""

from jira.client import GreenHopper
import utilities

section_name = 'JIRA_CONNECTION_DETAILS'
#########################JIRA Connection################
    
con_credentials = utilities.readProperties(section_name);
JIRA_SERVER = con_credentials.get('JIRA_SERVER')
CONSUMER_KEY = con_credentials.get('CONSUMER_KEY')
RSA_KEY = utilities.readFile('rsa.pem')


def getJiraClient():
    jira=GreenHopper(options={'server': JIRA_SERVER}, oauth={
               'access_token': con_credentials.get('ACCESS_TOKEN'),
               'access_token_secret': con_credentials.get('ACCESS_TOKEN_SECRET'),
               'consumer_key': CONSUMER_KEY,
               'key_cert': RSA_KEY
               })
    return jira


#comment = jira.add_comment('TEST-3718', 'new comment from python API')

# upload file from `/some/path/attachment.txt`
#jira.add_attachment(issue=issue, attachment='attachments.txt', filename='kishlai.txt')
