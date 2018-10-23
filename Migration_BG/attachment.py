# -*- coding: utf-8 -*-
import ssl
import queries
import urllib
import utilities
from io import StringIO

cookie_file = 'cookie.txt'

def get_attachment(attach_id):
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    attach_url = "https://bugzilla.metricstream.com/bugzilla/attachment.cgi?id="+attach_id
    request = urllib.request.Request(attach_url)
    request.add_header("Accept-Encoding", "gzip, deflate, br")
    request.add_header("User-Agent", "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")
    cookie = get_cookie(cookie_file)
    request.add_header("Cookie", cookie)
    try:
        response = urllib.request.urlopen(request,context=gcontext)
        attach_type = response.getheader('Content-disposition')
        if attach_type is None:
            cookie = get_authentication()
            request.add_header("Cookie", cookie)
            response = urllib.request.urlopen(request,context=gcontext)
            attach_type = response.getheader('Content-disposition')
        filename = attach_type.split(';')[1].split('=')[1]
        content = response.read()
        #content = StringIO(content.decode('utf-8'))
        return content,filename.strip("\"")
    except Exception as e:
        print(e)
  


def process_attachment(bug_id):
    records = utilities.getResultSetWith(queries.get_attachs,bug_id)
    attachments = {}
    for record in records:
        content,filename = get_attachment(record[0])
        attach = StringIO(content.decode('utf-8'))
        attachments[filename] = attach
        #attach.close()
    return attachments

        

def get_authentication():
    gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    login_url = "https://bugzilla.metricstream.com/bugzilla/index.cgi"
    auth_data = urllib.parse.urlencode({"Bugzilla_login":"gugulothu.pandu","Bugzilla_password":"rang123*","GoAheadAndLogIn":"Log+in"}).encode()
    request = urllib.request.Request(login_url, data = auth_data )
    request.add_header("Accept-Encoding", "gzip, deflate, br")
    request.add_header("User-Agent", "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")
 
    try:
        response = urllib.request.urlopen(request,context=gcontext)
        cookie = response.getheader('Set-Cookie')
        with open(cookie_file, 'w') as file:
            file.write(cookie)
        return cookie
    except urllib.error.HTTPError as e:
        print(e)
        return None
    
def get_cookie(file):
    try:
        with open(file, 'r') as file:
            cookie = file.read()
            if cookie is not None:
                return cookie
            else:
                return get_authentication()
    except FileNotFoundError:
        return get_authentication()