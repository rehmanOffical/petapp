from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from petapp.models import Appuser, userpet, Favourite_Profile
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def add_profile_favourite(request):
    if request.method == 'POST':
        try:
            profile_id = request.POST.get('profile_id')
            favorite = request.POST.get('status')
            favourite_by=request.POST.get('favourite_by')

            # Validate user existence
            if not Appuser.objects.filter(id=profile_id).exists():
                return JsonResponse({"message": "Profile does not exist", "success": False}, status=status.HTTP_400_BAD_REQUEST)
            # Determine favorite status
            status_fave = favorite == "1"

            # Check if a Favourite record already exists
            favorite_obj, created = Favourite_Profile.objects.update_or_create(
                user_id=Appuser.objects.get(id=profile_id),
                favourite_by=favourite_by,
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
