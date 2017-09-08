# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from infobox.models import Property
from rest_framework import viewsets
from infobox.serializers import UserSerializer, PropertySerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows properties to be viewed or edited.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
