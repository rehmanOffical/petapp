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
def delete_ad(requests):
    if requests.method=='POST':
        try:
            user_id=requests.POST.get('user_id')
            ad_id=requests.POST.get('ad_id')
            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message":"User not found","success":False},status=status.HTTP_400_BAD_REQUEST)
            if not POST_ADD.objects.filter(id=ad_id).exists():
                return JsonResponse({"message":"Ad Not Found","success":False},status=status.HTTP_400_BAD_REQUEST)
            ad_post=POST_ADD.objects.get(id=ad_id).delete()
            return JsonResponse({"message":"Ad Deleted Successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'message':"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)