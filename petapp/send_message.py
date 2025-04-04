import requests
from django.conf import settings
from rest_framework import status
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta

def send_fcm_notification(registration_ids, message_title, message_body, fcm_server_key):
    headers = {
        'Authorization': 'Bearer ' + fcm_server_key,
        'Content-Type': 'application/json; UTF-8',
    }

    payload = {
        'message': {
            'token': registration_ids,  # Assuming you are sending to a single token
            'notification': {
                'title': message_title,
                'body': message_body,
            }
        }
    }

    response = requests.post('https://fcm.googleapis.com/v1/projects/notifications-533b6/messages:send', headers=headers, json=payload)

    if response.status_code == 200:
        print("Notification sent successfully")
        return  "Sent Successfully"
    else:
        print(response.json())
        return  "Not Sent Successfully"

