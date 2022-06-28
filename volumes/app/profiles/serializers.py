import os
from dotenv import load_dotenv

from rest_framework import serializers
from profiles.models import Profile
from profiles.sendsms import KavenegarAPI



load_dotenv()
KAVEHNEGAR_APIKEY = os.getenv('KAVEHNEGAR_APIKEY')


class ProfileSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):

        l = [
            "addressVerified",
            "cellPhoneNumberVerified",
            "landingPhoneNumberVerified",
            "signedContract",
            "payedMemmber",
            "isEnable",
            "createTime",
            "paymentTime"
            "expirationTime"
        ]

        d = {
            "address"            : "addressVerified",
            "cellPhoneNumber"    : "cellPhoneNumberVerified",
            "landingPhoneNumber" : "landingPhoneNumberVerified"
        }

        if "cellPhoneNumber" in self.validated_data:
            kanenegar = KavenegarAPI(apikey=KAVEHNEGAR_APIKEY)
            kanenegar.sms_send(self.validated_data["cellPhoneNumber"])

        [self.validated_data.pop(i) for i in l  if i in self.validated_data]
        [(self.validated_data.__setitem__(d[k], False),
        self.validated_data.__setitem__("isEnable", False)) \
            for k in d.keys() if k in self.validated_data]

        return super().save(**kwargs)

    class Meta:
        model  = Profile
        fields = "__all__"