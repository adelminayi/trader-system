import os
from dotenv import load_dotenv
from cryptocode import encrypt,decrypt
from numpy import number

from rest_framework import serializers
from keysecrets.models import Secret



load_dotenv()
APIKEYPASS = os.getenv('APIKEYPASS')
SECKEYPASS = os.getenv('SECKEYPASS')


class SecretSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):
        if "uniquesign" in self.validated_data:
            self.validated_data.pop('uniquesign')
        if "apiKey" in self.validated_data and "secretKey" in self.validated_data:
            self.validated_data['uniquesign'] = self.validated_data['apiKey'][0:7] + self.validated_data['secretKey'][-8:]
            self.validated_data['apiKey'] = encrypt(self.validated_data['apiKey'], APIKEYPASS)
            self.validated_data['secretKey'] = encrypt(self.validated_data['secretKey'], SECKEYPASS)
        if "createTime" in self.validated_data:
            self.validated_data.pop('createTime')
        return super().save(**kwargs)

    def to_representation(self, data):
        data = super().to_representation(data)
        number_of_real_data = 8
        hidden_part = '•' * (64 - number_of_real_data)
        # data['apiKey']  = decrypt(data['apiKey'], APIKEYPASS)
        # data['secretKey'] = decrypt(data['secretKey'], SECKEYPASS)
        decrypted_apikey =  decrypt(data['apiKey'], APIKEYPASS)
        data['apiKey']    = f'{decrypted_apikey[:number_of_real_data]}{hidden_part}'
        decrypted_secretkey = decrypt(data['secretKey'], SECKEYPASS)
        data['secretKey'] = f'{decrypted_secretkey[:number_of_real_data]}{hidden_part}'

        return data
        
    class Meta:
        model  = Secret
        fields = "__all__"