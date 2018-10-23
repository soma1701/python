# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 18:10:19 2018

@author: gugulothu.pandu
"""
import configparser
import mysql.connector
import queries
from jira.exceptions import JIRAError

section_name = 'DB_CREDENTIALS'
assignee_result ={}
components_result = {}
users_map = {}
users = None

def readProperty(section, property_name):
    config = configparser.ConfigParser()
    config.read('Config.ini')
    return config.get(section, property_name);

def readFile(file_name):
    with open(file_name) as f:
        return f.read()
    
def readProperties(section):
    config = configparser.ConfigParser()
    config.read('Config.ini')
    return config[section];    

def getQueryResultSet(query):
   try:
      connection = getConnection()
      cursor = connection.cursor()
      cursor.execute(query)
      bug_ids = []
      for (big_id,) in cursor:
          bug_ids.append(big_id)
      return bug_ids
   except Exception as e:
      print('error occured while executing query'.format(e))
   finally: 
      cursor.close()
      connection.close()
      
def get_users():
    try:
        connection = getConnection()
        cursor = connection.cursor()
        cursor.execute(queries.get_assigne_name)      
        for (user_id,login_name) in cursor:
            assignee_result[user_id]  = login_name
        return assignee_result
    except Exception as e:
            print('exception occured while fetching assignee'.format(e))
    finally:
            cursor.close()
            connection.close()
            
def get_project_users():
    try:
        connection = getConnection()
        cursor = connection.cursor()
        cursor.execute(queries.get_project_users)      
        for (user_id,login_name) in cursor:
            assignee_result[user_id]  = login_name
        return assignee_result
    except Exception as e:
            print('exception occured while fetching assignee'.format(e))
    finally:
            cursor.close()
            connection.close()
            
def getComponents():
    try:
        connection = getConnection()
        cursor = connection.cursor()
        cursor.execute(queries.fetch_components)      
        for (component_id,component_name) in cursor:
            components_result[component_id]  = component_name
        return components_result
    except Exception as e:
            print('exception occured while fetching components'.format(e))
    finally:
            cursor.close()
            connection.close()
     
def getQueryResult(query):
   try:
      connection = getConnection()
      cursor = connection.cursor()
      cursor.execute(query)
      for (result,) in cursor:
          return result
   except Exception as e:
      print('error occured while executing query'.format(e))
   finally: 
      cursor.close()
      connection.close()    
      
def getQueryResultWith(query,param):
   try:
      connection = getConnection()
      cursor = connection.cursor()
      cursor.execute(query,(param,))
      for result in cursor:
          return result
   except Exception as e:
      print('error occured while executing query'.format(e))
   finally: 
      cursor.close()
      connection.close()         
      
def getResultSetWith(query,param):
   try:
      connection = getConnection()
      cursor = connection.cursor()
      cursor.execute(query,(param,))
      records  = []
      for result in cursor:
          records.append(result)
      return records
   except Exception as e:
      print('error occured while executing query'.format(e))
   finally: 
      cursor.close()
      connection.close()              
      
def getConnection():
    db_details = readProperties(section_name);
    db_username = db_details.get('USERNAME')
    db_password = db_details.get('PASSWORD')
    db_host = db_details.get('HOST')
    db_database = db_details.get('DATABASE')
    return mysql.connector.connect(user=db_username, password=db_password, host=db_host, database=db_database) 

def formattime(time):
    # format to workweeks, workdays, hours and minutes
    # a workweek is 5 days, a workday is 8 hours
    hours, minutes = divmod(time, 60)
    days, hours = divmod(hours, 8)  # work days
    weeks, days = divmod(days, 5)   # work weeks
    components = [str(v) + l for l, v in zip('wdhm', (weeks, days, hours, minutes)) if v]
    return ''.join(components) or '0m' or 'NoneType'     

def get_user(user_id,jira):   
    try:
        global users
        if(users is None):
            users_map,users = get_existing_users(jira)
        default_users = get_default_users()
        user = users[user_id]      
        if(user is None):
            user_id = default_users[0]
        else:
            user_id = user if users_map[user] == 'Y' else default_users[0]
    except Exception as e:
        user_id = default_users[0]
    return user_id

def get_existing_users(jira):
    users = get_project_users()
    for user in users:
        try:
            user = jira.user(id=users[user])
            users_map[users[user]] = 'Y'
        except JIRAError as e:
            #print("user:"+users[user]+"doesn't exists in jira")
            users_map[users[user]] = 'N'
    return users_map, users
    
def get_default_users():
    return readProperty("DEFAULT_USERS", "Assignee"),readProperty("DEFAULT_USERS", "Reporter"),readProperty("DEFAULT_USERS", "test_engineer")
            
