from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from petapp.models import category
from rest_framework import status
import logging

logger=logging.getLogger(__name__)

@csrf_exempt
def add_categeory(request):
    if request.method=='POST':
        try:
            name=request.POST.get('name')
            image=request.FILES.get('image')
            if not name:
                return JsonResponse({"message":"Please enter category name","success":False},status=status.HTTP_400_BAD_REQUEST)
            if category.objects.filter(name=name).exists():
                return JsonResponse({"message":"category already exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            categ=category(name=name,image=image)
            categ.save()
            return JsonResponse({"message":"Record enter successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)