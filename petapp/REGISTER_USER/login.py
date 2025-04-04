from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from petapp.models import Appuser,logout,userpet,category,Role,Favourite
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
import logging

logger=logging.getLogger(__name__)

@csrf_exempt
def login(request):
    if request.method=='POST':
        try:
            email=request.POST.get('email')
            password=request.POST.get('password')

            if not Appuser.objects.filter(email=email).exists():
                return JsonResponse({"message":"User does not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            appuser=Appuser.objects.get(email=email)

            if check_password(password,appuser.password):
                refresh_token=RefreshToken.for_user(appuser)
                access_token=str(refresh_token.access_token)
                Logout=logout(access_token=access_token,user_id=appuser)
                Logout.save()
                appuser.login_at=datetime.now()
                appuser.save()
                pets=userpet.objects.filter(user_id=appuser,delete=False)
                total_posted_pet=userpet.objects.filter(user_id=appuser,delete=False).count()
                favourite_pet=Favourite.objects.filter(user_id=appuser).count()
                pet_detail=[]
                for pet in pets:
                    pet_detail.append({
                    'id':pet.id,
                    'name':pet.name,
                    'price':pet.price,
                    'location':pet.location,
                    'address':pet.address,
                    'whatsapp_no':pet.whatsapp_no,
                    'description':pet.description,
                    'images':['https://petapp.billilo.com'+img for img in pet.images],
                    'categ':{
                        'id':pet.categ_id.id,
                        'name':category.objects.get(id=pet.categ_id.id).name
                    }
                    })
                data={
                    'access_token':str(access_token),
                    'refresh_token':str(refresh_token),
		            'id':appuser.id,
		            'type':Role.objects.get(id=appuser.role_id.id).name,
		            'first_name':appuser.first_name,
		            'last_name':appuser.last_name,
		            'email':appuser.email,
		            'country':appuser.country,
		            'phone_no':appuser.phone_no,
		            'password':password,
		            'image':'https://petapp.billilo.com'+appuser.profile_img.url if (appuser.profile_img) else '',
		            'pet_detail':pet_detail,
                    'total_posted_post':total_posted_pet,
                    'total_favourite_pet':favourite_pet
                }
                return JsonResponse({"message":"Login Successfully","success":True,'data':data},status=status.HTTP_200_OK)
            else:
                return JsonResponse({"message":"Invalid username and password","success":False},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)