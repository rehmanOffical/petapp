from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from petapp.models import Appuser, Role
from rest_framework import status
from datetime import datetime
from petapp.manage_otp import send_email, send_register_email, Generate_otp
from django.conf import settings
import logging
import os
import time
import threading

logger = logging.getLogger(__name__)

generated_otp = None
is_generated = False
is_register = False

def make_otp_expire(otp):
    global is_generated
    time.sleep(300)  # OTP expires after 5 minutes
    is_generated = False

@csrf_exempt
def register_user(request):
    global generated_otp, is_generated, is_register
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            country = request.POST.get('country', '')
            phone_no = request.POST.get('phone_no', '')
            password = request.POST.get('password', '')
            confirm_password = request.POST.get('confirm_password', '')
            profile_img = request.FILES.get('profile_img')
            role_id = request.POST.get('role_id', 2)  # Default role_id is 2 if not provided

            if not (first_name and last_name and email and country and phone_no and password and confirm_password):
                return JsonResponse({"message": "Please fill all required fields", "success": False}, status=status.HTTP_400_BAD_REQUEST)

            if Appuser.objects.filter(email=email).exists():
                return JsonResponse({"message": "User already exists", "success": False}, status=status.HTTP_400_BAD_REQUEST)

            if password != confirm_password:
                return JsonResponse({"message": "Password and Confirm Password do not match", "success": False}, status=status.HTTP_400_BAD_REQUEST)

            if not is_generated:
                generated_otp = Generate_otp()
                is_generated = True
                name = f"{first_name} {last_name}"
                send_register_email(email, generated_otp, name)
                threading.Thread(target=make_otp_expire, args=(generated_otp,)).start()
                return JsonResponse({"message": "OTP successfully sent to your email", "success": True}, status=status.HTTP_200_OK)

            if is_register:
                appuser = Appuser(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    country=country,
                    phone_no=phone_no,
                    password=make_password(password),
                    created_at=datetime.now(),
                    updated_at=datetime.now(),
                    profile_img=profile_img,
                    role_id=Role.objects.get(id=role_id)
                )
                appuser.save()

                result = {
                    "id": appuser.id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "country": country,
                    "phone_no": phone_no
                }

                is_generated = False
                generated_otp = None
                is_register = False

                return JsonResponse({"message": "User registered successfully", "success": True, "data": result}, status=status.HTTP_201_CREATED)

            return JsonResponse({"message": "OTP already sent", "success": True}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"message": "Error", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message": "Method not allowed", "success": False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@csrf_exempt
def verify_register_otp(request):
    global is_register
    if request.method == 'POST':
        try:
            otp = request.POST.get('otp', '')
            if not otp:
                return JsonResponse({"message": "Please enter OTP", "success": False}, status=status.HTTP_400_BAD_REQUEST)

            if otp != generated_otp:
                return JsonResponse({"message": "Invalid OTP", "success": False}, status=status.HTTP_400_BAD_REQUEST)

            if not is_generated:
                return JsonResponse({"message": "OTP has expired", "success": False}, status=status.HTTP_400_BAD_REQUEST)

            is_register = True
            return JsonResponse({"message": "OTP verified successfully", "success": True}, status=status.HTTP_200_OK)

        except Exception as e:
            return JsonResponse({"message": "Error", "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return JsonResponse({"message": "Method not allowed", "success": False}, status=status.HTTP_405_METHOD_NOT_ALLOWED)