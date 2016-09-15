import requests
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework import status
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from pentagram.serializers import UserSerializer, PhotoSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from pentagram.models import Photo
# Create your views here.


def login_auth(request, template_name):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)

        if user is not None:
            login(request, user)
            url = ''.join(['http://', get_current_site(request).domain, reverse('fetch_token')])
            response = requests.post(url, json={"username":username, "password":password})
            return HttpResponse(response.text, content_type = 'application/json', status=status.HTTP_200_OK )
        else:
            return HttpResponseBadRequest()
    else:
        if isinstance(request.user,User):
            return redirect(reverse('homepage'))
        else:
            context = {}
            return TemplateResponse(request, template_name, context)


@api_view(['POST'])
@permission_classes((AllowAny,))
def users(request):
    if request.method == 'POST':
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(status = status.HTTP_201_CREATED)
        return Response(status = status.HTTP_400_BAD_REQUEST, data = user_serializer.errors)


@api_view(['Get','POST'])
def photos(request):
    if request.method == 'GET':
        photos = Photo.objects.all()
        serializer = PhotoSerializer(photos, many = True)
        return Response(status = status.HTTP_200_OK, data = serializer.data)