from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from petapp.models import Appuser,Vet_Clinic
from datetime import datetime
import logging

logger=logging.getLogger(__name__)

def get_vet_clinic(request):
    if request.method=='GET':
        try:
            user_id=request.GET.get('user_id')
            
            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message":"User does not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            data=[]
            
            vet_clinics=Vet_Clinic.objects.filter(delete=False)
            for vet_clinic in vet_clinics:
                data.append({
                    'id':vet_clinic.id,
                    'name':vet_clinic.name,
                    'address':vet_clinic.address,
                    'location':vet_clinic.location,
                    'email':vet_clinic.email,
                    'phone_no':vet_clinic.phone_no,
                    'owner_name':vet_clinic.owner_name,
                    'country':vet_clinic.country,
                    'created_at':vet_clinic.created_at,
                    'updated_at':vet_clinic.updated_at
                })
            return JsonResponse({"message":"Data Fetch successfully","success":True,"data":data},status=status.HTTP_200_OK) 
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)