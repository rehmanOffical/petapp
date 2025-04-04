from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from petapp.models import Appuser
from rest_framework import status
from datetime import datetime
from django.conf import settings
import logging
import os
logger=logging.getLogger(__name__)

@csrf_exempt
def update_user(request):
    if request.method=='POST':
        try:
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            email=request.POST.get('email')
            country=request.POST.get('country')
            phone_no=request.POST.get('phone_no')
            password=request.POST.get('password')
            confirm_password=request.POST.get('confirm_password')
            profile_img=request.FILES.get('profile_img')
            user_id=request.POST.get('user_id')

            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message":"User does not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            if Appuser.objects.filter(email=email).exclude(id=user_id).exists():
                return JsonResponse({"message":"This email is already register","success":False},status=status.HTTP_400_BAD_REQUEST)
            if password!=confirm_password:
                return JsonResponse({"messgae":"Password and Confirm Password should be same","success":False},status=status.HTTP_400_BAD_REQUEST)
            appuser=Appuser.objects.get(id=user_id)
            appuser.first_name=first_name
            appuser.last_name=last_name
            appuser.country=country
            appuser.phone_no=phone_no
            appuser.password=make_password(password)
            appuser.email=email
            appuser.updated_at=datetime.now()
            appuser.profile_img=profile_img
            appuser.save()
            return JsonResponse({"message":"Record updated successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)