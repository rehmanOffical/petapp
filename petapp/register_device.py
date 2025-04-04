from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from .send_message import send_fcm_notification
from django.views.decorators.csrf import csrf_exempt
from .get_server_key import _get_access_token
import logging

logger = logging.getLogger(__name__)

@csrf_exempt
def notify_user(fcm_token,title,body):
    token = _get_access_token()
    print(fcm_token)
    response = send_fcm_notification(fcm_token, title, body,token)
    return response

