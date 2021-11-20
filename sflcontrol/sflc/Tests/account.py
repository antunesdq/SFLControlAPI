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

class Account():
  def __init__(self, usr_id = None, tag_name = None):
    self.status = True
    self.headers = {
        'Content-Type': 'application/json'
      }
    self.usr_id = usr_id
    self.acc_id = None
    self.tag_name = tag_name
    self.url_account = "http://127.0.0.1:8000/account"

  def create_account(self):
    # Test 6 - Create account
    try:
      if self.status:
        payload = json.dumps({
          "usr_id":self.usr_id,
          "acc_alias": "TestAccount",
          "tag_name":self.tag_name
        })
        response = requests.request("POST", url = self.url_account, headers=self.headers, data=payload)
        if response.status_code == 200:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 6 - create account -> Status: Success.{bcolors.ENDC}")
      else:
        self.status = False
        print(f"{bcolors.FAIL}Test 6 - create account -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 6 - create account -> Status: Failure.{bcolors.ENDC}")
      
  def get_accounts_by_user(self):
    # Test 7 - Get all accounts info by user
    try:
      if self.status:
        response = requests.request("GET", url = f"http://127.0.0.1:8000/account?usr_id={self.usr_id}", headers={}, data={})
        if response.status_code == 200:
          response = json.loads(response.text)
          self.acc_ids = [item.get('acc_id') for item in response]
          self.status = True
          print(f"{bcolors.OKGREEN}Test 7 - get accounts by user -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 7 - get accounts by user -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 7 - get accounts by user -> Status: Failure.{bcolors.ENDC}")

  def get_account(self):
    # Test 7 - Get accounts info
    try:
      if status:
        response = requests.request("GET", url = f"http://127.0.0.1:8000/account?acc_id={self.acc_ids[0]}", headers={}, data={})
        if response.status_code == 200:
          response = json.loads(response.text)
          self.status = True
          print(f"{bcolors.OKGREEN}Test 8 - get accounts -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 8 - get accounts -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 8 - get accounts -> Status: Failure.{bcolors.ENDC}")

  def update_account(self):
    # Test 8 - Update account info
    try:
      if self.status:
        payload = json.dumps({
          "acc_id": self.acc_ids[0],
          "acc_alias": "TestAliasChange",
        })
        response = requests.request("PUT", url = self.url_account, headers=self.headers, data=payload)
        if response.status_code == 200:
          response = json.loads(response.text)
          self.status = True
          print(f"{bcolors.OKGREEN}Test 9 - update account -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 9 - update account -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 9 - update account -> Status: Failure.{bcolors.ENDC}")

  def delete_account(self):
    # Test 9 - Delete account
    try:
      if self.status:
        payload = json.dumps({
          "acc_id": self.acc_ids[0]
        })
        response = requests.request("DELETE", url = self.url_account, headers=self.headers, data=payload)
        if response.status_code == 200:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 10 - delete account -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 10 - delete account -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 10 - delete account -> Status: Failure.{bcolors.ENDC}")

  def run_tests(self, usr_id):
    self.usr_id = usr_id
    self.create_account()
    self.get_accounts_by_user()
    self.get_account()
    self.update_account()
    self.delete_account()