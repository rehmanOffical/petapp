from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from petapp.models import Appuser, userpet, Favourite
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def add_favourite(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('user_id')
            pet_id = request.POST.get('pet_id')
            favorite = request.POST.get('status')

            # Validate user existence
            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message": "User does not exist", "success": False}, status=status.HTTP_400_BAD_REQUEST)

            # Validate pet existence
            if not userpet.objects.filter(id=pet_id).exists():
                return JsonResponse({"message": "Pet not found", "success": False}, status=status.HTTP_400_BAD_REQUEST)

            # Determine favorite status
            status_fave = favorite == "1"

            # Check if a Favourite record already exists
            favorite_obj, created = Favourite.objects.update_or_create(
                user_id=Appuser.objects.get(id=user_id),
                pet_id=userpet.objects.get(id=pet_id),
                defaults={"status": status_fave}
            )

            if created:
                message = "Added to favourite"
            else:
                message = "Removed to favourite"

            return JsonResponse({"message": message, "success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error in add_favourite: {str(e)}")
            return JsonResponse({"message": "Error", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message": "Method not allowed", "success": False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
