# -*- coding: utf-8 -*-
import queries
import utilities
import attachment
import pre_hooks
from io import StringIO

class comment(object):
    
    def __init__(self,comment_id):
        self.comment_id = comment_id
        
    def add_date(self,date_time):
        self.c_date = date_time.isoformat()


def process_comments(bug_id,jira,issue):
    comments = utilities.getResultSetWith(queries.get_comments,bug_id)
    i = 0
    descr = None
    for com in comments:
            cmnt =  comment(com[0])
            cmnt.who = com[1]
            cmnt.add_date(com[2])
            cmnt.text = com[3]
            cmnt.is_private = com[4]
            cmnt.attach = com[5]
            if(i<1):
                descr = cmnt.text
                continue
            user_id = utilities.get_user(cmnt.who,jira)
            final_comment= "Originally commented by [~"+user_id+"] on "+ cmnt.c_date +".\n\n"+cmnt.text
            if(cmnt.attach is not None):
                result = utilities.getQueryResultWith(queries.get_attachs,cmnt.attach)
                if(result is not None):
                    content = utilities.getQueryResultWith(queries.attach_content,cmnt.attach)
                    #content, filename = attachment.get_attachment(cmnt.attach)
                    final_comment = "Originally attached by [~"+user_id+"] on "+ cmnt.c_date+".\n [^"+result[0]+"] \n"+result[1] +"\n\n"
                    jira.add_attachment(issue=issue, attachment=content[0], filename=result[0])
                else:
                    continue
            jira.add_comment(issue, final_comment)
            i+=1
    return descr
 
def get_user(user_id,jira):        
    try:
        users_map,users = pre_hooks.get_existing_users(jira)
        default_users = pre_hooks.get_default_users()
        user = users[user_id]      
        if(user is None):
            user_id = default_users[0]
        else:
            user_id = user if users_map[user] == 'Y' else default_users[0]
    except Exception as e:
        user_id = default_users[0]
    return user_id