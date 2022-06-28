from django.http import Http404

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from profiles.models import Profile
from contract.serializers import ContractSerializer



class Contract(APIView):
    """
    get-patch contract
    /contract/
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
        serializer = ContractSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def patch(self, request, *args, **kwargs):
        profile = self.get_object(userId=request.user.id)
        data = request.data       
        data['user'] = request.user.id
        serializer = ContractSerializer(profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
