from django.shortcuts import render, redirect
from django.http import HttpResponse

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group,User

from .models import *
from .serializers import *
from .decorators import *
# Create your views here.
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_roles=['serviceproviders'])
def createService(request):
  data = request.data
  # user = request.user
  service = Service.objects.create(
    # user = user,
    name = data["name"],
    about = data["about"],
    feasiblelocations = data["feasiblelocations"],
    rating = data["rating"],
  )

  service.save()
  return Response({"message":"content added"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_roles=['serviceproviders','clients'])
def listService(request):
  allservices = Service.objects.all()
  serializer = ServiceSerializer(allservices, many = True)
  return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_roles=['serviceproviders','clients'])
def listByProviderId(request, providerId):
    provider = User.objects.get(id=providerId)
    services = provider.service_set.all()
    serializer = ServiceSerializer(services, many = True)
    return Response(serailzer.data)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_roles=['serviceproviders','clients'])
def listById(request, pk):
  try:
    serviceById = Service.objects.get(_id=pk)
    serializer = ServiceSerializer(serviceById, many = False)
    return Response(serializer.data)
  except:
    return Response({"message":"id does not exist"},status = status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_roles=['serviceproviders'])
def editList(request, pk):
  data = request.data
  try:
    serviceById = Service.objects.get(_id=pk)
    serviceById.name = data['name']
    serviceById.about = data['about']
    serviceById.feasiblelocations = data['feasiblelocations']
    serviceById.rating = data['rating']

    serviceById.save()
    return Response({"message":"data updated"})
  except:
    return Response({"message":'id passed does not exist'},status = status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@allowed_users(allowed_roles=['serviceproviders'])
def deleteList(request, pk):
  try:
    serviceById = Service.objects.get(_id=pk)
    serviceById.delete()
    return Response({"message":"service deleted"},status=status.HTTP_200_OK)
  except:
    return Response({"message":"id does not exist to delete"},status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_client(request):
  try:
    username = request.data['username']
    password = request.data['password']
    email = request.data['email']

    user = User.objects.create_user(username,email,password)
    group = Group.objects.get(name='clients')
    user.groups.add(group)
    user.save()

    return Response({"message":"client created"},status=status.HTTP_200_OK)
  except:
    return Response({"message":"user already exists"},status=status.HTTP_400_BAD_REQUEST)
  
@api_view(['POST'])
@permission_classes([AllowAny])
def create_serviceprovider(request):
  try:
    username = request.data['username']
    password = request.data['password']
    email = request.data['email']

    user = User.objects.create_user(username,email,password)
    
    group = Group.objects.get(name='serviceproviders')  
    user.groups.add(group)
    user.save()
    
    
    return Response({"message":"user created"},status=status.HTTP_200_OK)
  except:
    return Response({"message":"user already exists"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def Logout(request):
    request.user.auth_token.delete()
    logout(request)
    return Response({"Message":"User Logged out successfully"})
