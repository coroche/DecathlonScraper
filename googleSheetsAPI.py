
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient import errors
from googleapiclient.discovery import build

def getScriptID():
    with open('scriptID.txt', 'r') as file:
        SCRIPT_ID = file.read().rstrip()
    return SCRIPT_ID

def login():
    creds = None
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def buildService(creds):
    try:
        service = build('script', 'v1', credentials=creds)
    except errors.HttpError as error:
        print(error.content)
    return service
 
def removeWatch(SCRIPT_ID, service, email, URL):
    request = {"function": 'removeWatch',
                "parameters": [email, URL],
                "devMode": True}
    try:
        service.scripts().run(body=request, scriptId=SCRIPT_ID).execute()
    except errors.HttpError as error:
        print(error.content)

def getActiveTrackers(SCRIPT_ID, service):
    request = {"function": 'getActiveTrackers',
                "parameters": [],
                "devMode": True}
    try:
        response = service.scripts().run(body=request, scriptId=SCRIPT_ID).execute()
        return response['response']['result']
    except errors.HttpError as error:
        print(error.content)

