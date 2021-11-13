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
#User, Accout, Image, Tag_t, Transaction, Budget, Vault
#User - create or login, get, update, delete
#Account - create, get by user, get, update, delete
#Image - create, get all, get, update, delete
#Tag_t - create after geting information from Image, get all, get, update, delete
#Transaction - create after geting information from Account and Tag_t, get by acc, get, update, delete
#Vault - create after geting information from Account and Image, get by acc, get, update, delete
#Budget - create after geting information from Account and Image, get by acc, get, update, delete
#TODO create Investment and Active classes and test them.
#Active - create after geting information from Image, get all, get, update, delete
#Investment - create after geting information from Account and Active, get by acc, get, update, delete





  
print(f"{bcolors.OKGREEN}Begin User Crud!{bcolors.ENDC}")
user_test = User(usr_doc = 1234567890, usr_pwd = "TestPassword")
user_test.create_user()
user_test.login_user()
user_test.get_user()
user_test.update_user()

print(f"{bcolors.OKGREEN}Begin Image Crud!{bcolors.ENDC}")
image_test = Image(img_name="TestImgName")
image_test.create_image()
image_test.get_all_images()
image_test.get_image()
image_test.update_image()


print(f"{bcolors.OKGREEN}Begin  Account Crud!{bcolors.ENDC}")
tag_test = Tag(img_name=image_test.img_name, tag_name="TestTagName")
tag_test.create_tag()
tag_test.get_all_tags()
tag_test.get_tag()
tag_test.update_tag()
tag_test.delete_tag()

print(f"{bcolors.OKGREEN}Begin  Account Crud!{bcolors.ENDC}")
account_test = Account(usr_id=user_test.usr_id, tag_name=tag_test.tag_name)
account_test.create_account()
account_test.get_accounts_by_user()
account_test.get_account()
account_test.update_account()

print(f"{bcolors.OKGREEN}Begin Transaction Crud!{bcolors.ENDC}")
transaction_test = Transaction(acc_id=account_test.acc_ids[0], tag_name="TestTagNewName")
transaction_test.create_transaction()
transaction_test.get_transactions_by_account()
transaction_test.get_transaction()
transaction_test.update_transaction()

print(f"{bcolors.OKGREEN}Deleting Everything!{bcolors.ENDC}")
transaction_test.delete_transaction()
account_test.delete_account()
tag_test.delete_tag()
image_test.delete_image()
user_test.delete_user()


#  user_test.create_tag()
#  user_test.get_tag()

#  user_test.create_vault()
#  user_test.get_vault_by_account()
#  user_test.get_vault()
#  user_test.update_vault()
#  user_test.delete_vault()

#  user_test.create_budget()
#  user_test.get_budget_by_account()
#  user_test.get_budget()
#  user_test.update_budget()
#  user_test.delete_budget()

print(f"{bcolors.OKGREEN}End!{bcolors.ENDC}")