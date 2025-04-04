from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from petapp.models import Appuser,Animal_Shellter,Role
from datetime import datetime
import logging

logger=logging.getLogger(__name__)

@csrf_exempt
def add_animal_shellter(request):
    if request.method=='POST':
        try:
            house_name=request.POST.get('house_name')
            capacity=request.POST.get('capacity')
            current_occupancy=request.POST.get('current_occupancy')
            address=request.POST.get('address')
            location=request.POST.get('location')
            email=request.POST.get('email')
            owner_name=request.POST.get('owner_name')
            phone_no=request.POST.get('phone_no')
            user_id=request.POST.get('user_id')

            if not Appuser.objects.filter(id=user_id,role_id=Role.objects.get(id=1)).exists():
                return JsonResponse({"message":"User does not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            if not (house_name and capacity and current_occupancy and address and location and email and owner_name and phone_no):
                return JsonResponse({"message":"Please fill all required field","success":False},status=status.HTTP_400_BAD_REQUEST)

            animal_sheltter=Animal_Shellter(house_name=house_name,capacity=capacity,current_occupancy=current_occupancy,address=address,location=location,email=email,owner_name=owner_name,phone_no=phone_no,user_id=Appuser.objects.get(id=user_id),created_at=datetime.now(),updated_at=datetime.now())
            animal_sheltter.save()
            return JsonResponse({"message":"Record added successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)