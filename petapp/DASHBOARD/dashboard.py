from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from petapp.models import userpet, Appuser,category,Favourite
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@csrf_exempt
def dashboard(request):
    if request.method == 'GET':
        try:
            user_id = request.GET.get('user_id')
            name = request.GET.get('name')
            start_price = request.GET.get('start_price')
            end_price = request.GET.get('end_price')
            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            categ=request.GET.get('category')
            pet_status=request.GET.get('status')
            # Validate if user exists
            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse(
                    {"message": "User does not exist", "success": False},
                    status=status.HTTP_400_BAD_REQUEST
                )

            appuser = Appuser.objects.get(id=user_id)
            dashboard_filter = {'delete':False}
            if pet_status:
                dashboard_filter={'status':pet_status}
            # Filter by name
            if name:
                dashboard_filter['name__icontains'] = name
            if categ:
                dashboard_filter['categ_id']=category.objects.get(id=categ)
            # Filter by price range
            if start_price or end_price:
                try:
                    if start_price and end_price:
                        start_price = float(start_price)
                        end_price = float(end_price)
                        dashboard_filter['price__range'] = [start_price, end_price]
                    elif start_price:
                        start_price = float(start_price)
                        dashboard_filter['price__gte'] = start_price
                    elif end_price:
                        end_price = float(end_price)
                        dashboard_filter['price__lte'] = end_price
                except ValueError:
                    return JsonResponse(
                        {"message": "Invalid price format", "success": False},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Filter by created_at range
            if start_date or end_date:
                try:
                    if start_date and end_date:
                        start_date = datetime.strptime(start_date, "%Y-%m-%d")
                        end_date = datetime.strptime(end_date, "%Y-%m-%d")
                        dashboard_filter['created_at__range'] = [start_date, end_date]
                    elif start_date:
                        start_date = datetime.strptime(start_date, "%Y-%m-%d")
                        dashboard_filter['created_at__gte'] = start_date
                    elif end_date:
                        end_date = datetime.strptime(end_date, "%Y-%m-%d")
                        dashboard_filter['created_at__lte'] = end_date
                except ValueError:
                    return JsonResponse(
                        {"message": "Invalid date format", "success": False},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Query userpet with filters, excluding current user's pets
            pet_data = userpet.objects.filter(**dashboard_filter).exclude(user_id=appuser)

            # Prepare response data
            data = []
            for pet in pet_data:
                data.append({
                    'id': pet.id,
                    'name': pet.name,
                    'age': pet.age,
                    'breed': pet.breed,
                    'sex': pet.sex,
                    'status':pet.status,
                    'price': pet.price,
                    'location': pet.location,
                    'address': pet.address,
                    'whatsapp_no': pet.whatsapp_no,
                    'images': [
                        f"https://petapp.billilo.com/{img}" for img in pet.images
                    ] if pet.images else [],
                    'description': pet.description,
                    'category': pet.categ_id.name,
                    'favourite': Favourite.objects.get(pet_id=pet,user_id=appuser).status if Favourite.objects.filter(pet_id=pet,user_id=appuser).exists() else False,
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