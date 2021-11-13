from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from ratelimit.decorators import ratelimit

from sflc.serializer import *

from sflc.models import *

@csrf_exempt
@ratelimit(key='ip', rate='10/m', block = True, method = ratelimit.ALL)
def user(request, usr_doc = None, usr_pwd = None):
    # Method used to create user.
    if request.method == 'POST':
        try:
            user_data = JSONParser().parse(request)
            user_serializer = UserSerializer(data=user_data)
            if User.objects.filter(usr_doc = user_data['usr_doc']).exists():
                return JsonResponse("User already exists.", status=status.HTTP_400_BAD_REQUEST)
            elif user_serializer.is_valid():
                user_serializer.save()
                return JsonResponse("User Created.", safe= False, status = status.HTTP_201_CREATED)
            else:
                return JsonResponse("Wrong input.", status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Method used to get user.
    elif request.method == 'GET':
        try:
            usr_id=request.GET['usr_id']
            if usr_id == None:
                usr_doc = request.GET['usr_doc']
                usr_pwd = request.GET['usr_pwd']
                if usr_doc == None or usr_pwd == None:
                    return JsonResponse("User does not exist or wrong password.", safe=False, status = status.HTTP_404_NOT_FOUND)
                else:
                    user = User.objects.get(usr_doc=usr_doc, usr_pwd=usr_pwd)
                    user_serializer = UserSerializer(user)
                return JsonResponse({"usr_id":user_serializer.data['usr_id']}, safe=False, status= status.HTTP_200_OK)                
            else:
                user = User.objects.get(usr_id=usr_id)
                serializer = UserSerializer(user, many=False)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return JsonResponse("Something went wrong with your request.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
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
                return JsonResponse("Wrong input.", safe= False, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            if e == User.DoesNotExist:
                return JsonResponse("User does not exist.", safe= False, status = status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Method used to delete user.
    elif request.method == 'DELETE':
        try:
            user_data = JSONParser().parse(request)
            user = User.objects.get(usr_id=user_data['usr_id'])
            user.delete()
            return JsonResponse("Deleted Successfully!",safe = False, status=status.HTTP_200_OK)
        except Exception as e:
            if e == User.DoesNotExist:
                return JsonResponse("User does not exist.", safe= False, status = status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # Anything else then CRUD.
    else:
        return JsonResponse("Method not allowed.", safe= False, status = status.HTTP_405_METHOD_NOT_ALLOWED)