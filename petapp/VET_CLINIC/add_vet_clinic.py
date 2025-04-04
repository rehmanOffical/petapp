from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from petapp.models import Appuser,Vet_Clinic,Role
from datetime import datetime
import logging

logger=logging.getLogger(__name__)

@csrf_exempt
def add_vet_clinic(request):
    if request.method=='POST':
        try:
            user_id=request.POST.get('user_id')
            name=request.POST.get('name')
            address=request.POST.get('address')
            location=request.POST.get('location')
            email=request.POST.get('email')
            phone_no=request.POST.get('phone_no')
            owner_name=request.POST.get('owner_name')
            country=request.POST.get('country')

            if not Appuser.objects.filter(id=user_id,role_id=Role.objects.get(id=1)).exists():
                return JsonResponse({"message":"User does not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            if not (name,address,location,email,phone_no,owner_name,country):
                return JsonResponse({"message":"Please fill all required field","success":False},status=status.HTTP_400_BAD_REQUEST)
            vet_clinic=Vet_Clinic(name=name,address=address,location=location,email=email,phone_no=phone_no,owner_name=owner_name,country=country,created_at=datetime.now(),updated_at=datetime.now(),user_id=Appuser.objects.get(id=user_id))
            vet_clinic.save()
            return JsonResponse({"message":"Record added successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)