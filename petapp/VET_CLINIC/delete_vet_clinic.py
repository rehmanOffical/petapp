from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from petapp.models import Appuser,Vet_Clinic,Role
from datetime import datetime
import logging

logger=logging.getLogger(__name__)
@csrf_exempt
def delete_vet_clinic(request):
    if request.method=='POST':
        try:
            vet_clinic_id=request.POST.get('vet_clinic_id')
            user_id=request.POST.get('user_id')

            if not Appuser.objects.filter(id=user_id,role_id=Role.objects.get(id=1)).exists():
                return JsonResponse({"message":"User does not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            if not Vet_Clinic.objects.filter(id=vet_clinic_id,delete=False):
                return JsonResponse({"message":"Record not Found","success":False},status=status.HTTP_400_BAD_REQUEST)
            vet_clinic=Vet_Clinic.objects.get(id=vet_clinic_id)
            vet_clinic.delete=True
            vet_clinic.save()
            return JsonResponse({"message":"Deleted Successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_500_INTERNAL_SERVER_ERROR)