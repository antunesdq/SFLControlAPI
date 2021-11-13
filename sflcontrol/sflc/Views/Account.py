from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from ratelimit.decorators import ratelimit

from sflc.serializer import AccountSerializer

from sflc.models import Account, Tag

from sflc.Views.Tag import tag

@csrf_exempt
@ratelimit(key='ip', rate='60/m', block = True, method = ratelimit.ALL)
def account(request):
    # Method used to create account.
    if request.method == 'POST':
        try:
            account_data = JSONParser().parse(request)
            if Account.objects.filter(acc_name=account_data['acc_name'], usr_id=account_data['usr_id']).exists():
                return JsonResponse("Account already exists", status=status.HTTP_400_BAD_REQUEST)
            if not Tag.objects.filter(tag_name=account_data['tag_name']).exists():
                tag_status = tag(request)
            if tag_status.status_code == status.HTTP_201_CREATED:            
                account_serializer = AccountSerializer(data=account_data)
                if account_serializer.is_valid():
                    account_serializer.save()
                    return JsonResponse("Account Created.", safe= False, status = status.HTTP_201_CREATED)
                else:
                    return JsonResponse("Wrong input.", status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse("Wrong input.", status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Method used to get account information.
    elif request.method == 'GET':
        try:
            acc_id = request.GET.get('acc_id')
            if acc_id == None:
                usr_id=request.GET['usr_id'],
                if usr_id == None:
                    return JsonResponse("Wrong input.", status=status.HTTP_400_BAD_REQUEST)
                else:  
                    account = Account.objects.filter(usr_id=usr_id)
                    serializer = AccountSerializer(account, many=True)
                    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
            else:
                account = Account.objects.get(acc_id=request.GET['acc_id'],)
                serializer = AccountSerializer(account, many=False)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            if e == Account.DoesNotExist:
                return JsonResponse('Account does not exist', status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
                
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
        except Exception as e:
            if e == Account.DoesNotExist:
                return JsonResponse("Account does not exist", status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
    # Anything else then CRUD.
    else:
        return JsonResponse("Method not allowed.", safe= False, status = status.HTTP_405_METHOD_NOT_ALLOWED)