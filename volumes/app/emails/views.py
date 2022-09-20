import os
from redis import Redis
from dotenv import load_dotenv
from random import randint, randrange

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import NotAcceptable

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters

from allauth.account.models import EmailAddress

# from emails.serializers import PasswordResetSerializer, PasswordResetConfirmSerializer, 
from emails.serializers import EmailPasswordResetConfirmSerializer, EmailPasswordResetSerializer


load_dotenv()
REDIS_HOST          = os.getenv('REDIS_HOST')
REDIS_PORT          = os.getenv('REDIS_PORT')
REDIS_DB            = os.getenv('REDIS_DB')
REDIS_PASSWORD      = os.getenv('REDIS_PASSWORD')
EMAILHOSTUSER       = os.getenv('EMAILHOSTUSER')


r = Redis(
        host    = REDIS_HOST, 
        port    = int(REDIS_PORT), 
        db      = int(REDIS_DB),
        password= REDIS_PASSWORD
    )

UserModel = get_user_model()


sensitive_post_parameters_m = method_decorator(
    sensitive_post_parameters(
        'password', 'old_password', 'new_password1', 'new_password2',
    ),
)



class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get_user_id(self, key):
        return r.lpop(key).decode()

    def post(self, request):
        data = request.data
        if "key" in data:
            key  = data["key"]
            try:
                user_id = self.get_user_id(key)
                obj = EmailAddress.objects.filter(user_id=user_id).update(verified=True)
                if not obj:
                    return Response({"detail": "User not found!"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"detail": "Email verification done."}, status=status.HTTP_200_OK)
            except:
                return Response({"detail": "invalid key!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({"detail": "enter your key"}, status=status.HTTP_400_BAD_REQUEST)



# class PasswordResetView(GenericAPIView):
#     """
#     Calls Django Auth PasswordResetForm save method.

#     Accepts the following POST parameters: email
#     Returns the success/fail message.
#     """
#     serializer_class = PasswordResetSerializer
#     permission_classes = (AllowAny,)
#     throttle_scope = 'dj_rest_auth'

#     def post(self, request, *args, **kwargs):
#         # Create a serializer with request.data
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         serializer.save()
#         # Return the success message with OK HTTP status
#         return Response(
#             {'detail': _('Password reset e-mail has been sent.')},
#             status=status.HTTP_200_OK,
#         )



# class PasswordResetConfirmView(GenericAPIView):
#     """
#     Password reset e-mail link is confirmed, therefore
#     this resets the user's password.

#     Accepts the following POST parameters: token, uid,
#         new_password1, new_password2
#     Returns the success/fail message.
#     """
#     serializer_class = PasswordResetConfirmSerializer
#     permission_classes = [AllowAny]
#     throttle_scope = 'dj_rest_auth'

#     @sensitive_post_parameters_m
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {'detail': _('Password has been reset with the new password.')},
#         )



class EmailPasswordResetView(APIView):
    """
    Calls Django Auth PasswordResetForm save method.

    Accepts the following POST parameters: email
    Returns the success/fail message.
    """
    serializer_class = EmailPasswordResetSerializer
    permission_classes = (AllowAny,)
    throttle_scope = 'dj_rest_auth'

    def post(self, request, *args, **kwargs):
        data = request.data
        if "email" in data:
            useremail = data["email"]
            try:
                validate_email(useremail)
            except ValidationError as e:
                raise NotAcceptable(detail=e, code=406)
            token = randrange(100000, 999999)
            r.lpush(token, useremail)
            r.expire(token, 600)
            subject = "Password Reset Requested"
            c = {
					"email":useremail,
					'site_name': 'my.jirnal.ir',
					'protocol': 'https',
                    'token': token
					}
            emailtemp = render_to_string("account/email/email_password_reset_message.txt", c)
            try:
                send_mail(subject, emailtemp, EMAILHOSTUSER , [useremail], fail_silently=False)
            except BadHeaderError:
                return Response({"detail": "Invalid header found."}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'detail': _('Password reset e-mail has been sent.')},status=status.HTTP_200_OK)
        else:
            return Response({"detail": "enter your email"}, status=status.HTTP_400_BAD_REQUEST)



class EmailPasswordResetConfirmView(GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = EmailPasswordResetConfirmSerializer
    permission_classes = [AllowAny]
    throttle_scope = 'dj_rest_auth'

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_email(self,token):
        return r.lrange(token,0,0)[0].decode()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            email = self.get_email(request.data['token'])
            user = UserModel._default_manager.get(email=email)
            data = {
                'new_password1': request.data['new_password1'],
                'new_password2': request.data['new_password2']
            }
            form = SetPasswordForm(user, data)
            if form.is_valid():
                form.save()
                return Response({'detail': _('Password has been reset with the new password.')})
            return Response({'detail': str(form.errors)})
        except:
            return Response({"detail": _("invalid email-token!")}, status=status.HTTP_406_NOT_ACCEPTABLE)



class CheckEmailAddressView(APIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    permission_classes = [AllowAny]
    throttle_scope = 'dj_rest_auth'

    # def get_serializer_class(self):
    #     return None

    def post(self, request, *args, **kwargs):
        data=request.data
        if "email" in data:
            try:
                EmailAddress.objects.get(email=data["email"])
                return Response({"detail": _("OK!")}, status=status.HTTP_404_NOT_FOUND)
            except EmailAddress.DoesNotExist:
                return Response({"detail": _("Entered email not found!")}, status=status.HTTP_404_NOT_FOUND)
    
        return Response({'detail': _('Please insert email address.')},)
        