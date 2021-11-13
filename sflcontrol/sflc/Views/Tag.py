from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from ratelimit.decorators import ratelimit

from sflc.serializer import TagSerializer

from sflc.models import Tag, Image

from sflc.Views.Image import image

@csrf_exempt
@ratelimit(key='ip', rate='60/m', block = True, method = ratelimit.ALL)
def tag(request):
    # Method used to create tag.
    if request.method == 'POST':
        try:
            tag_data = JSONParser().parse(request)
            if Tag.objects.filter(tag_name=tag_data['tag_name']).exists():
                return JsonResponse({'Tag already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            if not Image.objects.filter(image_name=tag_data['img_name']).exists():
                image_status = image(request)
            if image_status.status_code == status.HTTP_201_CREATED:
                tag_serializer = TagSerializer(data=tag_data)
                if tag_serializer.is_valid():
                    tag_serializer.save()
                    return JsonResponse("Tag Created.", safe= False, status = status.HTTP_201_CREATED)
                else:
                    return JsonResponse("Wrong input.", status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse("Wrong input.", status=status.HTTP_400_BAD_REQUEST)
        except:
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
                return JsonResponse("Tag does not exist", status=status.HTTP_404_NOT_FOUND)
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
                return JsonResponse("Wrong input.", safe= False, status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            if e == Tag.DoesNotExist:
                return JsonResponse("Tag does not exist", status=status.HTTP_404_NOT_FOUND)
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
                return JsonResponse("Tag does not exist", status=status.HTTP_404_NOT_FOUND)
            else:
                return JsonResponse("Something went wrong with your request.", safe=False, status = status.HTTP_500_INTERNAL_SERVER_ERROR)    
    
    # Anything else then CRUD.
    else:
        return JsonResponse("Method not allowed.", safe= False, status = status.HTTP_405_METHOD_NOT_ALLOWED)