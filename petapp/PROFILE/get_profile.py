from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from petapp.models import Appuser,logout,userpet,category,Role,Favourite,Find_Lost_Pet
from datetime import datetime
from rest_framework import status
import logging

def get_profile(request):
    if request.method=='GET':
        try:
            user_id=request.GET.get('user_id')
            
            if not user_id:
                return JsonResponse({"message":"Please give user id","success":False},status=status.HTTP_400_BAD_REQUEST)
            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message":"User not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            appuser=Appuser.objects.get(id=user_id)
            total_favourite=Favourite.objects.filter(user_id=appuser).count()
            user_pet=userpet.objects.filter(user_id=appuser).count()
            find_lost_user_pet=Find_Lost_Pet.objects.filter(user_id=appuser).count()
            total_ads=user_pet+find_lost_user_pet
            data=[]
            posted_pet=userpet.objects.filter(user_id=appuser).order_by('-id')
            find_lost_posted=Find_Lost_Pet.objects.filter(user_id=appuser).order_by('-id')
            data.append({
                'id':appuser.id,
                'name':appuser.first_name+" "+appuser.last_name,
                'country':appuser.country,
                'email':appuser.email,
                'phone_no':appuser.phone_no,
                'created_at':appuser.created_at,
                'updated_at':appuser.updated_at,
                'profile_img':'https://petapp.billilo.com'+appuser.profile_img.url if appuser.profile_img else '',
                'post_pet':[{'id':pet.id,
                             'name':pet.name,
                             'age':pet.age,
                             'breed':pet.breed,
                             'sex':pet.sex,
                             'price':pet.price,
                             'status':pet.status,
                             'location':pet.location,
                             'address':pet.address,
                             'whatsapp_no':pet.whatsapp_no,
                             'desc':pet.description,
                             'created_at':pet.created_at,
                             'updated_at':pet.updated_at,
                             'category':pet.categ_id.name,
                             'images':['https://petapp.billilo.com/'+img for img in pet.images]} for pet in posted_pet],
                'find_lost_pet':[{'id':pets.id,
                                  'name':pets.name,
                                  'age':pets.age,
                                  'sex':pets.sex,
                                  'breed':pets.breed,
                                  'color':pets.color,
                                  'identity_mark':pets.identity_mark,
                                  'status':pets.status,
                                  'person_name':pets.person_name,
                                  'address':pets.address,
                                  'loction':pets.location,
                                  'phone_no':pets.phone_no,
                                  'desc':pets.description,
                                  'created_at':pets.created_at,
                                  'updated_at':pets.updated_at,
                                  'category':pets.categ_id.name,
                                  'images':['https://petapp.billilo.com/'+img for img in pets.images]} for pets in find_lost_posted],
                'total_favourite':total_favourite,
                'total_listed':total_ads,
            })
            return JsonResponse({"message":"Fetch successfully","success":True,'data':data},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)