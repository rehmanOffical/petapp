from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from petapp.models import Appuser,category,userpet
from rest_framework import status
import logging

logger=logging.getLogger(__name__)

@csrf_exempt
def get_category(request):
    if request.method=='GET':
        try:
            categs=category.objects.all()
            categ_list=[]
            for categ in categs:
                categ_list.append({
                    'id':categ.id,
                    'name':categ.name,
                    'image':'https://petapp.billilo.com'+ categ.image.url if categ.image else ''
                })
            return JsonResponse({"message":"Record fetch successfully","success":True,"data":categ_list},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)