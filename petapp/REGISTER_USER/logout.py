from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from petapp.models import Appuser,logout
from datetime import datetime
from rest_framework import status
import logging

logger=logging.getLogger(__name__)
@csrf_exempt
def user_logout(request):
    if request.method=='POST':
        try:
            user_id=request.POST.get('user_id')
            access_token=request.POST.get('access_token')
            
            if not Appuser.objects.filter(id=user_id):
                return JsonResponse({"message":"User does not exists","success":False},status=status.HTTP_400_BAD_REQUEST)
            if not access_token:
                return JsonResponse({"message":"Access token is required","success":False},status=status.HTTP_400_BAD_REQUEST)
            appuser=Appuser.objects.get(id=user_id)
            Logout=logout.objects.filter(user_id=appuser).delete()
            appuser.logout_at=datetime.now()
            appuser.save()
            return JsonResponse({"message":"Logout Successfully","success":True},status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"message":"Error","error":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message":"Method not allowed","success":False},status=status.HTTP_405_METHOD_NOT_ALLOWED)
