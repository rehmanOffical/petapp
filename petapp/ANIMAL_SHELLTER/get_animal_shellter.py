from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from petapp.models import Appuser,Animal_Shellter
from datetime import datetime
import logging

logger=logging.getLogger(__name__)
@csrf_exempt
def get_shellter_detail(request):
    if request.method=='GET':
        try:
            user_id=request.GET.get('user_id')

            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message":"User not found","success":False},status=status.HTTP_400_BAD_REQUEST)

            data=[]
            animal_shellters=Animal_Shellter.objects.filter(delete=False)
            for animal_shellter in animal_shellters:
                data.append({
                    'id':animal_shellter.id,
                    'house_name':animal_shellter.house_name,
                    'capacity':animal_shellter.capacity,
                    'current_occupancy':animal_shellter.current_occupancy,
                    'address':animal_shellter.address,
                    'location':animal_shellter.location,
                    'email':animal_shellter.email,
                    'owner_name':animal_shellter.owner_name,
                    'phone_no':animal_shellter.phone_no,
                    'created_at':animal_shellter.created_at,
                    'updated_at':animal_shellter.updated_at
                })
            return JsonResponse({"message":"Fetch data successfully","success":True,"data":data},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)