# import os
# from dotenv import load_dotenv

# from django.conf import settings
# from django.utils.encoding import force_str
# from django.utils.translation import gettext_lazy as _
# from django.contrib.auth.forms import SetPasswordForm
# from django.contrib.auth import get_user_model

from rest_framework import serializers
# from rest_framework.exceptions import ValidationError

# if 'allauth' in settings.INSTALLED_APPS:
#     from dj_rest_auth.forms import AllAuthPasswordResetForm

# from redis import Redis




# load_dotenv()

# REDIS_HOST          = os.getenv('REDIS_HOST')
# REDIS_PORT          = os.getenv('REDIS_PORT')
# REDIS_DB            = os.getenv('REDIS_DB')
# REDIS_PASSWORD      = os.getenv('REDIS_PASSWORD')


# r = Redis(
#         host    = REDIS_HOST, 
#         port    = int(REDIS_PORT), 
#         db      = int(REDIS_DB),
#         password= REDIS_PASSWORD
#     )

# Get the UserModel
# UserModel = get_user_model()


# class PasswordResetSerializer(serializers.Serializer):
#     """
#     Serializer for requesting a password reset e-mail.
#     """
#     email = serializers.EmailField()

#     reset_form = None

#     @property
#     def password_reset_form_class(self):
#         if 'allauth' in settings.INSTALLED_APPS:
#             return AllAuthPasswordResetForm
#         else:
#             return PasswordResetForm

#     def get_email_options(self):
#         """Override this method to change default e-mail options"""
#         return {}

#     def validate_email(self, value):
#         # Create PasswordResetForm with the serializer
#         self.reset_form = self.password_reset_form_class(data=self.initial_data)
#         if not self.reset_form.is_valid():
#             raise serializers.ValidationError(self.reset_form.errors)

#         return value

#     def save(self):
#         if 'allauth' in settings.INSTALLED_APPS:
#             from allauth.account.forms import default_token_generator
#         else:
#             from django.contrib.auth.tokens import default_token_generator

#         request = self.context.get('request')
#         # Set some values to trigger the send_email method.
#         opts = {
#             'use_https': request.is_secure(),
#             'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
#             'request': request,
#             'token_generator': default_token_generator,
#         }

#         opts.update(self.get_email_options())
#         self.reset_form.save(**opts)



# class PasswordResetConfirmSerializer(serializers.Serializer):
#     """
#     Serializer for confirming a password reset attempt.
#     """
#     new_password1 = serializers.CharField(max_length=128)
#     new_password2 = serializers.CharField(max_length=128)
#     uid = serializers.CharField()
#     token = serializers.CharField()

#     set_password_form_class = SetPasswordForm

#     _errors = {}
#     user = None
#     set_password_form = None

#     def custom_validation(self, attrs):
#         pass

#     def validate(self, attrs):
#         if 'allauth' in settings.INSTALLED_APPS:
#             from allauth.account.forms import default_token_generator
#             from allauth.account.utils import url_str_to_user_pk as uid_decoder
#         else:
#             from django.contrib.auth.tokens import default_token_generator
#             from django.utils.http import urlsafe_base64_decode as uid_decoder

#         # Decode the uidb64 (allauth use base36) to uid to get User object
#         try:
#             uid = force_str(uid_decoder(attrs['uid']))
#             self.user = UserModel._default_manager.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
#             raise ValidationError({'uid': ['Invalid value']})

#         if not default_token_generator.check_token(self.user, attrs['token']):
#             raise ValidationError({'token': ['Invalid value']})

#         self.custom_validation(attrs)
#         # Construct SetPasswordForm instance
#         self.set_password_form = self.set_password_form_class(
#             user=self.user, data=attrs,
#         )
#         if not self.set_password_form.is_valid():
#             raise serializers.ValidationError(self.set_password_form.errors)

#         return attrs

#     def save(self):
#         return self.set_password_form.save()











class EmailPasswordResetSerializer(serializers.Serializer):
    """
    Serializer for requesting a password reset e-mail.
    """
    email = serializers.EmailField()


class EmailPasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset attempt.
    """
    token         = serializers.CharField(max_length=6)
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)