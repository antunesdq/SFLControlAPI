from django.db.models.query_utils import Q
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from ratelimit.decorators import ratelimit

from sflc.serializer import *
 
# Create your views here.


@csrf_exempt
@ratelimit(key='ip', rate='60/m', block = True, method = ratelimit.ALL)
def user(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        user_serializer = UserSerializer(data=user_data)
        if user_serializer.is_valid():
            user_serializer.save()
            return JsonResponse("User Created.", safe= False, status = status.HTTP_200_OK)
        else:
            print(user_serializer.errors)
            return JsonResponse("User already exists or wrong input.", safe= False, status = status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PUT':
        return JsonResponse("Not Coded.", safe= False, status = status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        return JsonResponse("Not Coded.", safe= False, status = status.HTTP_200_OK)
    
    else:
        return JsonResponse("Method not allowed.", safe= False, status = status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
@ratelimit(key='ip', rate='60/m', block = True, method = ratelimit.ALL)
def login(request, usr_doc = None, usr_pwd = None):
    if request.method == 'POST': # TODO add this as a separate funcion so it can be ratelimit = 5s or so, also change it to post.
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