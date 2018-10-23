# -*- coding: utf-8 -*-

cf_type = {}
class bug_record(object):
    
    def __init__(self, bug_id):
        self.bug_id = bug_id   
          
    def create_record(self,bug_details):
        self.assigned_to = bug_details[1]
        self.bug_severity = bug_details[3]
        self.bug_status = bug_details[4]
        self.creation_ts = bug_details[5]
        self.summary = bug_details[7]
        self.op_sys = bug_details[8]
        self.priority = bug_details[9]
        self.product_id = bug_details[10]
        self.reporter = bug_details[12]
        self.affect_version = bug_details[13]
        self.component_id = bug_details[14]
        self.resolution = bug_details[15]
        self.qa_contact = bug_details[17]
        self.cclist_accessible = bug_details[23]
        self.estimated_time = bug_details[24]
        self.remaining_time = bug_details[25]
        self.deadline = bug_details[26]
        self.cf_build = bug_details[28]
        self.cf_fixes_available = bug_details[31]
        self.cf_type = bug_details[33]
        self.cf_testcaseid = bug_details[35]
        self.cf_browser = bug_details[30]
        self.cf_client_phase = bug_details[52]
       
