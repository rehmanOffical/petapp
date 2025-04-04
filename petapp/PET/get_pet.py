from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from petapp.models import Appuser,category,userpet
from rest_framework import status
import logging

logger=logging.getLogger(__name__)
@csrf_exempt
def get_pet(request):
    if request.method=='GET':
        try:
            user_id=request.GET.get('user_id')

            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message":"User does not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            user_pet=userpet.objects.filter(user_id=Appuser.objects.get(id=user_id),delete=False)
            pet_detail=[]

            for pet in user_pet:
                pet_detail.append({
                    'id':pet.id,
                    'name':pet.name,
                    'age':pet.age,
                    'breed':pet.breed,
                    'sex':pet.sex,
                    'price':pet.price,
                    'location':pet.location,
                    'address':pet.address,
                    'status':pet.status,
                    'whatsapp_no':pet.whatsapp_no,
                    'description':pet.description,
                    'images':['https://petapp.billilo.com/'+img for img in pet.images],
                    'categ':{
                        'id':pet.categ_id.id,
                        'name':category.objects.get(id=pet.categ_id.id).name
                    },
                    'user_detail':{
                        'id':pet.user_id.id,
                        'first_name':pet.user_id.first_name,
                        'last_name':pet.user_id.last_name,
                        'email':pet.user_id.email,
                        'phone_no':pet.user_id.phone_no,
                        'country':pet.user_id.country,
                        'image':'https://petapp.billilo.com'+pet.user_id.profile_img.url if (pet.user_id.profile_img) else ''
                    },
                    'created_at':pet.created_at,
                    'updated_at':pet.updated_at,
                    'deleted_at':pet.deleted_at
                })
            return JsonResponse({"message":"Fetch Successfully","success":True,"data":pet_detail},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)