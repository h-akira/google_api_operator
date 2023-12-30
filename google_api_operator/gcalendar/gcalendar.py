#!/usr/bin/env python3
SCOPES = ['https://www.googleapis.com/auth/calendar']

def sample():
  import sys
  import os
  sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
  from authentication import get_service
  import datetime
  import argparse
  parser = argparse.ArgumentParser(description="""\
イベントを10件取得する．
""")
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-t", "--token", metavar="Path", default="token.json", help="token.json（存在しない場合は生成される）")
  parser.add_argument("-c", "--credentials", metavar="Path", default="credentials.json", help="credentials.json（client_secret_hogehoge.json）")
  options = parser.parse_args()
  N=10
  service = get_service(SCOPES, options.credentials, options.token, "calendar", "v3")
# Call the Calendar API
  now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
  print('Getting the upcoming 10 events')
  events_result = service.events().list(calendarId='primary', timeMin=now,maxResults=N, singleEvents=True,orderBy='startTime').execute()
  events = events_result.get('items', [])
  if not events:
    print('No upcoming events found.')
    return

  # Prints the start and name of the next 10 events
  for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])

if __name__ == '__main__':
  sample()
