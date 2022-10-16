import os
import random
from dotenv import load_dotenv

from redis import Redis

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site

from allauth.account.adapter import DefaultAccountAdapter



load_dotenv()
REDIS_HOST          = os.getenv('REDIS_HOST')
REDIS_PORT          = os.getenv('REDIS_PORT')
REDIS_DB            = os.getenv('REDIS_DB')
REDIS_PASSWORD      = os.getenv('REDIS_PASSWORD')


r = Redis(
        host    = REDIS_HOST, 
        port    = int(REDIS_PORT), 
        db      = int(REDIS_DB),
        password= REDIS_PASSWORD
    )



class ActivationCode():
    @staticmethod
    def create(id):
        exp = settings.ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS
        key = random.randint(100000, 999999)
        r.lpush(key, id)
        r.expire(key, exp*24*3600)
        return key


class MyAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = get_current_site(request)
        ctx = {
            "user": emailconfirmation.email_address.user,
            "current_site": current_site,
            "key": ActivationCode.create(emailconfirmation.email_address.user.id) # comment this line to disable redis temporarely
        }
        if signup:
            email_template = "account/email/email_confirmation_signup"
        else:
            email_template = "account/email/email_confirmation_message"
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)