from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.http import JsonResponse
from rest_framework import status
from petapp.models import Appuser, fcm_token
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def take_fcm_token(request):
    if request.method == 'POST':
        try:
            user_id = request.POST.get('user_id')
            token = request.POST.get('token')
            enable=request.POST.get('enable')
            if not Appuser.objects.filter(id=user_id).exists():
                return JsonResponse({"message": "User does not exist", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            if enable=="0":
                enable=False
            elif enable=="1":
                enable=True
            muser = Appuser.objects.get(id=user_id)
            if not fcm_token.objects.filter(token=token, user_id=muser).exists():
                # Uncomment the following line if you want to notify when a token already exists
                # return JsonResponse({"message": "This token already exists", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                myuser=Appuser.objects.get(id=user_id)
                Token = fcm_token(token=token, user_id=myuser,enable=enable)
                Token.save()
                return JsonResponse({"message": "Token saved successfully", "success": True}, status=status.HTTP_200_OK)
            return JsonResponse({"message": "This token already exists", "success": False}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return JsonResponse({"message": "Error", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message": "Invalid method", "success": False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
