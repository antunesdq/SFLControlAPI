from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from ratelimit.decorators import ratelimit

from sflc.serializer import *

from sflc.models import *

@csrf_exempt
@ratelimit(key='ip', rate='60/m', block = True, method = ratelimit.ALL)
def image(request):
    # Method used to create image.
    if request.method == 'POST':
        try:
            image_form = ImageForm(request.POST, request.FILES)
            if Image.objects.filter(img_name = image_form['img_name']).exists():
                return JsonResponse("Image already exists", status=status.HTTP_400_BAD_REQUEST)
            elif image_form.is_valid():
                image_form.save()
                return JsonResponse("Image Created.", safe= False, status = status.HTTP_201_CREATED)
            else:
                return JsonResponse("Wrong input.", status=status.HTTP_400_BAD_REQUEST)
        except:
            return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Method used to get image information.
    if request.method == 'GET':
        try:
            img_name = request.GET('img_name')
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
    
    # Method used to update image information.
    if request.method == 'PUT':
            try:
                image_form = ImageForm(request.POST, request.FILES)
                image = Image.objects.get(img_name=image_form.data['img_name'])
                image_form = ImageForm(request.POST, request.FILES, instance=image)
                if image_form.is_valid():
                    image_form.save()
                    return JsonResponse("Image Updated.", safe= False, status = status.HTTP_200_OK)
                else:
                    return JsonResponse("Wrong input.", safe= False, status = status.HTTP_400_BAD_REQUEST)
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

