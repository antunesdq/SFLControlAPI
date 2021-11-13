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

class Budget():
  def __init__(self, acc_id = None):
    self.status = True
    self.headers = {
        'Content-Type': 'application/json'
      }
    self.acc_id = None
    self.url_budget = "http://127.0.0.1:8000/budget"

  def create_budget(self):
    # Test 21 - Create budget
    try:
      if self.status:
        payload = json.dumps({
          "acc_id":self.acc_ids[0],
          "tag_id":self.acc_ids[0],
          "bud_value": 105
        })
        response = requests.request("POST", url = self.url_budget, headers=self.headers, data=payload)
        if response.status_code == 200:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 21 - create budget -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 21 - create budget -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 21 - create budget -> Status: Failure.{bcolors.ENDC}")
  
  def get_budget_by_account(self):
    # Test 22 - Get all budget info by account
    try:
      if self.status:
        response = requests.request("GET", url = f"http://127.0.0.1:8000/budget?acc_id={self.acc_ids[0]}", headers={}, data={})
        if response.status_code == 200:
          response = json.loads(response.text)
          self.bud_ids = [item.get('bud_id') for item in response]
          self.status = True
          print(f"{bcolors.OKGREEN}Test 22 - get budget by accounts -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 22 - get budget by accounts -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 22 - get budget by accounts -> Status: Failure.{bcolors.ENDC}")

  def get_budget(self):
    # Test 23 - Get budget info
    try:
      if self.status:
        response = requests.request("GET", url = f"http://127:0.0.1:8000/budget?acc_id={self.acc_ids[0]}", headers={}, data={})
        if response.status_code == 200:
          response = json.loads(response.text)
          self.status = True
          print(f"{bcolors.OKGREEN}Test 23 - get budget -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 23 - get budget -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 23 - get budget -> Status: Failure.{bcolors.ENDC}")

  def update_vault(self):
    # Test 24 - Update budget info
    try:
      if self.status:
        payload = json.dumps({
          "bud_id": self.bud_ids[0],
          "bud_value": 200
        })
        response = requests.request("PUT", url = self.url_budget, headers=self.headers, data=payload)
        if response.status_code == 200:
          response = json.loads(response.text)
          self.status = True
          print(f"{bcolors.OKGREEN}Test 24 - update budget -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 24 - update budget -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 24 - update budget -> Status: Failure.{bcolors.ENDC}")

  def delete_budget(self):
    # Test 25 - Delete budget
    try:
      if self.status:
        payload = json.dumps({
          "bud_id": self.bud_ids[0]
        })
        response = requests.request("DELETE", url = self.url_budget, headers=self.headers, data=payload)
        if response.status_code == 200:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 25 - delete budget -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 25 - delete budget -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 25 - delete budget -> Status: Failure.{bcolors.ENDC}")


class Tag():
  def __init__(self, img_name = None):
    self.status = True
    self.headers = {
        'Content-Type': 'application/json'
      }
    self.tag_id = None
    self.url_tag = "http://127.0.0.1:8000/tag"

  def create_tag(self):
    # Test 26 - Create tag
    try:
      if self.status:
        payload = json.dumps({
          "tag_name": "Test_tag",
          "img_id": "foda viu"
        })
        response = requests.request("POST", url = self.url_tag, headers=self.headers, data=payload)
        if response.status_code == 200:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 26 - create tag -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 26 - create tag -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 26 - create tag -> Status: Failure.{bcolors.ENDC}")

  def get_all_tags(self):
    # Test 27 - Get tag info
    try:
      if self.status:
        Test_tag = "Test_tag"
        response = requests.request("GET", url = f"http://127:0.0.1:8000/tag?tag_name={Test_tag}", headers={}, data={})
        if response.status_code == 200:
          response = json.loads(response.text)
          self.tag_ids = [item.get('tag_id') for item in response]
          self.status = True
          print(f"{bcolors.OKGREEN}Test 27 - get tag -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 27 - get tag -> Status: Failure.{bcolors.ENDC}")
    except Exception as e:
      print(e)
      self.status = False
      print(f"{bcolors.FAIL}Test 27 - get tag -> Status: Failure.{bcolors.ENDC}")


  def get_tag(self):
    # Test 27 - Get tag info
    try:
      if self.status:
        Test_tag = "Test_tag"
        response = requests.request("GET", url = f"http://127:0.0.1:8000/tag?tag_name={Test_tag}", headers={}, data={})
        if response.status_code == 200:
          response = json.loads(response.text)
          self.tag_ids = [item.get('tag_id') for item in response]
          self.status = True
          print(f"{bcolors.OKGREEN}Test 27 - get tag -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 27 - get tag -> Status: Failure.{bcolors.ENDC}")
    except Exception as e:
      print(e)
      self.status = False
      print(f"{bcolors.FAIL}Test 27 - get tag -> Status: Failure.{bcolors.ENDC}")

  def update_tag(self):
    # Test 28 - Update tag info
    try:
      if self.status:
        payload = json.dumps({
          "tag_id": self.tag_ids[0],
          "tag_name": "Test_tag_updated"
        })
        response = requests.request("PUT", url = self.url_tag, headers=self.headers, data=payload)
        if response.status_code == 200:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 28 - update tag -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 28 - update tag -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 28 - update tag -> Status: Failure.{bcolors.ENDC}")
    
  def delete_tag(self):
    # Test 29 - Delete tag
    try:
      if self.status:
        payload = json.dumps({
          "tag_id": self.tag_ids[0]
        })
        response = requests.request("DELETE", url = self.url_tag, headers=self.headers, data=payload)
        if response.status_code == 200:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 29 - delete tag -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 29 - delete tag -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 29 - delete tag -> Status: Failure.{bcolors.ENDC}")