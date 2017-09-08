# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.http import urlquote

import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError


from infobox.models import Property
from infobox.serializers import PropertySerializer



class PropertyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows properties to be viewed or edited.
    """
    queryset = Property.objects.all()
    serializer_class = PropertySerializer


@api_view(['POST'])
def get_entity_info(request):
  """
  API endpoint to retrieve Wikidata information
  """
  entity_id = request.data.get('id') or ''
  lang = request.data.get('lang') or ''

  if entity_id == '':
    raise ValidationError('An entity ID must be given (add id parameter)', code=400)
  if lang == '':
    raise ValidationError('A language must be specified (add lang parameter)', code=400)

  return Response(request.data)




