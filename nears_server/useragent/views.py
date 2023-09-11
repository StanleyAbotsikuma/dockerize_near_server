from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from .assignALGO import *
# Create your views here.


def login(request):
    context = {'message': 'Hello, world!'}
    return render(request, 'login.html', context)

def signup(request):
    context = {'message': 'Hello, world!'}
    return render(request, 'signup.html', context)


@authentication_classes([SessionAuthentication])
def webrtc_test(request):
    context = {'message': 'Hello, world!'}
    return render(request, 'admin.html', context)
