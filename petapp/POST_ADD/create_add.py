from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from petapp.models import Appuser, POST_ADD
from rest_framework import status
import logging
import os
from datetime import datetime
import base64
import uuid

@csrf_exempt

def create_add(requests):
    if requests.method=='POST':
        try:
            user_id=requests.POST.get('user_id')
            title=requests.POST.get('title')
            desc=requests.POST.get('desc')
            images=requests.FILES.getlist('images')
            
            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message":"User not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'ads')
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

                relative_image_path = os.path.join('media', 'ads', unique_filename).replace('\\', '/')
                image_paths.append(relative_image_path)
            add_post=POST_ADD(title=title,desc=desc,images=image_paths,user_id=Appuser.objects.get(id=user_id),created_at=datetime.now(),updated_at=datetime.now())
            add_post.save()
            return JsonResponse({"message":"Ad Posted Successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)