from rest_framework import serializers
from profiles.models import Profile



class ContractSerializer(serializers.ModelSerializer):

    def save(self, **kwargs):

        if 'signedContract' in self.validated_data and \
            self.validated_data['signedContract']==False:
            self.validated_data['isEnable']=False
        return super().save(**kwargs)

    class Meta:
        model  = Profile
        fields = ("user","signedContract")