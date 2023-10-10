from __future__ import print_function

import os
import base64
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from info_copying import organizer
from deleting import deleting
from icecream import ic

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.labels',]

def get_label_id(creds, label_required: str):
    # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        result = service.users().labels().list(userId='me').execute()
        labels = result.get("labels", [])
        
        if not labels:
            print("No labels Found")
        else:
            for label in labels:
                if label['name'] == label_required: #Change label name. This is what I personaly needed
                    return label['id']
                
def get_attachment(messageId, attachmentId, creds):
    service = build('gmail', 'v1', credentials=creds)
    result = service.users().messages().attachments().get(
        userId='me', 
        messageId=messageId, 
        id= attachmentId
    ).execute()
    
    file_data = base64.urlsafe_b64decode(result.get('data').encode('UTF-8'))
    
    return file_data

def pdf_downloader_main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    fritz = None
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

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        fritz = get_label_id(creds, "Fritz")         
        result = service.users().messages().list(userId='me', labelIds=[fritz], q='is:unread').execute()
        
        msgsId = result.get('messages', [])
        
        if msgsId == []:
            print("No messages")
            return
        
        for msgId in msgsId:
            msgResult = service.users().messages().get(userId='me', id=msgId['id']).execute()
            payload = msgResult.get('payload')
            
            if 'parts' in payload:
                for part in payload['parts']:
                    filename = part['filename']
                    if filename == "":
                        continue
                    filename = filename.replace(' ', '_')
                    body = part['body']
                    if 'attachmentId' in body:
                        attachmentId = body['attachmentId']
                        attch = get_attachment(msgId, attachmentId, creds)

                        if not os.path.exists(f'./Download/{filename}'):
                            with open(f'./Download/{filename}', 'wb') as _f:
                                _f.write(attch)
                        else:
                            continue
                
            time.sleep(0.5)
            
        print('saved')

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

if __name__ == "__main__":
    pdf_downloader_main()
    if os.listdir('./Download') is not []:
        organizer()
        time.sleep(5)
        deleting()