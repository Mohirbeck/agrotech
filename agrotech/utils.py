import requests
import time
from django.conf import settings
import random
from django.core.mail import send_mail
from agrotech.models import EmailCode, EmailAttempt
from datetime import datetime, timedelta
from django.core.exceptions import SuspiciousOperation
from django.db.models import F


def email_code():
    return str(random.randint(100000, 999999))


def send_email_code(request, email):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    ip_count = EmailCode.objects.filter(ip=ip).count()
    if ip_count > 1000:
        raise SuspiciousOperation("Over limit")

    email_count = EmailCode.objects.filter(email=email).count()
    if email_count > 1000:
        raise SuspiciousOperation("Over limit")

    code = email_code()

    model = EmailCode()
    model.ip = ip
    model.email = email
    model.code = code
    model.expire_at = datetime.now() + timedelta(minutes=10)
    model.save()

    send_email(email, "Tasdiqlash kodi " + code)
    return code


def validate_email_code(email, code):
    try:
        obj = EmailAttempt.objects.get(email=email)
        if obj.counter >= 1000:
            return False

        obj.counter = F('counter') + 1
    except EmailAttempt.DoesNotExist:
        obj = EmailAttempt(email=email, counter=1)

    obj.last_attempt_at = datetime.now()
    obj.save()

    codes = EmailCode.objects.filter(email=email, expire_at__gt=datetime.now()).all()

    for row in codes:
        if row.code == code:
            return True

    return False


def send_email(email, text):
    print(type(text))
    print(type(settings.EMAIL_HOST_USER))
    print(type(email))

    try:
        send_mail(
            'Code',
            text,
            settings.EMAIL_HOST_USER,
            [email], fail_silently=False
        )
        print('email sending')
    except Exception as e:
        print(e)
        print('ishlamadi')
        return False

    return True