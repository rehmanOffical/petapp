from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from petapp.models import category,Sub_Category
from rest_framework import status
import logging

logger=logging.getLogger(__name__)

@csrf_exempt
def add_sub_categeory(request):
    if request.method=='POST':
        try:
            categ_id=request.POST.get('categ_id')
            name=request.POST.get('name')
            image=request.FILES.get('image')
            
            if not category.objects.filter(id=categ_id).exists():
                return JsonResponse({"message":"Category not found","success":False},status=status.HTTP_400_BAD_REQUEST)
            if not name:
                return JsonResponse({"message":"Please enter category name","success":False},status=status.HTTP_400_BAD_REQUEST)
            if Sub_Category.objects.filter(name=name).exists():
                return JsonResponse({"message":"category already exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            categ=Sub_Category(name=name,image=image,categ_id=category.objects.get(id=categ_id))
            categ.save()
            return JsonResponse({"message":"Record enter successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)