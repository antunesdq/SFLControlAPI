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

class Tag():
  def __init__(self, img_name = None, tag_name = None):
    self.status = True
    self.headers = {
        'Content-Type': 'application/json'
      }
    self.tag_name = tag_name
    self.img_name = img_name
    self.url_tag = "http://127.0.0.1:8000/tag"

  def create_tag(self):
    # Test 26 - Create tag
    try:
      if self.status:
        payload = json.dumps({
          "tag_name": "TestTagName",
          "tag_type": "TestTagType",
          "img_name": self.img_name
        })
        response = requests.request("POST", url = self.url_tag, headers=self.headers, data=payload)
        if response.status_code == 201 or response.status_code == 400:
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
        response = requests.request("GET", url = "http://127.0.0.1:8000/tag", headers={}, data={})
        if response.status_code == 200:
          response = json.loads(response.text)
          self.tag_names = [item.get('tag_name') for item in response]
          self.status = True
          print(f"{bcolors.OKGREEN}Test 27 - get all tag -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 27 - get all tag -> Status: Failure.{bcolors.ENDC}")
    except Exception as e:
      print(e)
      self.status = False
      print(f"{bcolors.FAIL}Test 27 - get all tag -> Status: Failure.{bcolors.ENDC}")


  def get_tag(self):
    # Test 28 - Get tag info
    try:
      if self.status:
        response = requests.request("GET", url = f"http://127.0.0.1:8000/tag?tag_name={self.tag_names[0]}", headers={}, data={})
        if response.status_code == 200:
          response = json.loads(response.text)
          self.status = True
          print(f"{bcolors.OKGREEN}Test 28 - get tag -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 28 - get tag -> Status: Failure.{bcolors.ENDC}")
    except Exception as e:
      print(e)
      self.status = False
      print(f"{bcolors.FAIL}Test 28 - get tag -> Status: Failure.{bcolors.ENDC}")

  def update_tag(self):
    # Test 29 - Update tag info
    try:
      if self.status:
        payload = json.dumps({
          "tag_name": self.tag_names[0],
          "tag_type": "TestTahNewType"
        })
        response = requests.request("PUT", url = self.url_tag, headers=self.headers, data=payload)
        if response.status_code == 200:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 29 - update tag -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 29 - update tag -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 29 - update tag -> Status: Failure.{bcolors.ENDC}")
    
  def delete_tag(self):
    # Test 30 - Delete tag
    try:
      if self.status:
        payload = json.dumps({
          "tag_name": self.tag_names[0]
        })
        response = requests.request("DELETE", url = self.url_tag, headers=self.headers, data=payload)
        if response.status_code == 200:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 30 - delete tag -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 30 - delete tag -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 30 - delete tag -> Status: Failure.{bcolors.ENDC}")