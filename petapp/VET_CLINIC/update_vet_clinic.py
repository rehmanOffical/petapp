from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from petapp.models import Appuser,Vet_Clinic,Role
from datetime import datetime
import logging

logger=logging.getLogger(__name__)

@csrf_exempt
def update_vet_clinic(request):
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
            vet_clinic_id=request.POST.get('vet_clinic_id')
            if not Appuser.objects.filter(id=user_id,role_id=Role.objects.get(id=1)).exists():
                return JsonResponse({"message":"User does not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            if not Vet_Clinic.objects.filter(id=vet_clinic_id):
                return JsonResponse({"message":"Record not Found","success":False},status=status.HTTP_400_BAD_REQUEST)
            vet_clinic=Vet_Clinic.objects.get(id=vet_clinic_id)
            vet_clinic.name=name
            vet_clinic.address=address
            vet_clinic.location=location
            vet_clinic.email=email
            vet_clinic.phone_no=phone_no
            vet_clinic.owner_name=owner_name
            vet_clinic.country=country
            vet_clinic.updated_at=datetime.now()
            vet_clinic.save()
            return JsonResponse({"message":"Record updated successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)