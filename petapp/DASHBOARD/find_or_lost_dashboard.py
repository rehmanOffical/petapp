from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from petapp.models import Find_Lost_Pet,category,Appuser
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@csrf_exempt
def find_or_lost_dashboard(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')
            pet_status=request.GET.get('status')
            # Validate if user exists
            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse(
                    {"message": "User does not exist", "success": False},
                    status=status.HTTP_400_BAD_REQUEST
                )
            appuser = Appuser.objects.get(id=user_id)
            # Query userpet with filters, excluding current user's pets
            if pet_status:
            	pet_data = Find_Lost_Pet.objects.filter(status=pet_status).exclude(user_id=appuser)
            else:
            	pet_data = Find_Lost_Pet.objects.all().exclude(user_id=appuser)

            # Prepare response data
            data = []
            for pet in pet_data:
                data.append({
                    'id': pet.id,
                    'name': pet.name,
                    'age': pet.age,
                    'breed': pet.breed,
                    'sex': pet.sex,
                    'color': pet.color,
                    'identity_mark':pet.identity_mark,
                    'status':pet.status,
                    'location': pet.location,
                    'address': pet.address,
                    'whatsapp_no': pet.phone_no,
                    'person_name':pet.person_name,
                    'images': [
                        f"https://petapp.billilo.com/{img}" for img in pet.images
                    ] if pet.images else [],
                    'description': pet.description,
                    'category': pet.categ_id.name,
                    'user': {
                        'id': pet.user_id.id,
                        'first_name': pet.user_id.first_name,
                        'last_name': pet.user_id.last_name,
                        'country': pet.user_id.country,
                        'email': pet.user_id.email,
                        'phone_no': pet.user_id.phone_no,
                        'image': 'https://petapp.billilo.com'+pet.user_id.profile_img.url if pet.user_id.profile_img else ""
                    },
                    'created_at':pet.created_at,
                    'updated_at':pet.updated_at,
                })

            return JsonResponse(
                {"message": "Fetch successful", "success": True, "data": data},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(f"Error in dashboard: {str(e)}")
            return JsonResponse(
                {"message": "Error", "error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        return JsonResponse(
            {"message": "Method not allowed", "success": False},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
