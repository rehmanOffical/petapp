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
def get_ad(requests):
    if requests.method=='GET':
        try:
            user_id=requests.GET.get('user_id')
            
            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message":"User not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            ad_list=[]
            ad_details=POST_ADD.objects.all().order_by('-id')
            
            for ad_detail in ad_details:
                ad_list.append({
                    'id':ad_detail.id,
                    'title':ad_detail.title,
                    'desc':ad_detail.desc,
                    'images':['https://petapp.billilo.com/'+img for img in ad_detail.images],
                    'created_at':ad_detail.created_at,
                    'updated_at':ad_detail.updated_at,
                })
            return JsonResponse({'message':"Data Fetch Successfully","success":True,"data":ad_list},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)        