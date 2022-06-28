import os
from dotenv import load_dotenv
from cryptocode import encrypt,decrypt

from django.contrib.auth.models import User

from rest_framework import serializers

from profiles.models import Profile
from keysecrets.models import Secret
from userstrategies.models import UserStrategy

from phonenumber_field.modelfields import PhoneNumberField



load_dotenv()
APIKEYPASS = os.getenv('APIKEYPASS')
SECKEYPASS = os.getenv('SECKEYPASS')



class SecretStrategySerializer(serializers.Serializer):
    walletName                  = serializers.CharField(required=False)
    apiKey                      = serializers.CharField(required=False)
    secretKey                   = serializers.CharField(required=False)
    createTime                  = serializers.DateTimeField(required=False)
    strategy                    = serializers.CharField(required=False)
    symbol                      = serializers.CharField(required=False)
    margin                      = serializers.FloatField(required=False)
    totallSL                    = serializers.FloatField(required=False)
    size                        = serializers.CharField(required=False)
    isActive                    = serializers.BooleanField(required=False)
    baseCurrency                = serializers.CharField(required=False)
    leverage                    = serializers.IntegerField(required=False)
    marginType                  = serializers.CharField(required=False)
    positionMode                = serializers.CharField(required=False)
    timeInForce                 = serializers.CharField(required=False)
    workingType                 = serializers.CharField(required=False)
    priceProtect                = serializers.CharField(required=False)
    createTime                  = serializers.DateTimeField(required=False)
    deactivateTime              = serializers.DateTimeField(required=False)

    # def to_representation(self, data):
    #     data = super().to_representation(data)
    #     data['apiKey']    = decrypt(data['apiKey'], APIKEYPASS)
    #     data['secretKey'] = decrypt(data['secretKey'], SECKEYPASS)
    #     return data


# class UserProfileSerializer(serializers.Serializer):    
#     username                    = serializers.CharField()
#     first_name                  = serializers.CharField(allow_blank=True)
#     last_name                   = serializers.CharField(allow_blank=True)
#     email                       = serializers.CharField()
#     is_superuser                = serializers.BooleanField()
#     is_staff                    = serializers.BooleanField()
#     is_active                   = serializers.BooleanField()
#     date_joined                 = serializers.DateTimeField()
#     last_login                  = serializers.DateTimeField()
#     image                       = serializers.ImageField()
#     dateOfBirth                 = serializers.DateTimeField(allow_null=True)
#     address                     = serializers.CharField(allow_null=True)
#     addressVerified             = serializers.BooleanField()
#     cellPhoneNumber             = PhoneNumberField()
#     cellPhoneNumberVerified     = serializers.BooleanField()
#     landingPhoneNumber          = PhoneNumberField(null=True)
#     landingPhoneNumberVerified  = serializers.BooleanField()
#     signedContract              = serializers.BooleanField()
#     payedMemmber                = serializers.BooleanField()
#     expirationTime              = serializers.DateTimeField()
#     isEnable                    = serializers.BooleanField()
#     createTime                  = serializers.DateTimeField()
#     isActive                    = serializers.BooleanField()

class PrpfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"       

class UserProfileSerializer(serializers.ModelSerializer):    
    profile = PrpfileSerializer()
    class Meta:
        model = User
        fields = "__all__"



class KeySecretSerializer(serializers.ModelSerializer):
    def to_representation(self, data):
        data = super().to_representation(data)
        data['apiKey']    = decrypt(data['apiKey'], APIKEYPASS)
        data['secretKey'] = decrypt(data['secretKey'], SECKEYPASS)
        return data   
    class Meta:
        model  = Secret
        fields = "__all__"

class SecretStrategySerializer(serializers.ModelSerializer):
    secret = KeySecretSerializer(many=True)
    class Meta:
        model  = UserStrategy
        # exclude = ("strategy",)
        fields = "__all__"





# class TotalSerializer(serializers.ModelSerializer):
    
#     UserProfile    = UserProfileSerializer()
#     SecretStrategy = SecretStrategySerializer()

class TotalSerializer(serializers.Serializer):
    username                    = serializers.CharField()
    first_name                  = serializers.CharField(allow_blank=True)
    last_name                   = serializers.CharField(allow_blank=True)
    email                       = serializers.CharField()
    is_superuser                = serializers.BooleanField()
    is_staff                    = serializers.BooleanField()
    is_active                   = serializers.BooleanField()
    date_joined                 = serializers.DateTimeField()
    last_login                  = serializers.DateTimeField()
    image                       = serializers.ImageField()
    dateOfBirth                 = serializers.DateTimeField(allow_null=True)
    address                     = serializers.CharField(allow_null=True)
    addressVerified             = serializers.BooleanField()
    cellPhoneNumber             = PhoneNumberField()
    cellPhoneNumberVerified     = serializers.BooleanField()
    landingPhoneNumber          = PhoneNumberField(null=True)
    landingPhoneNumberVerified  = serializers.BooleanField()
    signedContract              = serializers.BooleanField()
    payedMemmber                = serializers.BooleanField()
    expirationTime              = serializers.DateTimeField()
    isEnable                    = serializers.BooleanField()
    createTime                  = serializers.DateTimeField()
    isActive                    = serializers.BooleanField()
    walletName                  = serializers.CharField(required=False, allow_null=True)
    apiKey                      = serializers.CharField(required=False)
    secretKey                   = serializers.CharField(required=False)
    createTime                  = serializers.DateTimeField(required=False)
    strategy                    = serializers.CharField(required=False)
    symbol                      = serializers.CharField(required=False)
    margin                      = serializers.FloatField(required=False)
    totallSL                    = serializers.FloatField(required=False)
    size                        = serializers.CharField(required=False, allow_null=True)
    isActive                    = serializers.BooleanField(required=False)
    baseCurrency                = serializers.CharField(required=False)
    leverage                    = serializers.IntegerField(required=False)
    marginType                  = serializers.CharField(required=False)
    positionMode                = serializers.CharField(required=False)
    timeInForce                 = serializers.CharField(required=False)
    workingType                 = serializers.CharField(required=False)
    priceProtect                = serializers.CharField(required=False)
    createTime                  = serializers.DateTimeField(required=False)
    deactivateTime              = serializers.DateTimeField(required=False)

    def to_representation(self, data):
        data = super().to_representation(data)
        data['apiKey']    = decrypt(data['apiKey'], APIKEYPASS)
        data['secretKey'] = decrypt(data['secretKey'], SECKEYPASS)
        return data



class NestedSerializer(serializers.Serializer):
    user = serializers.ListField(
            child = serializers.DictField(
                child=serializers.CharField()
                ),
            read_only = True
    )
    plan = serializers.ListField(
            child = serializers.DictField(
                child=serializers.CharField()
                ),
            read_only = True
    )