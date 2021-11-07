from functools import partial
from django.db.models.query_utils import Q
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from ratelimit.decorators import ratelimit

from sflc.serializer import *

from sflc.models import *

# Create your views here.


@csrf_exempt
@ratelimit(key='ip', rate='60/m', block = True, method = ratelimit.ALL)
def user(request):
    # Method used to get user information.
    if request.method == 'GET':
        try:
            users = User.objects.get(usr_id=request.GET['usr_id'])
            serializer = UserSerializer(users, many=False)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return JsonResponse({'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    # Method used to create user.
    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("User Created.", safe= False, status = status.HTTP_200_OK)
        else:
            print(user_serializer.errors)
            return JsonResponse("User already exists or wrong input.", safe= False, status = status.HTTP_400_BAD_REQUEST)
    # Method used to update user information.
    elif request.method == 'PUT':
        try:
            user_data = JSONParser().parse(request)
            user = User.objects.get(usr_id=user_data['usr_id'])
            user_serializer = UserSerializer(user, data=user_data, partial = True)
            if user_serializer.is_valid():
                user_serializer.save()
                return JsonResponse("User Updated.", safe= False, status = status.HTTP_200_OK)
            else:
                return JsonResponse("Failed to update.", safe= False, status = status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return JsonResponse("User does not exist.", safe= False, status = status.HTTP_400_BAD_REQUEST)
    # Method used to delete user.
    elif request.method == 'DELETE':
        try:
            user_data = JSONParser().parse(request)
            user = User.objects.get(usr_id=user_data['usr_id'])
            user.delete()
            return JsonResponse("Deleted Successfully!",safe = False, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return JsonResponse("User does not exist.", safe= False, status = status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse("Method not allowed.", safe= False, status = status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
@ratelimit(key='ip', rate='60/m', block = True, method = ratelimit.ALL)
def account(request):
    # Method used to get account information.
    if request.method == 'GET':
        try:
            account = Account.objects.filter(usr_id=request.GET['usr_id'],)
            serializer = AccountSerializer(account, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except:
            try:
                account = Account.objects.get(acc_id=request.GET['acc_id'],)
                serializer = AccountSerializer(account, many=False)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
            except Account.DoesNotExist:
                return JsonResponse({'Account does not exist'}, status=status.HTTP_404_NOT_FOUND)
    # Method used to create account.
    elif request.method == 'POST':
        account_data = JSONParser().parse(request)
        account_serializer = AccountSerializer(data=account_data)
        if account_serializer.is_valid():
            account_serializer.save()
            return JsonResponse("Account Created.", safe= False, status = status.HTTP_200_OK)
        else:
            print(account_serializer.errors)
            return JsonResponse("Account already exists or wrong input.", safe= False, status = status.HTTP_400_BAD_REQUEST)
    # Method used to update account information.
    elif request.method == 'PUT':
        try:
            account_data = JSONParser().parse(request)
            account = Account.objects.get(acc_id=account_data['acc_id'])
            account_serializer = AccountSerializer(account, data=account_data, partial = True)
            if account_serializer.is_valid():
                account_serializer.save()
                return JsonResponse("Account Updated.", safe= False, status = status.HTTP_200_OK)
            else:
                return JsonResponse("Failed to update.", safe= False, status = status.HTTP_400_BAD_REQUEST)
        except Account.DoesNotExist:
            return JsonResponse("Account does not exist.", safe= False, status = status.HTTP_400_BAD_REQUEST)
    # Method used to delete account.
    elif request.method == 'DELETE':
        try:
            account_data = JSONParser().parse(request)
            account = Account.objects.get(acc_id=account_data['acc_id'])
            account.delete()
            return JsonResponse("Deleted Successfully!",safe = False, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return JsonResponse("Account does not exist.", safe= False, status = status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse("Method not allowed.", safe= False, status = status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
@ratelimit(key='ip', rate='60/m', block = True, method = ratelimit.ALL)
def login(request, usr_doc = None, usr_pwd = None):
    # Method used to log user.
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        usr_doc = user_data['usr_doc']
        usr_pwd = user_data['usr_pwd']
        if usr_doc is not None and usr_pwd is not None:
            try:
                user_data = User.objects.get(usr_doc = usr_doc, usr_pwd = usr_pwd)
                user_serializer = UserSerializer(user_data)
                return JsonResponse({"usr_id":user_serializer.data['usr_id']}, safe=False, status= status.HTTP_200_OK)
            except:
                return JsonResponse("User does not exist or wrong password.", safe=False, status = status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse("Provide user and password.", safe=False, status = status.HTTP_400_BAD_REQUEST)