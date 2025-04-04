import firebase_admin
from firebase_admin import credentials, firestore
import google.auth.transport.requests
from google.oauth2 import service_account
import os

SCOPES = ['https://www.googleapis.com/auth/cloud-platform']
def _get_access_token():
  """Retrieve a valid access token that can be used to authorize requests.

  :return: Access token.
  """
  credentials = service_account.Credentials.from_service_account_file(
    'petapi/notifications-533b6-firebase-adminsdk-f3nbz-2f2d848ec8.json', scopes=SCOPES)
  request = google.auth.transport.requests.Request()
  credentials.refresh(request)
  return credentials.token

