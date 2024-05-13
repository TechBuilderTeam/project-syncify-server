from django.shortcuts import render
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework import status
from rest_framework.response import Response
from accounts.models import User
from .serializers import UserSerializer

# Create your views here.
class VerifiedUserView(ListAPIView):
    queryset=User.objects.filter(is_verified=True)
    serializer_class=UserSerializer
    
class UnverifiedUserView(ListAPIView):
    queryset=User.objects.filter(is_verified=False)
    serializer_class=UserSerializer
    
class UserDetailView(RetrieveAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    lookup_field='email'
    
class UserDetailsView(RetrieveAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    lookup_field='id'