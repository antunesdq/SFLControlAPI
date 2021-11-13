from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from ratelimit.decorators import ratelimit

from sflc.serializer import TransactionSerializer

from sflc.models import Transaction, Account

from sflc.Views.Account import account


@csrf_exempt
@ratelimit(key='ip', rate='60/m', block = True, method = ratelimit.ALL)
def transaction(request):
    # Method used to create transaction.
    if request.method == 'POST':
        transaction_data = JSONParser().parse(request)
        transaction_serializer = TransactionSerializer(data=transaction_data)
        if transaction_serializer.is_valid():
            transaction_serializer.save()
            return JsonResponse("Transaction Created.", safe= False, status = status.HTTP_201_CREATED)
        else:
            return JsonResponse("Wrong input.", status=status.HTTP_400_BAD_REQUEST)

    # Method used to get transaction information.
    elif request.method == 'GET':
        try:
            tra_id = request.GET.get('tra_id')
            if tra_id is None:
                acc_id = request.GET.get('acc_id')
                if acc_id is None:
                    return JsonResponse("Wrong input.", status=status.HTTP_400_BAD_REQUEST)
                else:
                    transaction = Transaction.objects.filter(acc_id=request.GET['acc_id'])
                    serializer = TransactionSerializer(transaction, many=True)
                    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
            else:
                transaction = Transaction.objects.get(tra_id=request.GET['tra_id'],)
                serializer = TransactionSerializer(transaction, many=False)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            if e == Transaction.DoesNotExist:
                return JsonResponse({'Transaction does not exist'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Method used to update Transaction information.
    elif request.method == 'PUT':
        try:
            transaction_data = JSONParser().parse(request)
            transaction = Transaction.objects.get(tra_id=transaction_data['tra_id'])
            transaction_serializer = TransactionSerializer(transaction, data=transaction_data, partial = True)
            if transaction_serializer.is_valid():
                transaction_serializer.save()
                return JsonResponse("Transaction Updated.", safe= False, status = status.HTTP_200_OK)
            else:
                return JsonResponse("Failed to update.", safe= False, status = status.HTTP_400_BAD_REQUEST)
        except Transaction.DoesNotExist:
            return JsonResponse("Transaction does not exist.", safe= False, status = status.HTTP_400_BAD_REQUEST)
    
    # Method used to delete transaction.
    elif request.method == 'DELETE':
        try:
            transaction_data = JSONParser().parse(request)
            transaction = Transaction.objects.get(tra_id=transaction_data['tra_id'])
            transaction.delete()
            return JsonResponse("Deleted Successfully!",safe = False, status=status.HTTP_200_OK)
        except Exception as e:
            if e == Transaction.DoesNotExist:
                return JsonResponse("Transaction does not exist", status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
    # Anything else then CRUD.
    else:
        return JsonResponse("Method not allowed.", safe= False, status = status.HTTP_405_METHOD_NOT_ALLOWED)