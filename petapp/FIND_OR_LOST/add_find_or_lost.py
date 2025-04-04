from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from petapp.models import Appuser, category, Find_Lost_Pet
from rest_framework import status
import logging
import os
from datetime import datetime
import base64
import uuid

logger = logging.getLogger(__name__)

@csrf_exempt
def add_find_or_lost(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            images = request.FILES.getlist('images')
            age = request.POST.get('age')
            breed = request.POST.get('breed')
            sex = request.POST.get('sex')
            color = request.POST.get('color')
            identity_mark = request.POST.get('identity_mark')
            pet_status = request.POST.get('status')
            categ = request.POST.get('categ_id')
            person_name = request.POST.get('person_name')
            address = request.POST.get('address')
            location = request.POST.get('location')
            phone_no = request.POST.get('phone_no')
            description = request.POST.get('description')
            user_id = request.POST.get('user_id')

            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message": "User does not exist", "success": False}, status=status.HTTP_400_BAD_REQUEST)
            if not (name and images and color and identity_mark and pet_status and categ and person_name and address and location and phone_no and description):
                return JsonResponse({"message": "Please fill all required fields", "success": False}, status=status.HTTP_400_BAD_REQUEST)
            if not category.objects.filter(id=categ).exists():
                return JsonResponse({"message": "Category not found", "success": False}, status=status.HTTP_400_BAD_REQUEST)

            upload_dir = os.path.join(settings.MEDIA_ROOT, 'find_lost_pet')
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)

            image_paths = []
            for img in images:
                read_img = img.read()
                image_encode = base64.b64encode(read_img).decode("utf-8")
                # Generate a unique filename and save the image
                unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex}_{img.name}"
                image_path = os.path.join(upload_dir, unique_filename)

                with open(image_path, 'wb+') as destination:
                    for chunk in img.chunks():
                        destination.write(chunk)

                relative_image_path = os.path.join('media', 'find_lost_pet', unique_filename).replace('\\', '/')
                image_paths.append(relative_image_path)
            find_lost_pet=Find_Lost_Pet(name=name,images=image_paths,age=age,breed=breed,sex=sex,identity_mark=identity_mark,categ_id=category.objects.get(id=categ),color=color,status=pet_status,person_name=person_name,address=address,location=location,phone_no=phone_no,description=description,user_id=Appuser.objects.get(id=user_id),created_at=datetime.now(),updated_at=datetime.now())
            find_lost_pet.save()
            return JsonResponse({"message":"Record added successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)