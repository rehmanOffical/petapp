from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from petapp.models import Appuser, fcm_token
from rest_framework import status
import logging
from petapp.register_device import notify_user
import os
from datetime import datetime
import base64
import uuid

@csrf_exempt
def forward_notification(requests):
    if requests.method=='POST':
        try:
            user_id=requests.POST.get('user_id')
            title=requests.POST.get('title')
            body=requests.POST.get('body')
            
            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message":"User not found","success":False},status=status.HTTP_400_BAD_REQUEST)
            if not (title and body):
                return JsonResponse({"message":"Title and body is required","success":False},status=status.HTTP_400_BAD_REQUEST)
            tokens=fcm_token.objects.filter(enable=True)
            
            for token in tokens:
                notify_user(token.token,title,body)
            return JsonResponse({"message":"Send Successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)
            
            