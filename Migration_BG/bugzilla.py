
import utilities
import queries
from bugzilla_record import bug_record
from jira_class import jira_record
from comment import process_comments
from attachment import process_attachment
import jira_client
import pre_hooks
import pandas as pd
import json as simplejson
from decimal import Decimal
from datetime import date,datetime

users = {}
components_result = {}
users_map = {}
default_users = ()
default_values = ()
transition_ids = {}
transitions_value = {}
exception = {}
create_status = ""
update_status = ""
comment_status = ""
jira_issue = ""
type = {}

def process_columns(record,jira,df,file,j):
    global jira_issue,exception,type,create_status,update_status,comment_status,attachment_status
    project_name = utilities.readProperty("Projects", "Destination_Project")
    #assignee  = utilities.getQueryResult(queries.assignee_name)
    #project_name = utilities.getQueryResultWith(queries.project_name)
    summary = record.summary
    #component = utilities.getQueryResultWith(queries.component_name,record.component_id)
    jira_obj = jira_record(summary)
    jira_obj.assignee = utilities.get_user(record.assigned_to,jira)
    jira_obj.components = components_result[record.component_id]
    #jira_obj.user_name = utilities.assignee_result[record.assigned_to]
    jira_obj.bug_severity = jira_obj.process_severity(record.bug_severity,default_values[0])
    jira_obj.status = record.bug_status
    jira_obj.priority = jira_obj.process_priority(record.priority,default_values[1])
    jira_obj.creation_ts = record.creation_ts.isoformat()
    jira_obj.product_id = record.product_id
    #jira_obj.component_id = record.component_id
    jira_obj.resolution = record.resolution
         
    jira_obj.phase_of_detection = jira_obj.process_record_validation(record.cf_client_phase,default_values[2])
    jira_obj.fix_version =   jira_obj.process_record_validation(record.cf_fixes_available,default_values[3])   
    jira_obj.test_engineer = default_users[2]
    jira_obj.issue_type = jira_obj.process_issue_type(record.cf_type,default_values[4])
    jira_obj.test_caseid = record.cf_testcaseid        
    jira_obj.build = record.cf_build
    if(record.estimated_time!=None and record.estimated_time!=0.0):
        jira_obj.estimated_time = utilities.formattime(record.estimated_time*60)
        #since estimated_time is in hours and arguments(arguments for formattime) is in minutes so multiplied by 60
    else:
        jira_obj.estimated_time = record.estimated_time
    if(record.remaining_time != None and record.remaining_time!=0.0):
        jira_obj.remaining_estimate = utilities.formattime(record.remaining_time*60)
        #since estimated_time is in hours and arguments(arguments for formattime) is in minutes so multiplied by 60
    else:
        jira_obj.remaining_estimate = record.remaining_time
    if(record.deadline!=None):    
        jira_obj.deadline =datetime.strptime(record.deadline, '%Y-%m-%d %H:%M:%S.%f').date()
        
    jira_obj.browser = jira_obj.process_browser(record.cf_browser,default_values[5])     
    jira_obj.os = jira_obj.process_os(record.op_sys,default_values[6])
    jira_obj.estimated_time = str(jira_obj.estimated_time)
    jira_obj.remaining_estimate = str(jira_obj.remaining_estimate)
    #converting remaining and estimated time to str because it is showing error 'Object of type 'Decimal' is not JSON serializable' 
    issue_dict = {
          "project": {"key": project_name},
          "summary": summary,
          "description": summary,
          "issuetype": {"name": jira_obj.issue_type},
          "customfield_10513": jira_obj.test_caseid,
          "components": [{"name": jira_obj.components}],
          "customfield_10503" : {"value": jira_obj.phase_of_detection},
          "versions": [{"name": "Wave 1"}],
          "priority":{"name": jira_obj.priority},
          "customfield_10300" : {"value": jira_obj.bug_severity},
          "customfield_10601": {"value": default_users[0]}  
            }
    update_issue = {
            #"aggregatetimeoriginalestimate" : {"value": jira_obj.estimated_time},
            #"timeestimate" : jira_obj.remaining_estimate,
            #"duedate" :{"name" : jira_obj.due_date}
            #"assignee" : {"name" : jira_obj.assignee }
            #"customfield_1020" : {"name" : jira_obj.browser},
            #"customfield_10601" : {"name" : jira_obj.test_engineer },
            #"customfield_16233" : {"name" : jira_obj.status},
            #"resolution" : {"name" : jira_obj.resolution}
            #"customfield_10512": {"value" : jira_obj.build}
            "timeoriginalestimate" : {"value" : jira_obj.estimated_time},
            #"duedate" :{"value" : jira_obj.due_date}
            }
    #new_issue = jira.create_issue(fields=issue_dict)
    new_issue = jira.issue('TPFWD-2')
    #transitions = jira.transitions(new_issue)
    #new_issue.update(update)
    #description = process_comments(record.bug_id,jira,new_issue)
    print("fields",new_issue.fields)
    #new_issue,c_status = jira_obj.issue_create(record.bug_id,i,jira,issue_dict,df)
    #if(c_status=='Y'):
    #j=+1
    status = jira_obj.issue_update(new_issue,update_issue,j,df,record.bug_id)
    print("update status",status)
    j+=1
    #status,description = jira_obj.comments_status(record.bug_id,jira,new_issue,j,df)
    #j+=1
    #print("comment status n description",status,description)
    return j
    
def getColumns():
    columns = utilities.readProperty('LOG_ATTRIBUTES','COLUMNS')
    if columns is not None:
        columns = columns.split(',')
    return columns

file = open('logs.csv','a')
columns = getColumns()
df = pd.DataFrame(columns= columns[0:])
if __name__ == "__main__":
    jira = jira_client.getJiraClient()
    get_project = queries.get_project
    get_bugCount = queries.get_bugCount
    default_users = utilities.get_default_users()
    default_values = pre_hooks.get_default_values()
    #users = utilities.get_users() 
    #users_map,users = pre_hooks.get_existing_users(jira)
    components_result = utilities.getComponents()
    project_name = utilities.getQueryResult(get_project)
    bug_count = utilities.getQueryResult(get_bugCount)
    print(bug_count)
    get_bugIds = queries.get_bugIds
    bug_ids = utilities.getQueryResultSet(get_bugIds)
    i = 1
    j = 0
    for bug in bug_ids:
        try:
          connection = utilities.getConnection()
          cursor = connection.cursor()
          cursor.execute(queries.bug_details,(bug,))
          for bug_details in cursor:
              record = bug_record(bug_details[0])
              record.create_record(bug_details)
              print(record.bug_id)
              print(record.summary)
              j = process_columns(record,jira,df,file,j)
        except Exception as e:
            print('error occured while executing query {}'.format(e))
            break
        finally:
            cursor.close()
            connection.close()
        if(i>=2):
            break
        i+=1

#file = open('logs.csv','a')
#file.write('#Project Name:{} \n'.format(project_name))
#file.write('#Total Bugs count:{}\n'.format(bug_count))            
#columns = getColumns()
#df = [(1,2,'abc'),(3,4,'xyz'),(5,6,'wxy')]
#df = pd.DataFrame(data =df, columns= columns[0:3])
df.to_csv(file)
file.close()
#print(df)
