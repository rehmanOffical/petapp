from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from petapp.models import category,Sub_Category
from rest_framework import status
import logging

logger=logging.getLogger(__name__)

@csrf_exempt
def get_sub_category(request):
    if request.method=='GET':
        try:
            categ_id=request.GET.get('categ_id')
            
            if not category.objects.filter(id=categ_id).exists():
                return JsonResponse({"message":"Category not found","success":False},status=status.HTTP_400_BAD_REQUEST)
            sub_categories=Sub_Category.objects.filter(categ_id=category.objects.get(id=categ_id))
            data=[]
            for categ in sub_categories:
                data.append({
                    'id':categ.id,
                    'name':categ.name,
                    'image':'https://petapp.billilo.com'+categ.image.url if categ.image else ''
                })
            return JsonResponse({"message":"Record fetch successfully","success":True,"data":data},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)