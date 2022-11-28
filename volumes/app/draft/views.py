from django.shortcuts import render
from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework import serializers

from .models import Person

from .serializers import PersonSerializer

# Create your views here.
class PreRegister(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, format=None):
        """
        Return a list registered persons.
        Methods: GET, POST
        :POST params: name, email, phone, comment
        """
        persons = Person.objects.all()
        serializer = PersonSerializer(persons, many=True)
        return Response({'persons':serializer.data})
    
    def post(self, request, *args, **kwargs):
        data = request.data
        # print(data)
        serializer = PersonSerializer(data=data)
        # print('here serializer:\n', serializer)
        if serializer.is_valid():
            serializer.save()
            # return Response({'adel':1234})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # print('not valiiiiiiiiiiiiiiiiiiiiiiiiiiid')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonDetailView(APIView):
    """
    update Person object info
    Method: PATCH
    :params: is_allow {False/True}
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return Person.objects.get(pk=pk)

    def patch(self, request, pk):
        testmodel_object = self.get_object(pk)
        serializer = PersonSerializer(testmodel_object, data=request.data, partial=True) # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data="wrong parameters",status=status.HTTP_400_BAD_REQUEST)

class AllowRegister(APIView):
    """
    check registration possibility
    if true, is allowed to register, else rejected
    """
    permission_classes=[permissions.AllowAny]

    def get(self, request):
        email = request.data.get('email')
        qs = Person.objects.get(email=email)
        # print(qs)
        # print(request.data.get('email'))
        if qs.isAllowed:
            return Response({'status': True})
        else:
            return Response({'status': False})


