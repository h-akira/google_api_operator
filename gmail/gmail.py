#!/usr/bin/env python3
import base64
from . import mail_class as mc
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def send_mail(service, To, From, Subject, Message):
  try:
    message = EmailMessage()
    message.set_content(Message)
    message["To"] = To
    message["From"] = From
    message["Subject"] = Subject

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message

def get_data(detail_point,data_list=list()):
  if detail_point.__class__ is list:
    iter = detail_point
  else:
    iter =  [detail_point]
  for d in iter:
    if d['body']['size']!=0:
      try:
        data_list.append(d['body']['data'])
      except:
        pass
    else:
      detail_point,data_list = get_data(d['parts'],data_list=data_list)
  return detail_point,data_list      

def get_mail_list(service,query,N,progress=False,known_ids=[],known_continue=False,div=False,cur=None):
  mail_list = mc.Mail_list()
  message_ids = service.users().messages().list(userId="me", maxResults=N, q=query).execute()
  if message_ids["resultSizeEstimate"] == 0:
    print("取得可能なメッセージはありません．")
  else:
    for i,message in enumerate(message_ids["messages"]):
      if progress:
        print("\r"+f'progress:{i+1}/{N}',end="")
      mail = mc.Mail()
      mail.id=message["id"]
      if mail.id in known_ids:
        mail_list.known_flag = True
        if known_continue:
          print(' 既知のメッセージのため飛ばします．')
          continue
        else:
          print(' 既知のメッセージに達したため取得を終了します．')
          break
      if cur!=None:
        sql = f"SELECT mail_id FROM mail WHERE mail_id='{mail.id}'"
        cur.execute(sql)
        row = cur.fetchone()
        if row != None:
          mail_list.known_flag = True
          if known_continue:
            print(' 既知のメッセージのため飛ばします．')
            continue
          else:
            print(' 既知のメッセージに達したため取得を終了します．')
            break
      
      detail = service.users().messages().get(userId="me", id=message["id"]).execute()
      for header in detail["payload"]["headers"]:
        # 日付、送信元、件名を取得する
        if header["name"] == "Date":
          mail.date = header["value"]
        elif header["name"] == "From":
          mail._from = header["value"]
        elif header["name"] == "To":
          mail._to = header["value"]
        elif header["name"] == "Subject":
          mail.subject = header["value"]

      _, data_list = get_data(detail["payload"],[])  # よくわからないけどデフォルト値で[]だと残るみたい
      if div:
        mail.html=[]
      for data in data_list:
        row = base64.urlsafe_b64decode(data).decode("UTF-8")
        if not (div and "<html>" in row and "</html>" in row):
          mail.body.append(base64.urlsafe_b64decode(data).decode("UTF-8"))
        else:
          mail.html.append(base64.urlsafe_b64decode(data).decode("UTF-8"))
      mail_list.append(mail)
    print("")
    if not mail_list.known_flag:
      print("既知のメッセージに達しませんでした．")
  return mail_list
