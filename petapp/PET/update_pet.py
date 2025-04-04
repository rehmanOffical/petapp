from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from petapp.models import Appuser,category,userpet
from rest_framework import status
import logging
import os
from datetime import datetime
import base64
import uuid
logger=logging.getLogger(__name__)
@csrf_exempt
def update_pet(request):
    if request.method=='POST':
        try:
            images=request.FILES.getlist('images')
            name=request.POST.get('name')
            age=request.POST.get('age')
            breed=request.POST.get('breed')
            sex=request.POST.get('sex')
            pet_status=request.POST.get('status')
            price=request.POST.get('price')
            location=request.POST.get('location')
            address=request.POST.get('address')
            whatsapp_no=request.POST.get('whatsapp_no')
            description=request.POST.get('description')
            categ_id=request.POST.get('categ_id')
            user_id=request.POST.get('user_id')
            pet_id=request.POST.get('pet_id')
            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message":"User does not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            if not category.objects.filter(id=categ_id).exists():
                return JsonResponse({"message":"category does not exist","success":False},status=status.HTTP_400_BAD_REQUEST)
            if not userpet.objects.filter(id=pet_id).exists():
                return JsonResponse({"message":"Pet not found","success":False},status=status.HTTP_400_BAD_REQUEST)
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            image_paths=[]
            for img in images:
                read_img = img.read()
                image_encode = base64.b64encode(read_img).decode("utf-8")
                # Generate a unique filename and save the image
                unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}_{img.name}"
                image_path = os.path.join(upload_dir, unique_filename)

                with open(image_path, 'wb+') as destination:
                    for chunk in img.chunks():
                        destination.write(chunk)

                relative_image_path = os.path.join('media', 'uploads', unique_filename).replace('\\', '/')
                image_paths.append(relative_image_path)
            user_pet=userpet.objects.get(id=pet_id)
            user_pet.name=name
            user_pet.price=price
            user_pet.location=location
            user_pet.age=age
            user_pet.breed=breed
            user_pet.status=pet_status
            user_pet.sex=sex
            user_pet.address=address
            user_pet.whatsapp_no=whatsapp_no
            user_pet.description=description
            user_pet.categ_id=category.objects.get(id=categ_id)
            if images:
                user_pet.images=image_paths
            user_pet.updated_at=datetime.now()
            user_pet.save()
            return JsonResponse({"message":"Record updated successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)