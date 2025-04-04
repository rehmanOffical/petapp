import random
from django.conf import settings
from django.core.mail import send_mail
from petapi.settings import set_email_config

def Generate_otp():
    # Generate a 4-digit OTP
    otp = ''.join(random.sample('0123456789', 4))
    print(f"Generated 4-digit OTP: {otp}")
    return otp

def send_email(email, otp, name, use_primary):
    email_setting = set_email_config(primary=use_primary)
    settings.EMAIL_HOST_USER = email_setting["EMAIL_HOST_USER"]
    settings.EMAIL_HOST_PASSWORD = email_setting["EMAIL_HOST_PASSWORD"]
    print(settings.EMAIL_HOST_USER)
    print(settings.EMAIL_HOST_PASSWORD)
    
    subject = "AI Poultry Farm app - Reset Password OTP"
    message = f"""Dear {name},

We received a request to reset the password for your AI Poultry Form account. Please use the One-Time Password (OTP) below to proceed with resetting your password.

Your OTP: {otp}

This OTP is valid for the next 5 minutes. If you did not request a password reset, please ignore this email or contact our support team immediately.

For security reasons, please do not share this OTP with anyone.

Thank you for using AI Poultry Farm.

Regards,
AI Poultry Farm
www.hisabkarlay.com
WhatsApp or Call us: +923269498569"""
    
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_form, recipient_list)
    return True

def send_register_email(email, otp, name):
    email_setting = set_email_config(primary=True)
    settings.EMAIL_HOST_USER = email_setting["EMAIL_HOST_USER"]
    settings.EMAIL_HOST_PASSWORD = email_setting["EMAIL_HOST_PASSWORD"]
    print(settings.EMAIL_HOST_USER)
    print(settings.EMAIL_HOST_PASSWORD)
    
    subject = "Billilo - New Account Registration"
    message = f"""Dear {name},

Please use the One-Time Password (OTP) below to proceed with account registration.

Your OTP: {otp}

This OTP is valid for the next 5 minutes. If you did not request a password reset, please ignore this email or contact our support team immediately.

For security reasons, please do not share this OTP with anyone.

Regards,
Billilo"""
    
    email_form = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_form, recipient_list)
    return True
