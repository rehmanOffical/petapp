from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from petapp.models import Appuser, userpet, Favourite
import logging

logger=logging.getLogger(__name__)
@csrf_exempt
def get_favourite(request):
    if request.method=='GET':
        try:
            user_id=request.GET.get('user_id')

            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message":"user does not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            favorite_obj=Favourite.objects.filter(user_id=Appuser.objects.get(id=user_id),status=True)
            fav_data=[]
            for obj in favorite_obj:
                fav_data.append({
                    'id':obj.id,
                    'status':obj.status,
                    'pet':{
                        'id':obj.pet_id.id,
                        'name':obj.pet_id.name,
                        'age':obj.pet_id.age,
                        'breed':obj.pet_id.breed,
                        'sex':obj.pet_id.sex,
                        'price':obj.pet_id.price,
                        'location':obj.pet_id.location,
                        'address':obj.pet_id.address,
                        'whatsapp_no':obj.pet_id.whatsapp_no,
                        'description':obj.pet_id.description,
                        'images':['https://petapp.billilo.com/'+img for img in obj.pet_id.images],
                        'category':obj.pet_id.categ_id.name,
                        'owner_detail':{
                            'id':obj.pet_id.user_id.id,
                            'first_name':obj.pet_id.user_id.first_name,
                            'last_name':obj.pet_id.user_id.last_name,
                            'email':obj.pet_id.user_id.email,
                            'phone_no':obj.pet_id.user_id.phone_no,
                            'country':obj.pet_id.user_id.country,
                            'image':'https://petapp.billilo.com'+obj.pet_id.user_id.profile_img.url if (obj.pet_id.user_id.profile_img) else ''
                        },
                    },
                    'favorite_added_by':{
                        'id':obj.user_id.id,
                            'first_name':obj.user_id.first_name,
                            'last_name':obj.user_id.last_name,
                            'email':obj.user_id.email,
                            'phone_no':obj.user_id.phone_no,
                            'country':obj.user_id.country,
                            'image':'https://petapp.billilo.com'+obj.user_id.profile_img.url if (obj.user_id.profile_img) else ''
                    }
                })
            return JsonResponse({"message":"Fetch record successfully","success":True,"data":fav_data},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","succcess":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)
