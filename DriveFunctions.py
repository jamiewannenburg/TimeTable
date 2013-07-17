import webbrowser;
import json
import httplib2
import pprint
import logging
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import Credentials

def build_service(credentials):
    ##### make drive service #####
    try:
        http = httplib2.Http()
        http = credentials.authorize(http)
        drive_service = build('drive', 'v2', http=http)
        return drive_service
    except FlowExchangeError:
        raise FlowExchangeError
	

def write_new_file(drive_service,title,description,filename):
    ##### Insert a file #####
    media_body = MediaFileUpload(filename, mimetype='text/csv', resumable=True)
    body = {
      'title': title,
      'description': description,
      'mimeType': 'text/csv'
    }
    drive_service.files().insert(body=body, media_body=media_body, convert=True).execute()

def update_file(file_id,drive_service,title,description,filename):
    file = drive_service.files().get(fileId=file_id).execute()
    # File's new metadata.
    file['title'] = title
    file['description'] = description
    file['mimeType'] = 'text/csv'
    # File's new content.
    media_body = MediaFileUpload(filename, mimetype='text/csv', resumable=True)
    # Send the request to the API.
    drive_service.files().update(fileId=file_id,body=file,newRevision=True,media_body=media_body,convert=True).execute()
	

def write_files_to_drive(drive_service,title,description,filename):
    ##### Search for a file #####
    query = "title = \'"+title+"\'"
    list_of_files = drive_service.files().list(q=query).execute()
    if list_of_files["items"] == []:
        write_new_file(drive_service,title,description,filename)
    else:
        for file in list_of_files["items"]:
            if file["labels"]["trashed"] == False:
                file_id = file["id"]
                # print file_id
        try:
            file_id
            update_file(file_id,drive_service,title,description,filename)
        except NameError:
            write_new_file(drive_service,title,description,filename)

def get_credentials():
    CLIENT_ID = "841081248455.apps.googleusercontent.com"
    CLIENT_SECRET = 'DHsKDxF-yg2Jb7DNCSn_Vx5O'
    OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
    REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

    flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)

    ##### get_credentials #####
    try:
		##### read from my_credentials #####
        try:
            file = open("data/my_credentials.json","r")
            credentials = Credentials.new_from_json(file.read())
            file.close
            drive_service = build_service(credentials)
            return credentials
        except IOError:
            ##### get authentication from the browser #####
            authorize_url = flow.step1_get_authorize_url()
            webbrowser.open(authorize_url)
            code = raw_input('Enter verification code: ').strip()
            credentials = flow.step2_exchange(code)
            return credentials
		
    except FlowExchangeError: # of iets, maar dalk iets anders
        try:
            ##### try refresh code #####
            file = open("data/my_credentials.json","r")
            my_credentials = json.load(file)
            code = my_credentials["refresh_token"]
            file.close
            credentials = flow.step2_exchange(code)
            return credentials
            
        except FlowExchangeError:
            ##### get authentication from the browser #####
            authorize_url = flow.step1_get_authorize_url()
            webbrowser.open(authorize_url)
            code = raw_input('Enter verification code: ').strip()
            credentials = flow.step2_exchange(code)
            return credentials
			
