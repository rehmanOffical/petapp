from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from petapp.models import Appuser,category,Find_Lost_Pet
from rest_framework import status
import logging

logger=logging.getLogger(__name__)

@csrf_exempt
def delete_find_or_lost(request):
    if request.method=='POST':
        try:
            user_id=request.POST.get('user_id')
            pet_id=request.POST.get('pet_id')

            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message":"User does not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            if not Find_Lost_Pet.objects.filter(id=pet_id).exists():
                return JsonResponse({"message":"Pet not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            pet=Find_Lost_Pet.objects.get(id=pet_id,delete=False)
            pet.delete=True
            pet.save()
            return JsonResponse({"message":"Pet deleted successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)