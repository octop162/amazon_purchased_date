from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

q = 'Amazon.co.jpでのご注文'
email = 'test@gmail.com'

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
creds = None

# 認証
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())


# 注文取り出し 
service = build('gmail', 'v1', credentials=creds)
results = service.users().messages().list(userId=email, q=q).execute()
messages = results.get('messages', [])

for message in messages:
    message_id = message.get('id')
    mail = service.users().messages().get(userId=email, id=message_id, format='minimal').execute()
    print(mail.get('internalDate'))