import os
from dotenv import load_dotenv

from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication

from profiles.models import Profile
from profiles.serializers import ProfileSerializer
from profiles.sendsms import KavenegarAPI

from redis import Redis



load_dotenv()
KAVEHNEGAR_APIKEY = os.getenv('KAVEHNEGAR_APIKEY')

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


class UserProfile(APIView):
    """
    get-post-patch-delete profile
    /profile/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, userId):
        try:
            return Profile.objects.get(user__id=userId)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        profile = self.get_object(userId=request.user.id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id
        serializer = ProfileSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        profile = self.get_object(userId=request.user.id)
        data = request.data       
        data['user'] = request.user.id
        serializer = ProfileSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        profile = self.get_object(userId=request.user.id)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SendCellphoneToken(APIView):
    """
    post token to verify cellphone number
    /profile/sendCellphoneToken/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, userId):
        try:
            return Profile.objects.get(user__id=userId)
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):
        profile = self.get_object(userId=request.user.id)
        cellphonenumber = profile.cellPhoneNumber.as_national.replace(" ", "")
        kanenegar = KavenegarAPI(apikey=KAVEHNEGAR_APIKEY)
        kanenegar.sms_send(cellphonenumber)
        return Response({"detail": "Verification token sent."}, status=status.HTTP_200_OK)


class VerifyCellphone(APIView):
    """
    post token to verify cellphone number
    /profile/verify-cellphone/
    """
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_number(self,token):
        return r.lpop(token).decode()

    def post(self, request, *args, **kwargs):
        data = request.data
        if "token" in data:
            token  = data["token"]
            try:
                number = self.get_number(token)
                number = number[:4] + ' ' + number[4:7] + ' ' + number[7:]
                # get_object_or_404(Profile,cellPhoneNumber=number).update(cellPhoneNumberVerified=True)
                obj = Profile.objects.filter(cellPhoneNumber=number).update(cellPhoneNumberVerified=True)
                if not obj:
                    return Response({"detail": "cellphone number not found!"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"detail": "cellphone number verification done."}, status=status.HTTP_200_OK)
            except:
                return Response({"detail": "invalid cellphone-token!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({"detail": "enter your token"}, status=status.HTTP_400_BAD_REQUEST)