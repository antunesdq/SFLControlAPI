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

class Transaction():
  def __init__(self, acc_id = None, tag_name = None):
    self.status = True
    self.headers = {
        'Content-Type': 'application/json'
      }
    self.acc_id = acc_id
    self.tag_name = tag_name
    self.url_transaction = "http://127.0.0.1:8000/transaction"

  def create_transaction(self):
    # Test 11 - Create transaction
    try:
      if self.status:
        payload = json.dumps({
          "acc_id":self.acc_id,
          "tra_date": "2006-10-25 14:30",
          "tra_value": 105,
          "tra_name": "Sei la",
          "tag_name": self.tag_name
        })
        response = requests.request("POST", url = self.url_transaction, headers=self.headers, data=payload)
        if response.status_code == 201:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 11 - create transaction -> Status: Success.{bcolors.ENDC}")
      else:
        self.status = False
        print(f"{bcolors.FAIL}Test 11 - create transaction -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 11 - create transaction -> Status: Failure.{bcolors.ENDC}")
      
  def get_transactions_by_account(self):
    # Test 12 - Get all transaction info by account
    try:
      if self.status:
        response = requests.request("GET", url = f"http://127.0.0.1:8000/transaction?acc_id={self.acc_id}", headers={}, data={})
        if response.status_code == 200:
          response = json.loads(response.text)
          self.tra_ids = [item.get('tra_id') for item in response]
          self.status = True
          print(f"{bcolors.OKGREEN}Test 12 - get transactions by accounts -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 12 - get transactions by accounts -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 12 - get transactions by accounts -> Status: Failure.{bcolors.ENDC}")

  def get_transaction(self):
    # Test 13 - Get transactions info
    try:
      if status:
        response = requests.request("GET", url = f"http://127.0.0.1:8000/transaction?tra_id={self.tra_ids[0]}", headers={}, data={})
        if response.status_code == 200:
          response = json.loads(response.text)
          self.status = True
          print(f"{bcolors.OKGREEN}Test 13 - get transactions -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 13 - get transactions -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 13 - get transactions -> Status: Failure.{bcolors.ENDC}")

  def update_transaction(self):
    # Test 14 - Update transaction info
    try:
      if self.status:
        payload = json.dumps({
          "tra_id": self.tra_ids[0],
          "tra_value": 2500,
        })
        response = requests.request("PUT", url = self.url_transaction, headers=self.headers, data=payload)
        if response.status_code == 200:
          response = json.loads(response.text)
          self.status = True
          print(f"{bcolors.OKGREEN}Test 14 - update transactions -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 14 - update transactions -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 14 - update transactions -> Status: Failure.{bcolors.ENDC}")

  def delete_transaction(self):
    # Test 15 - Delete transactions
    try:
      if self.status:
        payload = json.dumps({
          "tra_id": self.tra_ids[0]
        })
        response = requests.request("DELETE", url = self.url_transaction, headers=self.headers, data=payload)
        if response.status_code == 200:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 15 - delete transaction -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 15 - delete transaction -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 15 - delete transaction -> Status: Failure.{bcolors.ENDC}")