#!/usr/bin/env python3
# Based on https://developers.google.com/sheets/api/quickstart/python?hl=ja

# Import
import sys
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.exceptions import RefreshError

def get_service(SCOPES, credentials_json, token_json, resource_name, api_version, if_RefreshError=False):
  # resource_name: gmail, sheets, etc.
  # api_version: v1, v4, etc.
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(token_json):
    if if_RefreshError:
      try:
        creds = Credentials.from_authorized_user_file(token_json, SCOPES)
      except RefreshError:
        os.remove(token_json)
        creds = Credentials.from_authorized_user_file(token_json, SCOPES)
    else:
      creds = Credentials.from_authorized_user_file(token_json, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        credentials_json, SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(token_json, 'w') as token:
      token.write(creds.to_json())

  try:
    service = build(resource_name, api_version, credentials=creds)
  except:
    print("Couldn't get service.")
    sys.exit()
  return service
