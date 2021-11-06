from django.test import TestCase
import requests
import json

# Create your tests here.

#Test 1 - Create a new user

url = "http://127.0.0.1:8000/user"

payload = json.dumps({
  "usr_nickname": "PCjr",
  "usr_email": "jkfdsahkjfhksdjhkf",
  "usr_doc": 8801255830,
  "usr_pwd": "Matt1!123",
  "usr_credate": "2021-11-05",
  "login": 0
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

#Test 2 - Login with user

url = "http://127.0.0.1:8000/login"

payload = json.dumps({
  "usr_doc": 8801255830,
  "usr_pwd": "Matt1!123"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

#Test 3 - Get user info

url = "http://127.0.0.1:8000/users?usr_id=749366f1-4aa0-47de-8d57-ae32b450c68f"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

#Test 4 - Update user info

url = "http://127.0.0.1:8000/user"

payload = json.dumps({
  "usr_id": "749366f1-4aa0-47de-8d57-ae32b450c68f",
  "usr_nickname": "PCjr",
  "usr_email": "Email",
  "usr_doc": 8801255830,
  "usr_pwd": "Matt1!123",
  "usr_credate": "2021-11-05",
  "login": 0
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("PUT", url, headers=headers, data=payload)

print(response.text)

#Test 5 - Delete user

url = "http://127.0.0.1:8000/user"

payload = json.dumps({
  "usr_id": "e41c018f-7a8f-415e-9900-10a95a620e44"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("DELETE", url, headers=headers, data=payload)

print(response.text)
