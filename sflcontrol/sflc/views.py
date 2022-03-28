from functools import partial
from time import thread_time_ns
from django.db.models.query_utils import Q
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from ratelimit.decorators import ratelimit
from django.http import QueryDict
from rest_framework.serializers import Serializer
from sflc.serializer import *

import datetime

from sflc.models import *

# Create your views here.
# TODO Change all https to make sure they're unique.
rate =1000
@csrf_exempt
@ratelimit(key='ip', rate=f'{rate}/m', block = True, method = ratelimit.ALL)
def user(request, usr_doc = None, usr_pwd = None):
    # Method used to create user.
    if request.method == 'POST':
        try:
            user_data = JSONParser().parse(request)
            user_serializer = UserSerializer(data=user_data)
            if User.objects.filter(usr_doc = user_data['usr_doc']).exists():
                return JsonResponse("User already exists.", safe=False, status=status.HTTP_400_BAD_REQUEST)
            elif user_serializer.is_valid():
                user_serializer.save()
                return JsonResponse("User Created.", safe= False, status = status.HTTP_201_CREATED)
            else:
                return JsonResponse("Wrong input.", safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            print(e)
            return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Method used to get user.
    elif request.method == 'GET':
        try:
            usr_id=request.GET.get('usr_id')
            if usr_id == None:
                usr_doc = request.GET.get('usr_doc')
                usr_pwd = request.GET.get('usr_pwd')
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
            return JsonResponse("Something went wrong with your request.", safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
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
                return JsonResponse("Wrong input.", safe= False, status = status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            if e == User.DoesNotExist:
                return JsonResponse("User does not exist.", safe= False, status = status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Method used to delete user.
    elif request.method == 'DELETE':
        try:
            user_data = JSONParser().parse(request)
            user = User.objects.get(usr_id=user_data['usr_id'])
            user.delete()
            return JsonResponse("Deleted Successfully!", safe = False, status=status.HTTP_200_OK)
        except Exception as e:
            if e == User.DoesNotExist:
                return JsonResponse("User does not exist.", safe= False, status = status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    # Anything else then CRUD.
    else:
        return JsonResponse("Method not allowed.", safe= False, status = status.HTTP_405_METHOD_NOT_ALLOWED)


@csrf_exempt
@ratelimit(key='ip', rate=f'{rate}/m', block = True, method = ratelimit.ALL)
def user_serial(request, usr_id = None):
    if request.method == 'GET':
        try:
            usr_id = request.GET.get('usr_id')
            if usr_id != None:
                transactionlist = []    
                accs = Account.objects.filter(usr_id=usr_id)
                for acc in accs:
                    if datetime.datetime.now().day == acc.acc_refday:
                        refdate = datetime.datetime.now().date()
                    elif datetime.datetime.now().day > acc.acc_refday:
                        refdate = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, acc.acc_refday)
                    else:
                        if datetime.datetime.now().month == 1:
                            refdate = datetime.datetime(datetime.datetime.now().year-1, 12, acc.acc_refday)
                        else:
                            refdate = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month - 1, acc.acc_refday)
                    
                    transactionlist += Transaction.objects.filter(acc_id=acc.acc_id, tra_date__gte = refdate)
                tra_serializer = TransactionSerializer(transactionlist, many=True)
                exp_responseitem = {}
                pay_responseitem = {}

                for item in tra_serializer.data:
                    if item.get('tra_type') == 'Expense':
                        try:
                            exp_responseitem[item['tag_name']] += float(item['tra_value'])
                        except KeyError:
                            exp_responseitem[item['tag_name']] = float(item['tra_value'])
                    elif item.get('tra_type') == 'Payment':
                        try:
                            pay_responseitem[item['tag_name']] += float(item['tra_value'])
                        except KeyError:
                            pay_responseitem[item['tag_name']] = float(item['tra_value'])

                budgetlist = []
                accs = Account.objects.filter(usr_id=usr_id)
                for acc in accs:
                    budgetlist += Budget.objects.filter(acc_id=str(acc.acc_id))
                
                bud_serializer = BudgetSerializer(budgetlist, many=True)
                bud_responseitem = {}
                for item in bud_serializer.data:
                    try:
                        bud_responseitem[item['tag_name']] += float(item['bud_value'])
                    except KeyError:
                        bud_responseitem[item['tag_name']] = float(item['bud_value'])


                response = {}
                response['pieEntriesTraExp'] = exp_responseitem
                response['pieEntriesTraPay'] = pay_responseitem
                response['pieEntriesBud'] = bud_responseitem
                ## TODO: Fix this here. 
                response['transactions'] = {item["tra_id"]:item for item in tra_serializer.data if item.get('tra_type') == 'Expense'}
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
            else:
                return JsonResponse("You must Specify a user id.", safe=False, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return JsonResponse("Something went wrong with your request.", safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt
@ratelimit(key='ip', rate=f'{rate}/m', block = True, method = ratelimit.ALL)
def image(request, parsed = False, data = None):
    # Method used to create image.
    if request.method == 'POST':
        try:
            image_form = ImageForm(request.POST, request.FILES)
            if Image.objects.filter(img_name = image_form['img_name'].data).exists():
                if request.POST.get('img_update') == "True":
                    try:
                        image_form = ImageForm(request.POST, request.FILES)
                        image = Image.objects.get(img_name=image_form.data['img_name'])
                        image_form = ImageForm(request.POST, request.FILES, instance=image)
                        if image_form.is_valid():
                            image_form.save()
                            return JsonResponse("Image Updated.", safe= False, status = status.HTTP_200_OK)
                        else:
                            return JsonResponse("Wrong input.", safe= False, status = status.HTTP_406_NOT_ACCEPTABLE)
                    except Exception as e:
                        if e == Image.DoesNotExist:
                            return JsonResponse("Image does not exist.", safe= False, status = status.HTTP_404_NOT_FOUND)
                        else:
                            return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    return JsonResponse("Image already exists", safe=False, status=status.HTTP_400_BAD_REQUEST)
            elif parsed:
                image_form = ImageForm(data)
            if image_form.is_valid():
                image_form.save()
                return JsonResponse("Image Created.", safe= False, status = status.HTTP_201_CREATED)
        except:
            return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Method used to get image information.
    if request.method == 'GET':
        try:
            img_name = request.GET.get('img_name')
            if img_name == None:
                image = Image.objects.all()
                serializer = ImageSerializer(image, many=True)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
            else:
                image = Image.objects.get(img_name=img_name)
                serializer = ImageSerializer(image, many=False)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            if e == Image.DoesNotExist:
                return JsonResponse("Image does not exist.", safe= False, status = status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
                
    # Method used to delete image.
    elif request.method == 'DELETE':
        try:
            image_data = JSONParser().parse(request)
            image = Image.objects.get(img_name=image_data['img_name'])
            image.delete()
            return JsonResponse("Deleted Successfully!",safe = False, status=status.HTTP_200_OK)
        except Exception as e:
            if e == Image.DoesNotExist:
                return JsonResponse("Image does not exist.", safe= False, status = status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)    
   
    # Anything else then CRUD.
    else:
        return JsonResponse("Method not allowed.", safe= False, status = status.HTTP_405_METHOD_NOT_ALLOWED)


@csrf_exempt
@ratelimit(key='ip', rate=f'{rate}/m', block = True, method = ratelimit.ALL)
def tag(request, parsed = False, data = None):
    # Method used to create tag.
    if request.method == 'POST':
        try:
            if parsed:
                tag_data = data
                tag_data['img_name'] = tag_data['tag_name']
            else:
                tag_data = JSONParser().parse(request)
            if Tag.objects.filter(tag_name=tag_data['tag_name']).exists():
                return JsonResponse('Tag already exists.', safe=False, status=status.HTTP_400_BAD_REQUEST)
            if not Image.objects.filter(img_name=tag_data['img_name']).exists():
                image_status = image(request, parsed = True, data=tag_data)
                if image_status.status_code == status.HTTP_201_CREATED:
                    image_exists = True
            else:
                image_exists = True
            if image_exists:
                tag_serializer = TagSerializer(data=tag_data)
                if tag_serializer.is_valid():
                    tag_serializer.save()
                    return JsonResponse("Tag Created.", safe= False, status = status.HTTP_201_CREATED)
                else:
                    return JsonResponse("Wrong input.", safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return JsonResponse("Wrong input.", safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Method used to get tag information.
    elif request.method == 'GET':
        try:
            tag_name = request.GET.get('tag_name')
            if tag_name == None:
                tag = Tag.objects.all()
                serializer = TagSerializer(tag, many=True)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
            else:
                tag = Tag.objects.get(tag_name = tag_name)
                serializer = TagSerializer(tag, many=False)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            if e == Tag.DoesNotExist:
                return JsonResponse("Tag does not exist", safe=False, status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Method used to update tag information.
    elif request.method == 'PUT':
        try:
            tag_data = JSONParser().parse(request)
            tag = Tag.objects.get(tag_name=tag_data['tag_name'])
            tag_serializer = TagSerializer(tag, data=tag_data, partial = True)
            if tag_serializer.is_valid():
                tag_serializer.save()
                return JsonResponse("Tag Updated.", safe= False, status = status.HTTP_200_OK)
            else:
                return JsonResponse("Wrong input.", safe= False, status = status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            if e == Tag.DoesNotExist:
                return JsonResponse("Tag does not exist", safe=False, status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
    # Method used to delete tag.
    elif request.method == 'DELETE':
        try:
            tag_data = JSONParser().parse(request)
            tag = Tag.objects.get(tag_name=tag_data['tag_name'])
            tag.delete()
            return JsonResponse("Deleted Successfully!",safe = False, status=status.HTTP_200_OK)
        except Exception as e:
            if e == Tag.DoesNotExist:
                return JsonResponse("Tag does not exist", safe=False, status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
    # Anything else then CRUD.
    else:
        return JsonResponse("Method not allowed.", safe= False, status = status.HTTP_405_METHOD_NOT_ALLOWED)


@csrf_exempt
@ratelimit(key='ip', rate=f'{rate}/m', block = True, method = ratelimit.ALL)
def account(request):
    # Method used to create account.
    if request.method == 'POST':
        try:
            account_data = JSONParser().parse(request)
            if Account.objects.filter(acc_alias=account_data['acc_alias'], usr_id=account_data['usr_id']).exists():
                return JsonResponse("Account already exists", safe=False, status=status.HTTP_400_BAD_REQUEST)
            if not Tag.objects.filter(tag_name=account_data['tag_name']).exists():
                tag_status = tag(request, parsed = True, data = account_data)
                if tag_status.status_code == status.HTTP_201_CREATED: 
                    tag_exists = True
            else:
                tag_exists = True
            if tag_exists:           
                account_serializer = AccountSerializer(data=account_data)
                if account_serializer.is_valid():
                    account_serializer.save()
                    return JsonResponse({"Message":"Account Created.", "acc_id":account_serializer.data["acc_id"]}, safe= False, status = status.HTTP_201_CREATED)
                else:
                    return JsonResponse("Wrong input.", safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return JsonResponse("Wrong input.", safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Method used to get account information.
    elif request.method == 'GET':
        try:
            acc_id = request.GET.get('acc_id')
            if acc_id == None:
                usr_id=request.GET.get('usr_id'),
                if usr_id == None:
                    return JsonResponse("Wrong input.", safe=False, status=status.HTTP_406_NOT_ACCEPTABLET)
                else:  
                    account = Account.objects.filter(usr_id=usr_id)
                    serializer = AccountSerializer(account, many=True)
                    return JsonResponse({item["acc_id"]:item for item in serializer.data}, safe=False, status=status.HTTP_200_OK)
            else:
                account = Account.objects.get(acc_id=request.GET.get('acc_id'))
                serializer = AccountSerializer(account, many=False)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            if e == Account.DoesNotExist:
                return JsonResponse('Account does not exist', safe=False, status=status.HTTP_404_NOT_FOUND)
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
                return JsonResponse("Account does not exist", safe=False, status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
    # Anything else then CRUD.
    else:
        return JsonResponse("Method not allowed.", safe= False, status = status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
@ratelimit(key='ip', rate=f'{rate}/m', block = True, method = ratelimit.ALL)
def account_serial(request, acc_id = None):
    if request.method == 'GET':
        try:
            acc_id = request.GET.get('acc_id')
            if acc_id != None:
                acc = Account.objects.get(acc_id=acc_id)
                if datetime.datetime.now().day == acc.acc_refday:
                    refdate = datetime.datetime.now().date()
                elif datetime.datetime.now().day > acc.acc_refday:
                    refdate = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month, acc.acc_refday)
                else:
                    if datetime.datetime.now().month == 1:
                        refdate = datetime.datetime(datetime.datetime.now().year-1, 12, acc.acc_refday)
                    else:
                        refdate = datetime.datetime(datetime.datetime.now().year, datetime.datetime.now().month - 1, acc.acc_refday)
                transactionlist = Transaction.objects.filter(acc_id=str(acc_id), tra_date__gte = refdate)
                tra_serializer = TransactionSerializer(transactionlist, many=True)
                exp_responseitem = {}
                pay_responseitem = {}
                
                for item in tra_serializer.data:
                    if item.get('tra_type') == 'Expense':
                        try:
                            exp_responseitem[item['tag_name']] += float(item['tra_value'])
                        except KeyError:
                            exp_responseitem[item['tag_name']] = float(item['tra_value'])
                    elif item.get('tra_type') == 'Payment':
                        try:
                            pay_responseitem[item['tag_name']] += float(item['tra_value'])
                        except KeyError:
                            pay_responseitem[item['tag_name']] = float(item['tra_value'])

                budgetlist = Budget.objects.filter(acc_id=str(acc_id))
                bud_serializer = BudgetSerializer(budgetlist, many=True)
                bud_responseitem = {}
                for item in bud_serializer.data:
                    try:
                        bud_responseitem[item['tag_name']] += float(item['bud_value'])
                    except KeyError:
                        bud_responseitem[item['tag_name']] = float(item['bud_value'])

                vaultslist = Vault.objects.filter(acc_id=str(acc_id))
                vau_serializer = VaultSerializer(vaultslist, many=True)
                vau_responseitem = {}
                for item in vau_serializer.data:
                        vau_responseitem[item['tag_name']] = float(item['vau_value'])

                response = {}
                response['pieEntriesTraExp'] = exp_responseitem
                response['pieEntriesTraPay'] = pay_responseitem
                response['pieEntriesBud'] = bud_responseitem
                ## TODO: Fix this here.
                response['transactions'] = {item["tra_id"]:item for item in tra_serializer.data if item.get('tra_type') == 'Expense'}
                response['vaults'] = {item["vau_id"]:item for item in vau_serializer.data}
                return JsonResponse(response, safe=False, status=status.HTTP_200_OK)
            else:
                return JsonResponse("You must Specify a user id.", safe=False, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return JsonResponse("Something went wrong with your request.", safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@ratelimit(key='ip', rate=f'{rate}/m', block = True, method = ratelimit.ALL)
def transaction(request):
    # Method used to create transaction.
    if request.method == 'POST':
        try:
            transaction_data = JSONParser().parse(request)
            if Transaction.objects.filter(**transaction_data).exists():
                return JsonResponse("Transaction already exists.", safe=False, status=status.HTTP_400_BAD_REQUEST)
            if not Tag.objects.filter(tag_name=transaction_data['tag_name']).exists():
                tag_status = tag(request, parsed = True, data = transaction_data)
                if tag_status.status_code == status.HTTP_201_CREATED: 
                    tag_exists = True
            else:
                tag_exists = True
            if tag_exists:                       
                transaction_serializer = TransactionSerializer(data=transaction_data)
                if transaction_serializer.is_valid():
                    transaction_serializer.save()
                    return JsonResponse({"Message":"Transaction Created.", "tra_id":transaction_serializer.data["tra_id"]}, safe= False, status = status.HTTP_201_CREATED)
                else:
                    return JsonResponse("Wrong input.", safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return JsonResponse("Wrong input.", safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Method used to get transaction information.
    elif request.method == 'GET':
        try:
            tra_id = request.GET.get('tra_id')
            if tra_id is None:
                acc_id = request.GET.get('acc_id')
                if acc_id is None:
                    return JsonResponse("Wrong input.", safe=False, status=status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    transaction = Transaction.objects.filter(acc_id=acc_id)
                    serializer = TransactionSerializer(transaction, many=True)

                    return JsonResponse({item["tra_id"]:item for item in serializer.data}, safe=False, status=status.HTTP_200_OK)
            else:
                transaction = Transaction.objects.get(tra_id=tra_id)
                serializer = TransactionSerializer(transaction, many=False)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            if e == Transaction.DoesNotExist:
                return JsonResponse('Transaction does not exist', safe=False, status=status.HTTP_404_NOT_FOUND)
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
                return JsonResponse("Transaction does not exist", safe=False, status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
    # Anything else than the above methods will return 405 Method Not Allowed.
    else:
        return JsonResponse("Method not allowed.", safe= False, status = status.HTTP_405_METHOD_NOT_ALLOWED)


@csrf_exempt
@ratelimit(key='ip', rate=f'{rate}/m', block = True, method = ratelimit.ALL)
def vault(request):
    # Method used to get vault information.
    if request.method == 'GET':
        try:
            vault = Vault.objects.filter(acc_id=request.GET.get('acc_id'))
            serializer = VaultSerializer(vault, many=True)
            return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except:
            try:
                vault = Vault.objects.get(vau_id=request.GET.get('vau_id'))
                serializer = VaultSerializer(vault, many=False)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
            except Vault.DoesNotExist:
                return JsonResponse({'Vault does not exist'}, status=status.HTTP_404_NOT_FOUND)
    # Method used to create vault.
    elif request.method == 'POST':
        vault_data = JSONParser().parse(request)
        vault_serializer = VaultSerializer(data=vault_data)
        if vault_serializer.is_valid():
            vault_serializer.save()
            return JsonResponse({"Message":"Vault Created.", "vau_id":vault_serializer.data["vau_id"]}, safe= False, status = status.HTTP_201_CREATED)
        else:
            return JsonResponse("Vault already exists or wrong input.", safe= False, status = status.HTTP_400_BAD_REQUEST)
            
    # Method used to update vault information.
    elif request.method == 'PUT':
        try:
            vault_data = JSONParser().parse(request)
            vault = Vault.objects.get(vau_id=vault_data['vau_id'])
            vault_serializer = VaultSerializer(vault, data=vault_data, partial = True)
            if vault_serializer.is_valid():
                vault_serializer.save()
                return JsonResponse("Vault Updated.", safe= False, status = status.HTTP_200_OK)
            else:
                return JsonResponse("Failed to update.", safe= False, status = status.HTTP_400_BAD_REQUEST)
        except Vault.DoesNotExist:
            return JsonResponse("Vault does not exist.", safe= False, status = status.HTTP_400_BAD_REQUEST)
    # Method used to delete vault.
    elif request.method == 'DELETE':
        try:
            vault_data = JSONParser().parse(request)
            vault = Vault.objects.get(vau_id=vault_data['vau_id'])
            vault.delete()
            return JsonResponse("Deleted Successfully!",safe = False, status=status.HTTP_200_OK)
        except Vault.DoesNotExist:
            return JsonResponse("Vault does not exist.", safe= False, status = status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse("Method not allowed.", safe= False, status = status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
@ratelimit(key='ip', rate=f'{rate}/m', block = True, method = ratelimit.ALL)
def budget(request):
    # Method used to create budget.
    if request.method == 'POST':
        try:
            budget_data = JSONParser().parse(request)
            if Budget.objects.filter(**budget_data).exists():
                return JsonResponse("Budget already exists.", safe=False, status=status.HTTP_400_BAD_REQUEST)
            if not Tag.objects.filter(tag_name=budget_data['tag_name']).exists():
                tag_stattus = tag(request, parsed=True, data=budget_data)
                if tag_stattus.status_code == status.HTTP_201_CREATED:
                    tag_exists = True
            else:
                tag_exists = True
            if tag_exists:
                budget_serializer = BudgetSerializer(data=budget_data)
                if budget_serializer.is_valid():
                    budget_serializer.save()
                    return JsonResponse({"Message":"Budget Created.", "bud_id":budget_serializer.data["bud_id"]}, safe= False, status = status.HTTP_201_CREATED)
                else:
                    return JsonResponse("Wrong input.", safe= False, status = status.HTTP_406_NOT_ACCEPTABLE)
            else:
                return JsonResponse("Wrong input.", safe= False, status = status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        # Method used to get budget information.
    elif request.method == 'GET':
        try:
            bud_id = request.GET.get('bud_id')
            if bud_id is None:
                acc_id = request.GET.get('acc_id')
                if acc_id is None:
                    return JsonResponse("Wrong input.", safe= False, status = status.HTTP_406_NOT_ACCEPTABLE)
                else:
                    budget = Budget.objects.filter(acc_id=acc_id)
                    serializer = BudgetSerializer(budget, many=True)

                    return JsonResponse({item["bud_id"]:item for item in serializer.data}, safe=False, status=status.HTTP_200_OK)
            else:
                budget = Budget.objects.get(bud_id=bud_id)
                serializer = BudgetSerializer(budget, many=False)
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
        except Exception as e:
            if e == Budget.DoesNotExist:
                return JsonResponse("Budget does not exist.", safe= False, status = status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    # Method used to update budget information.
    elif request.method == 'PUT':
        try:
            budget_data = JSONParser().parse(request)
            budget = Budget.objects.get(bud_id=budget_data['bud_id'])
            budget_serializer = BudgetSerializer(budget, data=budget_data, partial = True)
            if budget_serializer.is_valid():
                budget_serializer.save()
                return JsonResponse("Budget Updated.", safe= False, status = status.HTTP_200_OK)
            else:
                return JsonResponse("Budget to update.", safe= False, status = status.HTTP_400_BAD_REQUEST)
        except Budget.DoesNotExist:
            return JsonResponse("Budget does not exist.", safe= False, status = status.HTTP_400_BAD_REQUEST)
    # Method used to delete Budget.
    elif request.method == 'DELETE':
        try:
            budget_data = JSONParser().parse(request)
            budget = Budget.objects.get(bud_id=budget_data['bud_id'])
            budget.delete()
            return JsonResponse("Deleted Successfully!",safe = False, status=status.HTTP_200_OK)
        except Exception as e:
            if e == Budget.DoesNotExist:
                return JsonResponse("Budget does not exist.", safe= False, status = status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    #Anything else than the above methods will return 405 Method Not Allowed.
    else:
        return JsonResponse("Method not allowed.", safe= False, status = status.HTTP_405_METHOD_NOT_ALLOWED)



