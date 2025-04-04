
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from petapp.models import Appuser,Animal_Shellter
from datetime import datetime
import logging

logger=logging.getLogger(__name__)

@csrf_exempt
def delete_animal_shellter(request):
    if request.method=='POST':
        try:
            user_id=request.POST.get('user_id')
            animal_shellter_id=request.POST.get('animal_shellter_id')
            
            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message":"User does not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            if not Animal_Shellter.objects.filter(id=animal_shellter_id,delete=False).exists():
                return JsonResponse({"message":"Record does not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            anima_shellter=Animal_Shellter.objects.get(id=animal_shellter_id,delete=False)
            anima_shellter.delete=True
            anima_shellter.save()
            return JsonResponse({"message":"Deleted Successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)