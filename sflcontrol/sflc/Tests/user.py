from typing import Tuple
from django.conf.urls import url
from django.test import TestCase
from pip._vendor import requests
import json

from rest_framework import status

# Create your tests here.

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class User():
  def __init__(self, usr_doc, usr_pwd):
      self.usr_doc = usr_doc
      self.usr_pwd = usr_pwd
      self.status = True
      self.headers = {
          'Content-Type': 'application/json'
        }
      self.usr_id = None
      self.url_user = "http://127.0.0.1:8000/user"
      self.url_login = f"http://127.0.0.1:8000/user?usr_doc={self.usr_doc}&usr_pwd={self.usr_pwd}"

  def create_user(self):
    # Test 1 - Create a new user
    try:
      if self.status:
        payload = json.dumps({
          "usr_nickname": "TestNickname",
          "usr_email": "TestEmail",
          "usr_doc": self.usr_doc,
          "usr_pwd": self.usr_pwd,
          "usr_credate": "2021-11-05",
        })
        response = requests.request("POST", url=self.url_user, headers=self.headers, data=payload)
        if response.status_code == 201 or response.status_code == 400:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 1 - create user -> Status: Success.{bcolors.ENDC}")
      else:
        self.status = False
        print(f"{bcolors.FAIL}Test 1 - create user -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 1 - create user -> Status: Failure.{bcolors.ENDC}")

  def login_user(self):
    # Test 2 - Login with user
    try:
      if self.status:

        response = requests.request("GET", url = self.url_login, headers={}, data={})
        if response.status_code == 200:
          response = json.loads(response.text)
          self.usr_id = response.get('usr_id')
          self.status = True
          print(f"{bcolors.OKGREEN}Test 2 - login user -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 2 - login user -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 2 - login user -> Status: Failure.{bcolors.ENDC}")

  def get_user(self):
    # Test 3 - Get user info
    try:
      if self.status:
        response = requests.request("GET", url = f"http://127.0.0.1:8000/user?usr_id={self.usr_id}", headers={}, data={})
        if response.status_code == 200:
          response = json.loads(response.text)
          self.status = True
          print(f"{bcolors.OKGREEN}Test 3 - get user -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 3 - get user -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 3 - get user -> Status: Failure.{bcolors.ENDC}")

  def update_user(self):
    # Test 4 - Update user info
    try:
      if self.status:
        payload = json.dumps({
          "usr_id": self.usr_id,
          "usr_email": "TestEmailChange",
        })
        response = requests.request("PUT", url=self.url_user, headers=self.headers, data=payload)
        if response.status_code == 200:
          response = json.loads(response.text)
          self.status = True
          print(f"{bcolors.OKGREEN}Test 4 - update user -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 4 - update user -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 4 - update user -> Status: Failure.{bcolors.ENDC}")

  def delete_user(self):
    # Test 5 - Delete user
    try:
      if self.status:
        payload = json.dumps({
          "usr_id": self.usr_id
        })
        response = requests.request("DELETE", url=self.url_user, headers=self.headers, data=payload)
        if response.status_code == 200:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 5 - delete user -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 5 - delete user -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 5 - delete user -> Status: Failure.{bcolors.ENDC}")

  def run_tests(self):
    self.create_user()
    self.login_user()
    self.get_user()
    self.update_user()
    self.delete_user()