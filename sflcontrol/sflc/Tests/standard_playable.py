import random
from typing import Tuple
from django.conf.urls import url
from django.test import TestCase
from pip._vendor import requests
import json

from rest_framework import status

from user import User
from account import Account
from image import Image
from tag import Tag
from transaction import Transaction
from vault import Vault
from budget import Budget


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

#TODO check all tests
#Vault - create after geting information from Account and Tag, get by acc, get, update, delete
#Budget - create after geting information from Account and Tag, get by acc, get, update, delete
#TODO create Investment and Active classes and test them.
#Investment - create after geting information from Account and Tag, get by acc, get, update, delete





  
print(f"{bcolors.OKGREEN}Begin User Crud!{bcolors.ENDC}")
user_test = User(usr_doc = 123, usr_pwd = "123")
user_test.create_user()
user_test.login_user()

print(f"{bcolors.OKGREEN}Begin Image Crud!{bcolors.ENDC}")
image_test = Image(img_name="TestImgName")
image_test.create_image()


print(f"{bcolors.OKGREEN}Begin  Account Crud!{bcolors.ENDC}")

for i in [("Tag1","#33B5E5"), ("Tag2", "#99CC00"), ("Tag3", "#FFBB33"), ("Tag4", "#FF4444"), ("Tag5", "#AA66CC"), ("Tag6", "#00FF00")]:
    tag_test = Tag(img_name = "TestImageName", tag_type="Test",  tag_name=i[0], tag_colour=i[1])
    tag_test.create_tag()

for i in range(5):
    account_test = Account(usr_id=user_test.usr_id, tag_name="Tag1", acc_alias=f"Account1{str(i)}")
    account_test.create_account()
    account_test.get_account()
    if account_test.acc_id is None:
        account_test.status = True
        account_test.get_accounts_by_user()
        account_test.acc_id = account_test.acc_ids[0]
    
    print(f"{bcolors.OKGREEN}Begin Budget Crud!{bcolors.ENDC}")
    for tag in [("Tag1","#33B5E5"), ("Tag2", "#99CC00"), ("Tag3", "#FFBB33"), ("Tag4", "#FF4444"), ("Tag5", "#AA66CC"), ("Tag6", "#00FF00")]:
        bud_test = Budget(acc_id=account_test.acc_id, tag_name=tag[0])
        bud_test.create_budget()
    
    print(f"{bcolors.OKGREEN}Begin Transaction Crud!{bcolors.ENDC}")
    for j in range(15):
        tag = random.choice([("Tag1","#33B5E5"), ("Tag2", "#99CC00"), ("Tag3", "#FFBB33"), ("Tag4", "#FF4444"), ("Tag5", "#AA66CC"), ("Tag6", "#00FF00")])
        transaction_test = Transaction(acc_id=account_test.acc_id, tag_name=tag[0])
        transaction_test.create_transaction()

print(f"{bcolors.OKGREEN}End!{bcolors.ENDC}")