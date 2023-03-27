import string
import random
from django.core.mail import send_mail
from django.conf import settings


def generate_random_password():

    num = string.digits

    temp = random.sample(num, 10)

    password = "".join(temp)

    return password

def generate_otp():

    num = string.digits

    temp = random.sample(num, 6)

    otp = "".join(temp)

    return otp


def send_mail(subject,message,user):
    subject = subject
    message = message
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email, ]
    send_mail( subject, message, email_from, recipient_list )