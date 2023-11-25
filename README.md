# google_api_operator
## Overview
This library was created with the goal of organizing the functionality of google's api to make it easier to handle.

## Install
```
pip3 install git+ssh://git@github.com/h-akira/google_api_operator.git
```

## Usage
### Preparation
Prepare credential.json by referring to the following document.
The scope depends on the purpose.
- https://developers.google.com/gmail/api/quickstart/python
### Send Email
```
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
service = get_service(
  SCOPES, 
  "credentials.json",  # this is path, must exists
  "token.json",  # this is path, will be created if it does not exist
  "gmail",
  "v1",
  re_authenticate=True  # re-authenticate when RefreshError occurs
)
kwargs = {
  "service": service,
  "Subject": "sample subject",
  "Message": "sample message",
}
# as needed
kwargs["To"] = "hoge.0000@hoge.com"
kwargs["Cc"] = ["hoge.0011@hoge.com", "hoge.0012@hoge.com"]
kwargs["Bcc"] = ["hoge.0021@hoge.com", "hoge.0022@hoge.com"]
# send
send_mail(**kwargs)
```
### Get Email
comming soon
