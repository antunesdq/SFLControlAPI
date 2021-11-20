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


class Image():
  def __init__(self, img_name = None):
    self.status = True
    self.headers = {}
    self.img_name = img_name
    self.url_img = "http://127.0.0.1:8000/image"

  def create_image(self):
    # Test 30 - Create image
    try:
      if self.status:
        payload={'img_name': self.img_name}
        files=[('img_image',('1.jpg',open('/home/matt/Projects/SFLControlAPI/sflcontrol/sflc/Tests/1.jpg','rb'),'image/jpeg'))]
        response = requests.request("POST", url = self.url_img, headers=self.headers, data=payload, files = files)
        if response.status_code == 201 or response.status_code == 400:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 30 - create image -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 30 - create image -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 30 - create image -> Status: Failure.{bcolors.ENDC}")
    
  def get_all_images(self):
    # Test 31 - Get all images
    try:
      if self.status:
        response = requests.request("GET", url = self.url_img, headers={}, data={})
        if response.status_code == 200:
          response = json.loads(response.text)
          self.img_names = [item.get('img_name') for item in response]
          self.status = True
          print(f"{bcolors.OKGREEN}Test 31 - get all images -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 31 - get all images -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 31 - get all images -> Status: Failure.{bcolors.ENDC}")

  def get_image(self):
    # Test 32 - Get image info
    try:
      if self.status:
        response = requests.request("GET", url = f"http://127.0.0.1:8000/image?img_name={self.img_names[0]}", headers={}, data={})
        if response.status_code == 200:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 32 - get image -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 32 - get image -> Status: Failure.{bcolors.ENDC}")
    except Exception as e:
      print(e)
      self.status = False
      print(f"{bcolors.FAIL}Test 32 - get image -> Status: Failure.{bcolors.ENDC}")
    
  def update_image(self):
    # Test 33 - Update image info
    try:
      if self.status:
        payload={'img_name': self.img_name, 'img_update': True}
        files=[('img_image',('2.jpg',open('/home/matt/Projects/SFLControlAPI/sflcontrol/sflc/Tests/2.jpg','rb'),'image/jpeg'))]
        response = requests.request("POST", url = self.url_img, headers=self.headers, data=payload, files=files)
        if response.status_code == 200:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 33 - update image -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 33 - update image -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 33 - update image -> Status: Failure.{bcolors.ENDC}")

  def delete_image(self):
    # Test 34 - Delete image
    try:
      if self.status:
        payload = json.dumps({
          "img_name": self.img_names[0]
        })
        response = requests.request("DELETE", url = self.url_img, headers=self.headers, data=payload)
        if response.status_code == 200:
          self.status = True
          print(f"{bcolors.OKGREEN}Test 34 - delete image -> Status: Success.{bcolors.ENDC}")
        else:
          self.status = False
          print(f"{bcolors.FAIL}Test 34 - delete image -> Status: Failure.{bcolors.ENDC}")
    except:
      self.status = False
      print(f"{bcolors.FAIL}Test 34 - delete image -> Status: Failure.{bcolors.ENDC}")

  def run_tests(self):
    self.create_image()
    self.get_all_images()
    self.get_image()
    self.update_image()
    self.delete_image()