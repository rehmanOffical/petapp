from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from petapp.models import Appuser,Animal_Shellter
from datetime import datetime
import logging

logger=logging.getLogger(__name__)

@csrf_exempt
def update_animal_shellter(request):
    if request.method=='POST':
        try:
            animal_shellter_id=request.POST.get('animal_shellter_id')
            house_name=request.POST.get('house_name')
            capacity=request.POST.get('capacity')
            current_occupancy=request.POST.get('current_occupancy')
            address=request.POST.get('address')
            location=request.POST.get('location')
            email=request.POST.get('email')
            owner_name=request.POST.get('owner_name')
            phone_no=request.POST.get('phone_no')
            user_id=request.POST.get('user_id')

            if not Animal_Shellter.objects.filter(id=animal_shellter_id).exists():
                return JsonResponse({"message":"Record not found","success":False},status=status.HTTP_400_BAD_REQUEST)
            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message":"User does not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            animal_shellter=Animal_Shellter.objects.get(id=animal_shellter_id)
            animal_shellter.house_name=house_name
            animal_shellter.capacity=capacity
            animal_shellter.current_occupancy=current_occupancy
            animal_shellter.address=address
            animal_shellter.location=location
            animal_shellter.email=email
            animal_shellter.owner_name=owner_name
            animal_shellter.phone_no=phone_no
            animal_shellter.updated_at=datetime.now()
            animal_shellter.save()

            return JsonResponse({"message":"Record updated successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)