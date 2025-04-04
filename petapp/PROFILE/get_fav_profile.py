from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from petapp.models import Appuser, userpet, Favourite_Profile,Find_Lost_Pet
import logging

ogger = logging.getLogger(__name__)

@csrf_exempt
def get_profile_favourite(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')
            
            if not user_id:
                return JsonResponse({"message": "User id required", "success": False}, status=status.HTTP_400_BAD_REQUEST)
            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message": "User does not exist", "success": False}, status=status.HTTP_400_BAD_REQUEST)
            if not Favourite_Profile.objects.filter(favourite_by=user_id, status=True).exists():
                return JsonResponse({"message": "Fetch successfully", "success": True, 'data': []}, status=status.HTTP_200_OK)
            
            profiles = Favourite_Profile.objects.filter(favourite_by=user_id, status=True)
            data = []
            
            for profile in profiles:
                user_pet = userpet.objects.filter(user_id=profile.user_id)
                find_lost = Find_Lost_Pet.objects.filter(user_id=profile.user_id)
                data.append({
                    'id': profile.id,
                    'status': profile.status,
                    'user_detail': {
                        'id': profile.user_id.id,
                        'name': profile.user_id.first_name + " " + profile.user_id.last_name,
                        'country': profile.user_id.country,
                        'email': profile.user_id.email,
                        'phone_no': profile.user_id.phone_no,
                        'created_at': profile.user_id.created_at,
                        'updated_at': profile.user_id.updated_at,
                        'profile_img': 'https://petapp.billilo.com' + profile.user_id.profile_img.url if profile.user_id.profile_img else '',
                        'post_pet': [{
                            'id': pet.id,
                            'name': pet.name,
                            'age': pet.age,
                            'breed': pet.breed,
                            'sex': pet.sex,
                            'price': pet.price,
                            'status': pet.status,
                            'location': pet.location,
                            'address': pet.address,
                            'whatsapp_no': pet.whatsapp_no,
                            'desc': pet.description,
                            'created_at': pet.created_at,
                            'updated_at': pet.updated_at,
                            'category': pet.categ_id.name,
                            'images': ['https://petapp.billilo.com/' + img for img in pet.images]
                        } for pet in user_pet],
                        'find_lost_pet': [{
                            'id': pets.id,
                            'name': pets.name,
                            'age': pets.age,
                            'sex': pets.sex,
                            'breed': pets.breed,
                            'color': pets.color,
                            'identity_mark': pets.identity_mark,
                            'status': pets.status,
                            'person_name': pets.person_name,
                            'address': pets.address,
                            'loction': pets.location,
                            'phone_no': pets.phone_no,
                            'desc': pets.description,
                            'created_at': pets.created_at,
                            'updated_at': pets.updated_at,
                            'category': pets.categ_id.name,
                            'images': ['https://petapp.billilo.com/' + img for img in pets.images]
                        } for pets in find_lost],
                    }
                })
            
            return JsonResponse({"message": "Fetch successfully", "success": True, 'data': data}, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error in get_profile_favourite: {str(e)}")
            return JsonResponse({"message": "Error", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message": "Method not allowed", "success": False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)