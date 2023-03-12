import string
import random


def generate_random_password():

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits

    all = lower + upper + num
    temp = random.sample(all, 10)

    password = "".join(temp)

    return password

def generate_otp():

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits

    all = lower + upper + num
    temp = random.sample(all, 4)

    otp = "".join(temp)

    return otp