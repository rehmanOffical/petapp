from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .REGISTER_USER.register_user  import register_user,verify_register_otp
from .REGISTER_USER.update_user import update_user
from .REGISTER_USER.login import login
from .REGISTER_USER.logout import user_logout
from .CATEGEORY.add_categeory import add_categeory
from .CATEGEORY.get_category import get_category
from .PET.add_pet import add_pet
from .PET.update_pet import update_pet
from .PET.get_pet import get_pet
from .PET.delete_pet import delete_pet
from .DASHBOARD.dashboard import dashboard
from .FAVOURITE.add_to_favourite import add_favourite
from .FAVOURITE.get_favorite_data import get_favourite
from .FIND_OR_LOST.add_find_or_lost import add_find_or_lost
from .FIND_OR_LOST.update_find_or_lost import update_find_or_lost
from .FIND_OR_LOST.get_find_or_lost import get_find_or_lost
from .FIND_OR_LOST.delete_find_or_lost import delete_find_or_lost
from .DASHBOARD.find_or_lost_dashboard import find_or_lost_dashboard
from .ANIMAL_SHELLTER.add_animal_shellter import add_animal_shellter
from .ANIMAL_SHELLTER.update_animal_shellter import update_animal_shellter
from .ANIMAL_SHELLTER.get_animal_shellter import get_shellter_detail
from .ANIMAL_SHELLTER.delete_animal_shellter import delete_animal_shellter
from .VET_CLINIC.add_vet_clinic import add_vet_clinic
from .VET_CLINIC.update_vet_clinic import update_vet_clinic
from .VET_CLINIC.get_vet_clinic import get_vet_clinic
from .VET_CLINIC.delete_vet_clinic import delete_vet_clinic
from .FCM.take_fcm import take_fcm_token
from .POST_ADD.create_add import create_add
from .POST_ADD.update_ad import update_ad
from .POST_ADD.get_ad import get_ad
from .POST_ADD.delete_ad import delete_ad
from .SEND_NOTIFICATIONS.send_notification import forward_notification
from .PROFILE.get_profile import get_profile
from .PROFILE.make_profile_fav import add_profile_favourite
from .PROFILE.get_fav_profile  import get_profile_favourite
from .CATEGEORY.add_sub_category import add_sub_categeory
from .CATEGEORY.get_sub_category import get_sub_category
urlpatterns = [
    path('register-user/',register_user),
    path('update-user/',update_user),
    path('login/',login),
    path('logout/',user_logout),
    path('add-category/',add_categeory),
    path('get-category/',get_category),
    path('add-pet/',add_pet),
    path('update-pet/',update_pet),
    path('get-pet/',get_pet),
    path('delete-pet/',delete_pet),
    path('dashboard/',dashboard),
    path('add-to-favorite/',add_favourite),
    path('get-favorite/',get_favourite),
    path('add-find-lost/',add_find_or_lost),
    path('update-find-lost/',update_find_or_lost),
    path('get_find_or_lost/',get_find_or_lost),
    path('delete-find-lost/',delete_find_or_lost),
    path('find-lost-dashboard/',find_or_lost_dashboard),
    path('add-animal-shellter/',add_animal_shellter),
    path('update-animal-shellter/',update_animal_shellter),
    path('get-animal-shellter/',get_shellter_detail),
    path('delete-animal-sheltter/',delete_animal_shellter),
    path('add-vet-clinic/',add_vet_clinic),
    path('update-vet-clinic/',update_vet_clinic),
    path('get-vet-clinic/',get_vet_clinic),
    path('delete-vet-clinic/',delete_vet_clinic),
    path('take-fcm-token/',take_fcm_token),
    path('create-ad/',create_add),
    path('update-ad/',update_ad),
    path('get-ad/',get_ad),
    path('delete-ad/',delete_ad),
    path('send-notification/',forward_notification),
    path('verify-otp/',verify_register_otp),
    path('get-profile/',get_profile),
    path('make-profile-fav/',add_profile_favourite),
    path('get-profile-fav/',get_profile_favourite),
    path('add-sub-category/',add_sub_categeory),
    path('get-sub-category/',get_sub_category)
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)