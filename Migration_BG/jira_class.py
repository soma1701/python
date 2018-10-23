from comment import process_comments

class jira_record(object):
  
     def __init__(self, summary):
         self.summary = summary

     def process_record_validation(self,bugzila_value,default_value):
        if(bugzila_value!=None and bugzila_value!='---'):
            jira_value=bugzila_value
        else:
            jira_value=default_value
        
        return jira_value
    
     def process_issue_type(self,bugzila_record,default_value):
        if(bugzila_record=='Defect'):
            issue_type = 'Bug'
        elif(bugzila_record=='Change Request'):
            issue_type = 'Improvement'
        else:
            issue_type = default_value
        return issue_type
    
     def process_browser(self,bugzila_record,default_value):
         if(bugzila_record =='IE 8.0'):
             browser = 'IE 8.0'
         elif(bugzila_record == 'IE 9.0') :
             browser = 'IE 9.0'
         elif(bugzila_record == 'IE 10.0') :
             browser = 'IE 10'
         elif(bugzila_record == 'IE 11.0') :
             browser = 'IE 11'
         elif('IE' is bugzila_record):
             browser = 'Internet Explorer'
         elif('FireFox' is bugzila_record):
            browser = 'Mozila FireFox'
         elif('chrome' is bugzila_record):
            browser = 'Google Chrome'
         else :
            browser = default_value
         return browser
     
     def process_os(self,bugzila_record,default_value):
        if(bugzila_record=='None'):
            os ='Others'
        elif(bugzila_record=='All'):
            os = 'All'
        elif('Windows' is bugzila_record):
            os = 'Windows'
        elif('RHEL' is bugzila_record):
            os = 'Linux'
        elif('Sun' is bugzila_record):
            os = 'Solaris Sparc'
        else :
            os = default_value
        return os
    
     def process_severity(self,bugzila_record,default_value):
         if(bugzila_record=='major'):
             severity = 'Major'
         elif(bugzila_record == 'minor' or bugzila_record == 'normal'):
             severity = 'Normal'
         elif(bugzila_record == 'critical'):
             severity = 'Critical'
         elif(bugzila_record == 'blocker'):
             severity = 'Blocker'
         elif(bugzila_record == 'trivial'):
             severity = 'Trivial'
         else:
             severity = default_value
         return severity
     
     def process_priority(self,bugzila_record,default_value):
        if(bugzila_record=='P1'):
            priority = 'P1 - Critical'
        elif(bugzila_record == 'P2'):
            priority = 'P2 - High'
        elif(bugzila_record == 'P3'):
            priority = 'P3 - Normal'
        elif(bugzila_record == 'P4'):
            priority = 'P4 - Minority/Request'
        elif(bugzila_record == 'P5'):
            priority = 'P5 - Review Priority'
        else:
            priority = 'Medium'
        return priority
    
     def issue_create(self,bug_id,i,jira,fields,df):
         issue = ''
         try:
             issue = jira.create_issue(fields)
             status = "Y"
             data = [bug_id,issue,status,'','','created successfully without any exception']
         except Exception as e :
             create_exception = e.args
             status = "N"
             data = [bug_id,'',status,'','',create_exception]
         df.loc[i] = data
         return issue,status
     
     def issue_update(self,issue,fields,j,df,bug_id):
         try:
             issue.update(fields)
             status = "Y"
             data = [bug_id,issue,'',status,'','']
         except Exception as e :
             update_Exception = e.args
             status = "N"
             data = [bug_id,issue,'',status,'',update_Exception]
         df.loc[j] = data
         return status
     
     def comments_status(self,bug_id,jira,issue,j,df):
         try:
             description = process_comments(bug_id,jira,issue)
             status = "Y"
             data = [bug_id,issue,'','',status,'']
         except Exception as e :
             status = "N"
             comments_exception = e.args
             data = [bug_id,issue,'','',status,comments_exception]
         df.loc[j] = data
         return description,status
     
    
    
    
    