from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import RegistrationSerializer
# Create your views here.


class RegistrationAPI(GenericAPIView):
    """Endpoint for creating a user"""
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response("User has been created")
