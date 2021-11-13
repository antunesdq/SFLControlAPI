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

class Vault():
  def __init__(self, acc_id = None):
    self.status = True
    self.headers = {
        'Content-Type': 'application/json'
      }
    self.acc_id = None
    self.url_vault = "http://127.0.0.1:8000/vault"

  def create_vault(self):
    # Test 16 - Create vault
    try:
      if self.status:
        payload = json.dumps({
          "acc_id":self.acc_ids[0],
          "tag_id": self.tag_ids[0],
          "vau_value": 105
        })
        response = requests.request("POST", url = self.url_vault, headers=self.headers, data=payload)
        if response.status_code == 200:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 16 - create vault -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 16 - create vault -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 16 - create vault -> Status: Failure.{bcolors.ENDC}")

  def get_vault_by_account(self):
    # Test 17 - Get all vault info by account
    try:
      if self.status:
        response = requests.request("GET", url = f"http://127.0.0.1:8000/vault?acc_id={self.acc_ids[0]}", headers={}, data={})
        if response.status_code == 200:
          response = json.loads(response.text)
          self.vau_ids = [item.get('vau_id') for item in response]
          self.status = True
          print(f"{bcolors.OKGREEN}Test 17 - get vault by accounts -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 17 - get vault by accounts -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 17 - get vault by accounts -> Status: Failure.{bcolors.ENDC}")

  def get_vault(self):
    # Test 18 - Get vault info
    try:
      if self.status:
        response = requests.request("GET", url = f"http://127.0.0.1:8000/vault?acc_id={self.acc_ids[0]}", headers={}, data={})
        if response.status_code == 200:
          response = json.loads(response.text)
          self.status = True
          print(f"{bcolors.OKGREEN}Test 18 - get vault -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 18 - get vault -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 18 - get vault -> Status: Failure.{bcolors.ENDC}")

  def update_vault(self):
    # Test 19 - Update vault info
    try:
      if self.status:
        payload = json.dumps({
          "vau_id": self.vau_ids[0],
          "vau_value": 200
        })
        response = requests.request("PUT", url = self.url_vault, headers=self.headers, data=payload)
        if response.status_code == 200:
          response = json.loads(response.text)
          self.status = True
          print(f"{bcolors.OKGREEN}Test 19 - update vault -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 19 - update vault -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 19 - update vault -> Status: Failure.{bcolors.ENDC}")

  def delete_vault(self):
    # Test 20 - Delete vault
    try:
      if self.status:
        payload = json.dumps({
          "vau_id": self.vau_ids[0]
        })
        response = requests.request("DELETE", url = self.url_vault, headers=self.headers, data=payload)
        if response.status_code == 200:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 20 - delete vault -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 20 - delete vault -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 20 - delete vault -> Status: Failure.{bcolors.ENDC}")